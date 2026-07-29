#!/usr/bin/env bash
# BeWater skill installer (spec §9). Ships self-contained bw-* skills plus the shared
# _bw-shared/ references and the bwkit helper package. Default mode is --copy.
set -euo pipefail

VERSION="0.1.0"
MARKER=".bewater-managed"
MODE="copy"
DEST=""
SRC=""
UNINSTALL=0
MARKER_JSON='{"managed_by":"bewater","version":"'"$VERSION"'"}'

die() { echo "error: $*" >&2; exit 1; }

usage() {
  cat <<EOF
usage: install.sh [--copy|--link] [--dest DIR] [--src DIR] [--uninstall]
  --copy       copy skills into DEST (default)
  --link       symlink skill contents + bwkit into DEST (repo development)
  --dest DIR   destination skills dir (default: \$HOME/.claude/skills)
  --src DIR    repository root with .claude/skills and src/bwkit (default: this script's dir)
  --uninstall  remove only bewater-managed targets from DEST
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)       MODE="copy"; shift;;
    --link)       MODE="link"; shift;;
    --dest)       DEST="${2:?--dest needs a value}"; shift 2;;
    --src)        SRC="${2:?--src needs a value}"; shift 2;;
    --uninstall)  UNINSTALL=1; shift;;
    -h|--help)    usage; exit 0;;
    *)            die "unknown argument: $1";;
  esac
done

[[ -z "${SRC:-}" ]] && SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SRC/.claude/skills"
BWKIT_SRC="$SRC/src/bwkit"
[[ -d "$SKILLS_SRC" ]] || die "no .claude/skills under --src: $SRC"
[[ -d "$BWKIT_SRC" ]]  || die "no src/bwkit under --src: $SRC"

[[ -z "${DEST:-}" ]] && DEST="$HOME/.claude/skills"
mkdir -p "$DEST"

write_marker() { printf '%s\n' "$MARKER_JSON" > "$1/$MARKER"; }
has_marker()   { [[ -f "$1/$MARKER" ]]; }

# Replace a target from a staged dir, after verifying it is bewater-managed if it exists.
stage_replace() {
  local target="$1" staged="$2"
  if [[ -e "$target" || -L "$target" ]]; then
    has_marker "$target" || die "target exists and is not bewater-managed: $target"
  fi
  rm -rf "$target"
  mv "$staged" "$target"
  write_marker "$target"
}

deploy_unit() {
  local name="$1" srcdir="$SKILLS_SRC/$name"
  [[ -d "$srcdir" ]] || die "missing source unit: $name"
  local staged
  staged="$(mktemp -d "${TMPDIR:-/tmp}/bwinst.XXXXXX")"
  if [[ "$MODE" == "copy" ]]; then
    cp -R "$srcdir" "$staged/$name"
  else
    mkdir -p "$staged/$name"
    local f
    for f in "$srcdir"/*; do [[ -e "$f" ]] || continue; ln -s "$f" "$staged/$name/$(basename "$f")"; done
  fi
  stage_replace "$DEST/$name" "$staged/$name"
}

deploy_shared() {
  local staged
  staged="$(mktemp -d "${TMPDIR:-/tmp}/bwinst.XXXXXX")/_bw-shared"
  mkdir -p "$staged"
  local f
  for f in "$SKILLS_SRC/_bw-shared"/*.md; do
    [[ -e "$f" ]] || continue
    if [[ "$MODE" == "copy" ]]; then cp "$f" "$staged/"; else ln -s "$f" "$staged/$(basename "$f")"; fi
  done
  if [[ "$MODE" == "copy" ]]; then cp -R "$BWKIT_SRC" "$staged/bwkit"; else ln -s "$BWKIT_SRC" "$staged/bwkit"; fi
  stage_replace "$DEST/_bw-shared" "$staged"
}

uninstall_target() {
  local target="$1"
  if [[ ! -e "$target" && ! -L "$target" ]]; then return 0; fi
  if has_marker "$target" || [[ -L "$target" && ! -e "$target" ]]; then
    rm -rf "$target"
  else
    echo "skip (not bewater-managed): $target" >&2
  fi
}

main() {
  if (( UNINSTALL )); then
    local d
    for d in "$SKILLS_SRC"/*/; do
      [[ -d "$d" ]] || continue
      uninstall_target "$DEST/$(basename "$d")"
    done
    uninstall_target "$DEST/_bw-shared"
    echo "uninstalled bewater-managed skills from $DEST"
    return 0
  fi

  local units=() d
  for d in "$SKILLS_SRC"/bw-*/; do [[ -d "$d" ]] || continue; units+=("$(basename "$d")"); done
  [[ ${#units[@]} -gt 0 ]] || die "no bw-* skills found under $SKILLS_SRC"
  for name in "${units[@]}"; do deploy_unit "$name"; done
  deploy_shared
  echo "installed ${#units[@]} skill(s) + _bw-shared into $DEST (mode=$MODE)"
}

main "$@"

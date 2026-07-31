#!/usr/bin/env bash
# BeWater project installer. Deploys bw-* skills + bwkit into a project directory.
set -euo pipefail
shopt -s dotglob 2>/dev/null || true

VERSION="0.1.0"
MARKER=".bewater-managed"
MODE="copy"
DEST=""
SRC=""
PROJECT_ROOT=""
UNINSTALL=0
MARKER_JSON='{"managed_by":"bewater","version":"'"$VERSION"'"}'

die() { echo "error: $*" >&2; exit 1; }

usage() {
  cat <<EOF
usage: install.sh [--copy|--link] --project-root DIR [--src DIR] [--dest DIR] [--uninstall]

  --project-root DIR  (required) project root; skills → DIR/.claude/skills, bwkit → DIR/_bewater/bwkit
  --src DIR           repository root with .claude/skills and src/bwkit (default: this script's dir)
  --dest DIR          skills output dir (default: PROJECT_ROOT/.claude/skills)
  --copy              copy files (default)
  --link              symlink instead of copy (repo development)
  --uninstall         remove bewater-managed targets from project
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)           MODE="copy"; shift;;
    --link)           MODE="link"; shift;;
    --dest)           DEST="${2:?--dest needs a value}"; shift 2;;
    --project-root)   PROJECT_ROOT="${2:?--project-root needs a value}"; shift 2;;
    --src)            SRC="${2:?--src needs a value}"; shift 2;;
    --uninstall)      UNINSTALL=1; shift;;
    -h|--help)        usage; exit 0;;
    *)                die "unknown argument: $1";;
  esac
done

[[ -n "$PROJECT_ROOT" ]] || die "--project-root is required"
PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"  # resolve to absolute

[[ -z "${SRC:-}" ]] && SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SRC/src/skills"
BWKIT_SRC="$SRC/src/bwkit"
[[ -d "$SKILLS_SRC" ]] || die "no .claude/skills under --src: $SRC"
[[ -d "$BWKIT_SRC" ]]  || die "no src/bwkit under --src: $SRC"

[[ -z "${DEST:-}" ]] && DEST="$PROJECT_ROOT/.claude/skills"
mkdir -p "$DEST"

SKILLS_TARGET="$DEST"
BWKIT_TARGET="$PROJECT_ROOT/_bewater/bwkit"

# ---------------------------------------------------------------------------
# marker helpers
# ---------------------------------------------------------------------------
write_marker() { printf '%s\n' "$MARKER_JSON" > "$1/$MARKER"; }
has_marker() { [[ -f "$1/$MARKER" && ! -L "$1" ]] && grep -q '"managed_by":[[:space:]]*"bewater"' "$1/$MARKER"; }

# ---------------------------------------------------------------------------
# deploy helpers
# ---------------------------------------------------------------------------

# atomically replace target with staged content
stage_replace() {
  local target="$1" staged="$2"
  if [[ -e "$target" || -L "$target" ]]; then
    has_marker "$target" || die "target exists and is not bewater-managed: $target"
    rm -rf "$target"
  fi
  mv "$staged" "$target"
  write_marker "$target"
}

# stage a source dir into a temp, then atomically replace target
stage_dir() {
  local target="$1" srcdir="$2"
  local name; name="$(basename "$target")"
  local staged
  staged="$(mktemp -d "${TMPDIR:-/tmp}/bwinst.XXXXXX")"
  if [[ "$MODE" == "copy" ]]; then
    cp -R "$srcdir" "$staged/$name"
    find "$staged/$name" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
  else
    mkdir -p "$staged/$name"
    local f
    for f in "$srcdir"/*; do [[ -e "$f" ]] || continue; ln -s "$f" "$staged/$name/$(basename "$f")"; done
  fi
  stage_replace "$target" "$staged/$name"
}

# ---------------------------------------------------------------------------
# deploy skills (bw-*)
# ---------------------------------------------------------------------------
deploy_units() {
  local d count=0
  for d in "$SKILLS_SRC"/bw-*/; do
    [[ -d "$d" ]] || continue
    local name; name="$(basename "$d")"
    stage_dir "$SKILLS_TARGET/$name" "$d"
    ((count++))
  done
  [[ "$count" -gt 0 ]] || die "no bw-* skills found under $SKILLS_SRC"
}

# ---------------------------------------------------------------------------
# deploy _bw-shared (docs) + bwkit (tool)
# ---------------------------------------------------------------------------
deploy_shared() {
  # docs → DEST/_bw-shared/
  local staged_docs
  staged_docs="$(mktemp -d "${TMPDIR:-/tmp}/bwinst.XXXXXX")/_bw-shared"
  mkdir -p "$staged_docs"
  local f
  for f in "$SKILLS_SRC/_bw-shared"/*.md; do
    [[ -e "$f" ]] || continue
    if [[ "$MODE" == "copy" ]]; then cp "$f" "$staged_docs/"; else ln -s "$f" "$staged_docs/$(basename "$f")"; fi
  done
  stage_replace "$SKILLS_TARGET/_bw-shared" "$staged_docs"

  # bwkit → PROJECT_ROOT/_bewater/bwkit/; link mode keeps a real managed
  # directory and links its contents, so its marker never touches the source.
  mkdir -p "$PROJECT_ROOT/_bewater"
  stage_dir "$BWKIT_TARGET" "$BWKIT_SRC"
}

# ---------------------------------------------------------------------------
# uninstall
# ---------------------------------------------------------------------------
uninstall_target() {
  local target="$1"
  if [[ ! -e "$target" && ! -L "$target" ]]; then return 0; fi
  if has_marker "$target" || [[ -L "$target" && ! -e "$target" ]]; then
    rm -rf "$target"
  else
    echo "skip (not bewater-managed): $target" >&2
  fi
}

do_uninstall() {
  local d
  for d in "$SKILLS_TARGET"/bw-*/; do
    [[ -d "$d" ]] || continue
    uninstall_target "$d"
  done
  uninstall_target "$SKILLS_TARGET/_bw-shared"
  uninstall_target "$BWKIT_TARGET"
  echo "uninstalled bewater-managed targets from $PROJECT_ROOT"
}

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
main() {
  if (( UNINSTALL )); then
    do_uninstall
    return 0
  fi

  deploy_units
  deploy_shared

  local count=0 d
  for d in "$SKILLS_TARGET"/bw-*/; do [[ -d "$d" ]] || continue; ((count++)); done
  echo "installed $count skill(s) into $SKILLS_TARGET, bwkit into $BWKIT_TARGET (mode=$MODE)"
}

main "$@"

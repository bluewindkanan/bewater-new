#!/usr/bin/env bash
# BeWater 文档 HTML 生成脚本
# 用法: ./scripts/html-build.sh [项目根目录]

set -e

# 项目根目录（默认当前目录）
PROJECT_ROOT="${1:-$(pwd)}"

# 路径配置
OUTPUT_DIR="$PROJECT_ROOT/_bewater-output"
KNOWLEDGE_DIR="$OUTPUT_DIR/knowledge"
ARTIFACTS_DIR="$OUTPUT_DIR/artifacts"
HTML_DIR="$OUTPUT_DIR/html"
HTML_KNOWLEDGE="$HTML_DIR/knowledge"
HTML_ARTIFACTS="$HTML_DIR/artifacts"
CSS_FILE="$PROJECT_ROOT/resources/bewater-doc.css"

# 检查 pandoc
if ! command -v pandoc &> /dev/null; then
  echo "错误: 未找到 pandoc"
  echo "请安装: brew install pandoc"
  exit 1
fi

# 检查 CSS 文件
if [[ ! -f "$CSS_FILE" ]]; then
  echo "错误: 未找到样式文件 $CSS_FILE"
  exit 1
fi

echo "=== BeWater HTML 生成 ==="
echo "项目根目录: $PROJECT_ROOT"

# 创建输出目录
mkdir -p "$HTML_KNOWLEDGE" "$HTML_ARTIFACTS"

# 复制 CSS 文件
cp "$CSS_FILE" "$HTML_DIR/bewater-doc.css"

# 函数：转换单个文件
convert_file() {
  local src="$1"
  local dst="$2"
  local basename=$(basename "$src" .md)

  # pandoc 转换
  pandoc -f markdown -t html \
    --standalone \
    --css=bewater-doc.css \
    --metadata title="$basename" \
    -o "$dst" "$src"

  echo "  → $basename"
}

# 函数：遍历目录转换
convert_dir() {
  local src_dir="$1"
  local dst_dir="$2"

  if [[ ! -d "$src_dir" ]]; then
    echo "跳过: $src_dir 不存在"
    return
  fi

  echo "转换目录: $src_dir"

  for md_file in "$src_dir"/*.md; do
    if [[ -f "$md_file" ]]; then
      local basename=$(basename "$md_file" .md)
      convert_file "$md_file" "$dst_dir/$basename.html"
    fi
  done
}

# 转换 Knowledge 文档
echo ""
echo "[1/3] 转换 Knowledge 工论文..."
convert_dir "$KNOWLEDGE_DIR" "$HTML_KNOWLEDGE"

# 转换 Artifacts
echo ""
echo "[2/3] 转换 Artifacts..."
convert_dir "$ARTIFACTS_DIR" "$HTML_ARTIFACTS"

# 后处理：引用链接转换
echo ""
echo "[3/3] 后处理 HTML 文件..."
python3 "$PROJECT_ROOT/scripts/html-postprocess.py" "$HTML_DIR"

echo ""
echo "=== 完成 ==="
echo "HTML 输出目录: $HTML_DIR"
echo ""
echo "打开方式:"
echo "  file://$HTML_DIR/index.html"

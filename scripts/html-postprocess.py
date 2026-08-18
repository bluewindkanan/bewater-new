#!/usr/bin/env python3
"""HTML 后处理：引用链接转换 + 索引生成"""

import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List

# 引用链接正则模式
KNOWLEDGE_REF = re.compile(r'knowledge:(K-\d+)@(\d+)')
ARTIFACT_REF = re.compile(r'artifact:((?:ART|EXP)-\d+)@(\d+)')
EVIDENCE_REF = re.compile(r'evidence:E-\d+@\d+')

# YAML frontmatter 解析
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)


@dataclass
class DocMeta:
    """文档元数据"""
    doc_id: str
    revision: int
    title: str = ""
    status: str = ""
    kind: str = ""
    stage: str = ""


def parse_frontmatter(content: str) -> DocMeta | None:
    """解析 YAML frontmatter"""
    match = FRONTMATTER_RE.search(content)
    if not match:
        return None

    try:
        import yaml
        fm = yaml.safe_load(match.group(1))
        if not isinstance(fm, dict):
            return None

        # 提取元数据
        doc_id = fm.get('knowledge_id') or fm.get('artifact_id')
        revision = fm.get('revision', 1)
        title = fm.get('title', '')
        status = fm.get('status', '')
        kind = fm.get('kind', '')
        stage = fm.get('stage', '')

        if doc_id:
            return DocMeta(doc_id, revision, title, status, kind, stage)
    except Exception:
        pass

    return None


def convert_refs_in_html(content: str, html_path: Path) -> str:
    """转换 HTML 中的引用链接"""

    def replace_knowledge(m: re.Match) -> str:
        doc_id, rev = m.group(1), m.group(2)
        # 链接到 knowledge 目录
        return f'<a href="../knowledge/{doc_id}.html" class="ref-link">{m.group(0)}</a>'

    def replace_artifact(m: re.Match) -> str:
        doc_id, rev = m.group(1), m.group(2)
        # 链接到 artifacts 目录
        return f'<a href="../artifacts/{doc_id}.html" class="ref-link">{m.group(0)}</a>'

    # 转换引用
    content = KNOWLEDGE_REF.sub(replace_knowledge, content)
    content = ARTIFACT_REF.sub(replace_artifact, content)
    # evidence 保持原样（暂不支持）

    return content


def add_meta_card(content: str, meta: DocMeta, html_path: Path) -> str:
    """在 HTML 中添加元数据卡片"""

    if meta is None:
        return content

    # 确定状态样式
    status_class = "status-complete" if meta.status == "complete" else "status-working"
    status_text = meta.status or "unknown"

    # 构建元数据卡片 HTML
    meta_html = f"""
<div class="meta-card">
  <div class="meta-row">
    <span class="meta-label">ID:</span>
    <span class="meta-value">{meta.doc_id}<span class="version-badge">r{meta.revision}</span></span>
  </div>
  <div class="meta-row">
    <span class="meta-label">Status:</span>
    <span class="meta-value"><span class="status-badge {status_class}">{status_text}</span></span>
  </div>
"""

    if meta.title:
        meta_html += f"""
  <div class="meta-row">
    <span class="meta-label">Title:</span>
    <span class="meta-value">{meta.title}</span>
  </div>
"""

    if meta.kind:
        meta_html += f"""
  <div class="meta-row">
    <span class="meta-label">Type:</span>
    <span class="meta-value">{meta.kind}</span>
  </div>
"""

    if meta.stage:
        meta_html += f"""
  <div class="meta-row">
    <span class="meta-label">Stage:</span>
    <span class="meta-value">{meta.stage}</span>
  </div>
"""

    meta_html += "</div>\n"

    # 插入到 body 开始后
    content = re.sub(
        r'(<body[^>]*>)',
        r'\1' + meta_html,
        content,
        count=1
    )

    return content


def process_html_file(html_path: Path) -> DocMeta | None:
    """处理单个 HTML 文件"""
    content = html_path.read_text(encoding='utf-8')

    # 从原始 MD 读取元数据
    md_path = html_path.with_suffix('.md').parent.parent / \
              html_path.parent.name[:-1] / \
              html_path.with_suffix('.md').name

    # 尝试不同的 MD 路径
    possible_md_paths = [
        html_path.with_suffix('.md'),  # 同目录
        html_path.parent.parent / 'knowledge' / html_path.with_suffix('.md').name,
        html_path.parent.parent / 'artifacts' / html_path.with_suffix('.md').name,
    ]

    meta = None
    for md_path in possible_md_paths:
        if md_path.exists():
            md_content = md_path.read_text(encoding='utf-8')
            meta = parse_frontmatter(md_content)
            if meta:
                break

    # 转换引用链接
    content = convert_refs_in_html(content, html_path)

    # 添加元数据卡片
    if meta:
        content = add_meta_card(content, meta, html_path)

    # 写回
    html_path.write_text(content, encoding='utf-8')

    return meta


def collect_docs(html_dir: Path) -> List[DocMeta]:
    """收集所有文档元数据"""
    docs = []

    for subdir in ['knowledge', 'artifacts']:
        sub_path = html_dir / subdir
        if not sub_path.exists():
            continue

        for html_file in sub_path.glob('*.html'):
            if html_file.name == 'index.html':
                continue
            meta = process_html_file(html_file)
            if meta:
                docs.append(meta)

    return docs


def generate_index(docs: List[DocMeta], html_dir: Path):
    """生成索引页"""

    # 分组文档
    knowledge_docs = [d for d in docs if d.doc_id.startswith('K-')]
    artifact_docs = [d for d in docs if d.doc_id.startswith(('ART-', 'EXP-'))]

    # 按子页面分组 artifacts
    def group_artifacts(arts: List[DocMeta]) -> dict:
        groups = {}
        for a in arts:
            key = a.stage or 'other'
            if key not in groups:
                groups[key] = []
            groups[key].append(a)
        return groups

    artifact_groups = group_artifacts(artifact_docs)

    # 生成 HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BeWater 文档索引</title>
  <link rel="stylesheet" href="bewater-doc.css">
</head>
<body class="index-page">
  <h1>BeWater 文档索引</h1>

  <div class="index-section">
    <h2>Knowledge 工论文 ({len(knowledge_docs)})</h2>
    <ul class="index-list">
'''

    for doc in sorted(knowledge_docs, key=lambda d: d.doc_id):
        status_class = "status-complete" if doc.status == "complete" else "status-working"
        html += f'''
      <li class="index-item">
        <span class="id">{doc.doc_id}<span class="version-badge">r{doc.revision}</span></span>
        <span class="title">{doc.title or doc.doc_id}</span>
        <span class="meta"><span class="status-badge {status_class}">{doc.status or 'unknown'}</span></span>
      </li>'''

    html += '''
    </ul>
  </div>

  <div class="index-section">
    <h2>Artifacts ({len(artifact_docs)})</h2>
'''

    for stage, docs in sorted(artifact_groups.items()):
        html += f'    <h3>{stage} ({len(docs)})</h3>\n    <ul class="index-list">\n'

        for doc in sorted(docs, key=lambda d: d.doc_id):
            status_class = "status-complete" if doc.status == "complete" else "status-working"
            kind_label = doc.kind or ''
            html += f'''
      <li class="index-item">
        <span class="id">{doc.doc_id}<span class="version-badge">r{doc.revision}</span></span>
        <span class="title">{doc.title or doc.doc_id}</span>
        <span class="meta">{kind_label} <span class="status-badge {status_class}">{doc.status or 'unknown'}</span></span>
      </li>'''

        html += '    </ul>\n'

    html += '''
  </div>

  <a href="knowledge/index.html" class="back-link">→ Knowledge 目录</a>
  <a href="artifacts/index.html" class="back-link">→ Artifacts 目录</a>

</body>
</html>'''

    (html_dir / 'index.html').write_text(html, encoding='utf-8')

    # 生成子索引页
    generate_sub_index(knowledge_docs, html_dir / 'knowledge', 'Knowledge 工论文')
    generate_sub_index(artifact_docs, html_dir / 'artifacts', 'Artifacts')


def generate_sub_index(docs: List[DocMeta], sub_dir: Path, title: str):
    """生成子目录索引页"""
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} - BeWater</title>
  <link rel="stylesheet" href="../bewater-doc.css">
</head>
<body>
  <h1>{title}</h1>
  <p><a href="../index.html" class="back-link">← 返回总索引</a></p>

  <ul class="index-list">
'''

    for doc in sorted(docs, key=lambda d: d.doc_id):
        status_class = "status-complete" if doc.status == "complete" else "status-working"
        html += f'''
  <li class="index-item">
    <span class="id">{doc.doc_id}<span class="version-badge">r{doc.revision}</span></span>
    <span class="title"><a href="{doc.doc_id}.html">{doc.title or doc.doc_id}</a></span>
    <span class="meta"><span class="status-badge {status_class}">{doc.status or 'unknown'}</span></span>
  </li>'''

    html += '''
  </ul>
</body>
</html>'''

    sub_dir.mkdir(parents=True, exist_ok=True)
    (sub_dir / 'index.html').write_text(html, encoding='utf-8')


def main():
    import sys

    if len(sys.argv) < 2:
        print("用法: html-postprocess.py <html_dir>")
        sys.exit(1)

    html_dir = Path(sys.argv[1])

    if not html_dir.exists():
        print(f"错误: 目录不存在 {html_dir}")
        sys.exit(1)

    print("处理 HTML 文件...")
    docs = collect_docs(html_dir)

    print(f"  收集到 {len(docs)} 个文档")

    print("生成索引页...")
    generate_index(docs, html_dir)

    print("  → 索引页生成完成")


if __name__ == '__main__':
    main()

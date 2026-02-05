#!/usr/bin/env python3
"""
微信公众号排版模板应用脚本（基础版本）
注意：这是一个示例脚本，实际使用时可能需要根据具体模板结构调整
"""

import re
import sys
from pathlib import Path

def load_template(template_path: str) -> str:
    """加载HTML模板文件"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_sections(content: str) -> dict:
    """
    从文章内容中提取不同部分
    这是一个简单实现，实际需要更复杂的解析
    """
    lines = content.strip().split('\n')

    sections = {
        'title': '',
        'paragraphs': [],
        'headings': []
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 提取标题
        if line.startswith('# '):
            sections['title'] = re.sub(r'^#+\s*', '', line)
        elif line.startswith('## '):
            heading = re.sub(r'^#+\s*', '', line)
            sections['headings'].append(heading)
        else:
            sections['paragraphs'].append(line)

    return sections

def apply_basic_template(template: str, sections: dict) -> str:
    """
    将内容应用到模板（基础版本）
    这个函数需要根据具体模板结构调整
    """
    # 简单替换示例
    result = template

    # 替换标题（如果模板中有{{title}}占位符）
    if '{{title}}' in template:
        result = result.replace('{{title}}', sections['title'])

    # 替换内容（如果模板中有{{content}}占位符）
    if '{{content}}' in template:
        # 简单的内容组合
        content_html = ""
        for para in sections['paragraphs'][:5]:  # 只取前5段
            content_html += f'<p style="margin: 0 0 20px 0;">{para}</p>\n'

        result = result.replace('{{content}}', content_html)

    return result

def create_wechat_html(title: str, content: str, style_name: str) -> str:
    """
    创建微信公众号HTML（简化版本）
    实际使用时应该基于具体模板文件
    """
    # 基础微信公众号HTML结构
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body style="margin: 0; padding: 0;">

<section style="max-width: 100%; box-sizing: border-box;
                font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif;
                color: #333; line-height: 1.75; font-size: 15px;
                background: #fff; padding: 20px 15px;">

    <!-- 标题区域 -->
    <section style="margin-top: 40px; margin-bottom: 20px; display: flex; align-items: center;">
        <span style="display: block; width: 4px; height: 18px; background-color: #000; margin-right: 12px;"></span>
        <h2 style="font-size: 18px; font-weight: bold; color: #000; margin: 0; letter-spacing: 1px;">{title}</h2>
    </section>

    <!-- 内容区域 -->
    <div style="margin-top: 30px;">
'''

    # 添加内容段落
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    for para in paragraphs:
        # 跳过标题行
        if para.startswith('#') or para.startswith('##'):
            continue
        html += f'        <p style="margin: 0 0 20px 0; text-align: justify;">{para}</p>\n'

    html += '''    </div>

    <!-- 页脚 -->
    <section style="text-align: right; margin-top: 40px;">
        <p style="margin: 0; font-size: 12px; color: #999; letter-spacing: 2px;">FORMATTED BY WECHAT ARTICLE SKILL</p>
    </section>

</section>
</body>
</html>'''

    return html

if __name__ == "__main__":
    # 使用示例
    if len(sys.argv) < 3:
        print("用法: python apply_template.py <文章文件> <风格名称>")
        print("示例: python apply_template.py article.txt 极简时尚")
        print("\n可用风格:")
        print("  - 极简时尚 (index.html)")
        print("  - 扁平风格 (扁平风格.html)")
        print("  - 像素风格 (像素.html)")
        print("  - ... 其他风格见 assets/templates/")
        sys.exit(1)

    article_file = sys.argv[1]
    style_name = sys.argv[2]

    # 读取文章内容
    with open(article_file, 'r', encoding='utf-8') as f:
        article_content = f.read()

    # 提取标题
    title = "Untitled"
    lines = article_content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            title = re.sub(r'^#+\s*', '', line)
            break
        elif line:
            title = line[:50]  # 取第一行前50字符
            break

    # 生成HTML
    html_content = create_wechat_html(title, article_content, style_name)

    # 输出文件名
    output_file = re.sub(r'[^\w\u4e00-\u9fff]', '_', title) + '.html'
    output_file = output_file[:100]  # 限制文件名长度

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"已生成HTML文件: {output_file}")
    print("注意: 这是一个基础版本，建议根据具体风格模板手动调整样式")
    print("参考 assets/templates/ 目录下的模板文件获取完整样式")
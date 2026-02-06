#!/usr/bin/env python3
"""
微信公众号排版与图片生成整合脚本

功能：
1. 分析文章内容生成prompts
2. 调用AI生成图片
3. 在Markdown文件中引用生成的图片
4. 将图片插入到HTML排版中
"""

import os
import sys
import re
import uuid
import requests
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
def load_env():
    """加载.env文件中的环境变量"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(os.path.dirname(script_dir))
    env_path = os.path.join(skill_dir, '.env')

    if os.path.exists(env_path):
        load_dotenv(env_path)
        return True
    return False

# 初始化客户端
def init_client():
    """初始化OpenAI客户端（豆包API）"""
    load_env()

    api_key = os.environ.get('ARK_API_KEY')
    if not api_key:
        print("错误：未设置ARK_API_KEY环境变量")
        print("请在.env文件中添加：ARK_API_KEY=your_api_key")
        sys.exit(1)

    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=api_key,
    )
    return client

# 提取标题
def extract_title(content: str) -> str:
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:
            if line.startswith('#'):
                title = re.sub(r'^#+\s*', '', line)
                return title
            return line
    return "Untitled"

# 提取摘要
def extract_summary(content: str, max_length: int = 200) -> str:
    lines = content.strip().split('\n')
    content_without_title = []
    for i, line in enumerate(lines):
        line = line.strip()
        if i == 0 and (line.startswith('#') or line == extract_title(content)):
            continue
        content_without_title.append(line)

    text = ' '.join(content_without_title)

    if len(text) <= max_length:
        return text

    cutoff = max_length
    for punct in ['.', '。', '!', '！', '?', '？']:
        last_pos = text.rfind(punct, 0, max_length + 10)
        if last_pos > 0:
            cutoff = last_pos + 1
            break

    return text[:cutoff].strip()

# 生成优化后的prompt
def generate_optimized_prompt(user_description: str, style: str = "") -> str:
    client = init_client()

    system_prompt = """You are an expert at writing image generation prompts. Your task is to:
1. Analyze user's description
2. Create a detailed, professional English prompt optimized for AI image generation
3. Include details about: subject, style, lighting, composition, mood, and quality
4. Ensure prompt is concise but comprehensive (50-150 words)
5. Focus on visual elements that AI image generators excel at understanding

Return ONLY optimized prompt text, no explanations."""

    user_prompt = f"Style preference: {style}\nDescription: {user_description}" if style else user_description

    response = client.chat.completions.create(
        model="doubao-pro-32k-241215",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()

# 生成图片
def generate_image(prompt: str, size: str = None, width: int = None, height: int = None, output_dir: str = "images") -> Optional[str]:
    client = init_client()

    # 确定图片尺寸
    if size == "cover" or size == "封面":
        final_size = "900x383"
    elif size == "banner" or size == "横幅":
        final_size = "900x300"
    elif size == "content" or size == "配图":
        final_size = "900x600"
    elif width and height:
        final_size = f"{width}x{height}"
    else:
        final_size = "900x600"

    try:
        images_response = client.images.generate(
            model="doubao-seedream-4-0-250828",
            prompt=prompt,
            size=final_size,
            response_format="url",
            extra_body={"watermark": False},
        )

        image_url = images_response.data[0].url

        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_output_dir = os.path.join(script_dir, output_dir)
        os.makedirs(full_output_dir, exist_ok=True)

        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            file_name = f"{uuid.uuid4()}.png"
            file_path = os.path.join(full_output_dir, file_name)

            with open(file_path, "wb") as f:
                f.write(image_response.content)

            return file_path

    except Exception as e:
        print(f"生成图片时发生错误: {str(e)}")
        return None

# 生成封面图prompt
def generate_cover_prompt(title: str, summary: str) -> str:
    prompt = f"A professional wechat article cover image about '{title}'. "
    prompt += f"The article discusses: {summary[:100]}... "
    prompt += "Style: modern tech minimalistic, clean, elegant, suitable for professional audience. "
    prompt += "High quality, detailed, 4K resolution, horizontal layout."
    return prompt

# 生成文中配图prompts
def generate_content_prompts(content: str, num_prompts: int = 3) -> List[str]:
    sentences = re.split(r'[。！？\.!\?]', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    prompts = []
    for i in range(min(num_prompts, len(sentences))):
        sentence = sentences[i]
        prompt = f"An illustration for article content: '{sentence[:50]}...'. "
        prompt += "Clean, professional, vector style, suitable for wechat article, horizontal layout."
        prompts.append(prompt)

    while len(prompts) < num_prompts:
        prompts.append(
            f"An illustration for wechat article about '{extract_title(content)}'. "
            "Clean, professional, vector style, horizontal layout."
        )

    return prompts

# 创建Markdown文件（包含图片引用）
def create_markdown_with_images(title: str, summary: str, cover_prompt: str,
                              cover_image: str, content_prompts: List[str],
                              content_images: List[str]) -> str:
    md = f"""# {title}

## 文章简介
{summary}

## 封面图
**Prompt:**
{cover_prompt}

**图片:**
![封面图](../{cover_image})

## 文中配图
"""

    for i, (prompt, img) in enumerate(zip(content_prompts, content_images), 1):
        md += f"""
### 配图 {i}

**Prompt:**
{prompt}

**图片:**
![配图{i}](../{img})

"""

    return md

# 查找模板文件
def find_template(style_name: str) -> Optional[str]:
    """根据风格名称查找模板文件"""
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'templates')

    # 常见的风格映射
    style_map = {
        '极简时尚': 'index.html',
        '极简': 'index.html',
        '简约': 'index.html',
        '扁平': '扁平风格.html',
        '扁平风格': '扁平风格.html',
        '像素': '像素.html',
        '像素风格': '像素.html',
        '科技像素': '科技简约像素.html',
        '科技简约像素': '科技简约像素.html',
        '弥散': '弥散风格.html',
        '弥散风格': '弥散风格.html',
        '手绘': '手绘风格.html',
        '手绘风格': '手绘风格.html',
        '玻璃': '玻璃拟态风格.html',
        '玻璃拟态': '玻璃拟态风格.html',
        '酸性': '酸性设计.html',
        '酸性设计': '酸性设计.html',
        '新粗野': '新粗野风格.html',
        '新粗野风格': '新粗野风格.html',
    }

    # 查找HTML文件
    if style_name in style_map:
        template_file = os.path.join(template_dir, style_map[style_name])
    elif style_name.endswith('.html'):
        template_file = os.path.join(template_dir, style_name)
    else:
        template_file = os.path.join(template_dir, f'{style_name}.html')

    if os.path.exists(template_file):
        return template_file

    # 查找所有HTML文件
    for f in os.listdir(template_dir):
        if f.endswith('.html'):
            file_path = os.path.join(template_dir, f)
            return file_path

    return None

# 将图片插入HTML模板
def insert_images_to_html(template_path: str, cover_image: str,
                         content_images: List[str], output_path: str):
    """读取模板并插入图片，生成最终HTML"""
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 查找图片插入位置（在img标签附近）
    lines = html_content.split('\n')
    content_images_count = 0

    # 插入封面图
    for i, line in enumerate(lines):
        if 'img src=' in line and content_images_count == 0:
            # 替换第一个img为封面图
            new_line = line
            new_line = re.sub(r'src="[^"]+"', f'src="../{cover_image}"', new_line)
            lines[i] = new_line
            content_images_count += 1

        # 插入文中配图
        elif'img src=' in line and content_images_count <= len(content_images):
            img_index = content_images_count - 1
            if 0 <= img_index < len(content_images):
                new_line = re.sub(r'src="[^"]+"', f'src="../{content_images[img_index]}"', line)
                lines[i] = new_line
                content_images_count += 1

    # 保存HTML
    html_content = '\n'.join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

# 主函数
def main():
    parser = argparse.ArgumentParser(description="微信公众号排版与图片生成工具")
    parser.add_argument("--article", "-a", required=True, help="文章文件路径")
    parser.add_argument("--style", "-s", default="index.html", help="风格名称")
    parser.add_argument("--output-dir", "-o", default="output", help="输出目录")

    args = parser.parse_args()

    # 读取文章内容
    with open(args.article, 'r', encoding='utf-8') as f:
        article_content = f.read()

    # 提取信息
    title = extract_title(article_content)
    summary = extract_summary(article_content)

    print("=" * 60)
    print("步骤 1/5: 分析文章内容...")
    print("=" * 60)
    print(f"标题: {title}")
    print(f"摘要: {summary[:100]}...")

    # 生成prompts
    print("\n" + "=" * 60)
    print("步骤 2/5: 生成图片提示词...")
    print("=" * 60)

    cover_prompt = generate_cover_prompt(title, summary)
    print(f"封面图prompt: {cover_prompt[:100]}...")

    content_prompts = generate_content_prompts(article_content, 3)
    for i, p in enumerate(content_prompts, 1):
        print(f"配图{i} prompt: {p[:80]}...")

    # 生成图片
    print("\n" + "=" * 60)
    print("步骤 3/5: 生成图片...")
    print("=" * 60)

    cover_image = generate_image(cover_prompt, size="cover")
    if not cover_image:
        print("封面图生成失败")
        return

    print(f"封面图已保存: {cover_image}")

    content_images = []
    for i, prompt in enumerate(content_prompts, 1):
        print(f"生成配图 {i}/{len(content_prompts)}...")
        img = generate_image(prompt, size="content")
        if img:
            content_images.append(img)
            print(f"  已保存: {img}")
        else:
            print(f"  配图{i}生成失败")
            content_images.append("")

    # 创建输出目录
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    # 创建Markdown文件
    print("\n" + "=" * 60)
    print("步骤 4/5: 创建Markdown文件（包含图片引用）...")
    print("=" * 60)

    safe_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)[:100]
    md_path = os.path.join(output_dir, f"{safe_title}.md")
    md_content = create_markdown_with_images(
        title, summary, cover_prompt, cover_image,
        content_prompts, content_images
    )

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Markdown文件已保存: {md_path}")

    # 查找模板并生成HTML
    print("\n" + "=" * 60)
    print("步骤 5/5: 生成HTML文件（插入图片）...")
    print("=" * 60)

    template_path = find_template(args.style)
    if not template_path:
        print(f"未找到模板: {args.style}")
        print("使用默认模板...")
        template_path = find_template('极简时尚')

    html_path = os.path.join(output_dir, f"{safe_title}.html")
    insert_images_to_html(template_path, cover_image, content_images, html_path)
    print(f"HTML文件已保存: {html_path}")

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)
    print(f"输出目录: {output_dir}")
    print(f"- Markdown: {md_path}")
    print(f"- HTML: {html_path}")
    print(f"- 封面图: {cover_image}")
    print(f"- 配图: {len([i for i in content_images if i])} 张")

if __name__ == "__main__":
    main()

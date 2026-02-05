#!/usr/bin/env python3
"""
微信公众号排版文章处理脚本
功能：提取文章标题、摘要，生成配图prompt
"""

import re
import sys
from typing import Tuple, List, Dict

def extract_title(content: str) -> str:
    """
    从文章内容中提取标题
    规则：第一行非空行作为标题，或包含#号的行
    """
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:
            # 如果以#开头，提取标题
            if line.startswith('#'):
                # 移除#号和空格
                title = re.sub(r'^#+\s*', '', line)
                return title
            # 否则第一行非空行作为标题
            return line
    return "Untitled"

def extract_summary(content: str, max_length: int = 200) -> str:
    """
    提取文章摘要
    规则：取文章前n个字符，确保句子完整
    """
    # 移除标题
    lines = content.strip().split('\n')
    content_without_title = []
    for i, line in enumerate(lines):
        line = line.strip()
        if i == 0 and (line.startswith('#') or line == extract_title(content)):
            continue  # 跳过标题行
        content_without_title.append(line)

    text = ' '.join(content_without_title)

    # 截取到最大长度，但确保句子完整
    if len(text) <= max_length:
        return text

    # 查找最后一个句号、问号或感叹号
    cutoff = max_length
    for punct in ['.', '。', '!', '！', '?', '？']:
        last_pos = text.rfind(punct, 0, max_length + 10)
        if last_pos > 0:
            cutoff = last_pos + 1
            break

    return text[:cutoff].strip()

def generate_image_prompt(title: str, summary: str, style: str = "modern minimalistic") -> str:
    """
    生成配图prompt
    """
    # 基于标题和摘要生成prompt
    prompt = f"A professional wechat article cover image about '{title}'. "
    prompt += f"The article discusses: {summary[:100]}... "
    prompt += f"Style: {style}, clean, elegant, suitable for professional audience. "
    prompt += "High quality, detailed, 4K resolution."

    return prompt

def generate_content_prompts(content: str, num_prompts: int = 3) -> List[str]:
    """
    生成文章内容配图prompt（用于文中配图）
    提取关键句子或关键词生成prompt
    """
    # 简单实现：提取包含关键字的句子
    sentences = re.split(r'[。！？\.!\?]', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    prompts = []
    for i in range(min(num_prompts, len(sentences))):
        sentence = sentences[i]
        prompt = f"An illustration for article content: '{sentence[:50]}...'. "
        prompt += "Clean, professional, vector style, suitable for wechat article."
        prompts.append(prompt)

    # 如果句子不足，用摘要补充
    while len(prompts) < num_prompts:
        prompts.append(
            f"An illustration for wechat article about '{extract_title(content)}'. "
            "Clean, professional, vector style."
        )

    return prompts

def process_article(content: str) -> Dict:
    """
    处理文章，返回结构化信息
    """
    title = extract_title(content)
    summary = extract_summary(content)
    cover_prompt = generate_image_prompt(title, summary)
    content_prompts = generate_content_prompts(content)

    return {
        "title": title,
        "summary": summary,
        "cover_prompt": cover_prompt,
        "content_prompts": content_prompts
    }

if __name__ == "__main__":
    # 命令行使用示例
    if len(sys.argv) > 1:
        # 从文件读取内容
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # 从标准输入读取
        content = sys.stdin.read()

    result = process_article(content)

    print("文章处理结果:")
    print(f"标题: {result['title']}")
    print(f"摘要: {result['summary']}")
    print(f"封面图prompt: {result['cover_prompt']}")
    print("\n文中配图prompts:")
    for i, prompt in enumerate(result['content_prompts'], 1):
        print(f"{i}. {prompt}")
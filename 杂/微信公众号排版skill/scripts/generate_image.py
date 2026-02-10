#!/usr/bin/env python3
"""
微信公众号配图生成脚本

功能：根据用户提供的描述，调用豆包大模型生成图片
使用方式：先展示生成的prompt给用户审核，确认后再生成图片

依赖：
    - openai
    - requests
    - python-dotenv

环境变量：
    - ARK_API_KEY: 火山引擎API密钥
"""

import os
import sys
import json
import argparse
import requests
import uuid
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
def load_env():
    """加载.env文件中的环境变量"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
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

# 生成优化后的prompt
def generate_optimized_prompt(user_description: str, style: str = "") -> str:
    """
    调用大模型生成优化后的图片生成prompt

    Args:
        user_description: 用户的原始描述
        style: 可选的风格提示

    Returns:
        优化后的英文prompt
    """
    client = init_client()

    system_prompt = """You are an expert at writing image generation prompts. Your task is to:
1. Analyze the user's description
2. Create a detailed, professional English prompt optimized for AI image generation
3. Include details about: subject, style, lighting, composition, mood, and quality
4. Ensure the prompt is concise but comprehensive (50-150 words)
5. Focus on visual elements that AI image generators excel at understanding

Return ONLY the optimized prompt text, no explanations."""

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
def generate_image(prompt: str, size: str = "2K", output_dir: str = "images") -> Optional[str]:
    """
    调用豆包API生成图片

    Args:
        prompt: 图片生成提示词
        size: 图片尺寸 (支持 "1K", "2K", "4K" 等)
        output_dir: 图片保存目录

    Returns:
        保存的图片路径，失败返回None
    """
    client = init_client()

    try:
        images_response = client.images.generate(
            model="doubao-seedream-4-0-250828",
            prompt=prompt,
            size=size,
            response_format="url",
            extra_body={
                "watermark": False,
            },
        )

        # 获取生成的图片URL
        image_url = images_response.data[0].url
        print(f"图片URL: {image_url}")

        # 确保输出目录存在
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_output_dir = os.path.join(script_dir, output_dir)
        os.makedirs(full_output_dir, exist_ok=True)

        # 下载图片到本地
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # 生成唯一的文件名
            file_name = f"{uuid.uuid4()}.png"
            file_path = os.path.join(full_output_dir, file_name)

            with open(file_path, "wb") as f:
                f.write(image_response.content)

            print(f"图片已成功保存到: {file_path}")
            return file_path
        else:
            print(f"图片下载失败，状态码: {image_response.status_code}")
            return None

    except Exception as e:
        print(f"生成图片时发生错误: {str(e)}")
        return None

# 主函数
def main():
    parser = argparse.ArgumentParser(description="微信公众号配图生成工具")
    parser.add_argument("--prompt", "-p", help="图片生成提示词")
    parser.add_argument("--style", "-s", default="", help="风格偏好（可选）")
    parser.add_argument("--size", default="2K", help="图片尺寸 (1K/2K/4K)")
    parser.add_argument("--output", "-o", default="images", help="输出目录")
    parser.add_argument("--optimize", "-O", action="store_true", help="使用AI优化提示词")

    args = parser.parse_args()

    # 如果没有提供prompt，显示帮助
    if not args.prompt and not args.optimize:
        print("=" * 60)
        print("微信公众号配图生成工具")
        print("=" * 60)
        print("\n用法示例:")
        print('  python generate_image.py -p "科技感的公众号封面图"')
        print('  python generate_image.py -p "简约商务风格插图" -s "扁平化" --size 2K')
        print('  python generate_image.py -p "未来城市" -O  # 使用AI优化提示词')
        print("\n参数说明:")
        print("  -p, --prompt    图片描述（英文或中文）")
        print("  -s, --style     风格偏好（可选）")
        print("  --size          图片尺寸: 1K, 2K, 4K (默认: 2K)")
        print("  -o, --output    输出目录 (默认: images)")
        print("  -O, --optimize  使用AI优化提示词")
        print("\n注意:")
        print("  需要在.env文件中设置ARK_API_KEY环境变量")
        print("=" * 60)
        return

    # 获取最终prompt
    final_prompt = args.prompt

    # 如果需要优化prompt
    if args.optimize or not args.prompt:
        print("=" * 60)
        print("步骤 1/3: 生成优化后的图片提示词...")
        print("=" * 60)

        user_desc = args.prompt if args.prompt else input("请描述您想要的图片内容: ")
        print(f"\n用户描述: {user_desc}")
        print(f"风格偏好: {args.style or '无'}")

        print("\n正在使用AI优化提示词...")
        final_prompt = generate_optimized_prompt(user_desc, args.style)

        print("\n" + "=" * 60)
        print("生成的图片提示词（请审核）:")
        print("=" * 60)
        print(final_prompt)
        print("=" * 60)

        # 询问用户是否继续
        user_input = input("\n是否使用此提示词生成图片? (y/n): ").strip().lower()
        if user_input not in ['y', 'yes', '是', '']:
            print("操作已取消")
            return

    # 生成图片
    print("\n" + "=" * 60)
    print("步骤 2/3: 正在生成图片...")
    print("=" * 60)
    print(f"提示词: {final_prompt[:100]}...")
    print(f"尺寸: {args.size}")

    image_path = generate_image(final_prompt, args.size, args.output)

    if image_path:
        print("\n" + "=" * 60)
        print("步骤 3/3: 图片生成成功!")
        print("=" * 60)
        print(f"图片路径: {image_path}")
        print("\n您可以在公众号文章中使用此图片。")
    else:
        print("\n图片生成失败，请检查API配置或稍后重试。")

if __name__ == "__main__":
    main()

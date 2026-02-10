import requests
import os
import time
import argparse
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从.env文件中获取API密钥
api_key = os.getenv('TOAPIS_API_KEY')

if not api_key:
    print("错误：未找到API密钥，请检查.env文件")
    exit(1)

# API请求参数
url = "https://toapis.com/v1/images/generations"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 命令行参数解析
parser = argparse.ArgumentParser(description='生成图片')
parser.add_argument('-p', '--prompt', required=True, help='图片描述prompt')
parser.add_argument('--ratio', default='16:9', help='宽高比，默认16:9')
parser.add_argument('--resolution', default='2K', help='分辨率，默认2K')
parser.add_argument('-o', '--output', default='output', help='输出目录，默认output')
parser.add_argument('--prefix', default='image', help='文件名前缀，默认image')

args = parser.parse_args()

# 支持的宽高比映射
ratio_map = {
    '2.35:1': '2.35:1',
    '16:9': '16:9',
    '4:3': '4:3',
    '1:1': '1:1',
}

ratio = ratio_map.get(args.ratio, '16:9')

payload = {
    "model": "gemini-3-pro-image-preview",
    "prompt": args.prompt,
    "size": ratio,
    "n": 1,
    "metadata": {
        "resolution": args.resolution,
        "orientation": "landscape"
    }
}

def get_image_status(task_id):
    response = requests.get(f"https://toapis.com/v1/images/generations/{task_id}", headers=headers)
    return response.json()

def wait_for_image(task_id, max_attempts=60, interval=3):
    for attempt in range(max_attempts):
        result = get_image_status(task_id)
        status = result.get('status')

        if status == 'completed':
            return result
        elif status == 'failed':
            raise Exception(f"任务失败: {result}")

        time.sleep(interval)

    raise Exception("任务超时")

try:
    # 发送API请求
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    # 处理响应
    task = response.json()
    task_id = task['id']
    print(f"任务 ID: {task_id}，状态: {task['status']}")

    # 等待任务完成
    result = wait_for_image(task_id)

    # 下载图片
    if 'result' in result and 'data' in result['result'] and len(result['result']['data']) > 0:
        image_url = result['result']['data'][0]['url']
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        # 创建输出目录
        os.makedirs(args.output, exist_ok=True)

        # 保存图片
        image_path = f"{args.output}/{args.prefix}_{task_id}.jpg"
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        print(f"图片已保存到: {image_path}")
        print(image_path)  # 输出文件路径供调用者捕获
    else:
        print("未找到图片URL，请检查返回结果")

except requests.exceptions.RequestException as e:
    print(f"API请求失败: {e}")
    exit(1)
except Exception as e:
    print(f"任务处理失败: {e}")
    exit(1)

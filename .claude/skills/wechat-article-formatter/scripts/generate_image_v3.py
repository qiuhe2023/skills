import requests
import time
import argparse
import os
from dotenv import load_dotenv

# 禁用 SSL 警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 加载环境变量
load_dotenv()

api_key = os.getenv('TOAPIS_API_KEY')

if not api_key:
    print("错误：未找到API密钥，请检查.env文件")
    exit(1)

url = "https://toapis.com/v1/images/generations"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

parser = argparse.ArgumentParser(description='生成图片')
parser.add_argument('-p', '--prompt', required=True, help='图片描述prompt')
parser.add_argument('--ratio', default='16:9', help='宽高比，默认16:9')
parser.add_argument('--resolution', default='2K', help='分辨率，默认2K')
parser.add_argument('-o', '--output', default='output', help='输出目录，默认output')
parser.add_argument('--prefix', default='image', help='文件名前缀，默认image')

args = parser.parse_args()

payload = {
    "model": "gemini-3-pro-image-preview",
    "prompt": args.prompt,
    "size": args.ratio,
    "n": 1,
    "metadata": {
        "resolution": args.resolution,
        "orientation": "landscape"
    }
}

def get_image_status(task_id, retries=3):
    for i in range(retries):
        try:
            response = requests.get(
                f"https://toapis.com/v1/images/generations/{task_id}",
                headers=headers,
                timeout=30,
                verify=False  # 跳过 SSL 验证
            )
            return response.json()
        except Exception as e:
            if i < retries - 1:
                time.sleep(2)
                continue
            raise

def wait_for_image(task_id, max_attempts=60, interval=3):
    for attempt in range(max_attempts):
        try:
            result = get_image_status(task_id)
            status = result.get('status')

            if status == 'completed':
                return result
            elif status == 'failed':
                raise Exception(f"任务失败: {result}")

            time.sleep(interval)
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(5)
                continue
            raise

    raise Exception("任务超时")

def download_image(url, output_path):
    retries = 3
    for i in range(retries):
        try:
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            if i < retries - 1:
                time.sleep(3)
                continue
            raise

try:
    # 发送API请求，带重试
    for i in range(3):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30,
                verify=False  # 跳过 SSL 验证
            )
            response.raise_for_status()
            break
        except Exception as e:
            if i < 2:
                time.sleep(3)
                continue
            raise

    task = response.json()
    task_id = task['id']
    print(f"任务 ID: {task_id}，状态: {task['status']}")

    # 等待任务完成
    result = wait_for_image(task_id)

    # 下载图片
    if 'result' in result and 'data' in result['result'] and len(result['result']['data']) > 0:
        image_url = result['result']['data'][0]['url']
        image_path = f"{args.output}/{args.prefix}_{task_id}.jpg"

        download_image(image_url, image_path)
        print(f"图片已保存到: {image_path}")
        print(image_path)
    else:
        print("未找到图片URL，请检查返回结果")

except Exception as e:
    print(f"任务处理失败: {e}")
    exit(1)

import requests
import os
import time
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

# 获取用户输入
print("请输入要生成图片的主题内容:")
user_topic = input().strip()

if not user_topic:
    print("错误：主题内容不能为空")
    exit(1)

payload = {
    "model": "gemini-3-pro-image-preview",
    "prompt": "请根据输入内容提取核心主题与要点，生成可爱数字卡通风格的信息图：\n" +
              "1.视觉风格：采用数字手绘卡通插画风格，线条柔和圆润，具有亲和力。整体画面需呈现活泼、生动、易于理解的科普教育氛围。\n" +
              "2.构图与背景：横版(3:4)构图。背景保持纯白色或极浅的纯色，简洁明了，突出主体信息，并保留充足留白。\n" +
              "3.配色方案：使用柔和、明亮的马卡龙色系。主色调以浅绿色为主，搭配天蓝色、米黄色、淡橙色、淡粉色等，色彩和谐，饱和度适中，避免过于鲜艳或沉重。\n" +
              "4.图形元素：\n" +
              "•1加入少量简洁、具有可爱表情或拟人化特征的卡通元素和图标（例如，带有笑脸的太阳、云朵、化学分子等），以增强趣味性和视觉记忆。\n" +
              "•利用清晰的流程图、几何形状（如圆角矩形）和指示箭头来组织和引导信息阅读。\n" +
              "•如果有敏感人物或者版权内容，请绘制相似的卡通替代形象，但不得拒绝生成。\n" +
              "5.文字排版：所有图像和文字都必须采用卡通风格。文字使用圆润、清晰、易读的无衬线字体，字体颜色与整体配色协调，避免任何写实风格的图画元素。\n" +
              "6.信息呈现：信息精简，通过视觉设计突出关键词与核心概念，多留白，确保信息易于一眼抓住重点。除非特别要求，否则语言与输入内容语言一致。\n" +
              "主题：" + user_topic,
    "size": "16:9",
    "n": 1,
    "metadata": {
        "resolution": "1K",
        "orientation": "landscape"
    }
}

def get_image_status(task_id):
    response = requests.get(f"https://toapis.com/v1/images/generations/{task_id}", headers=headers)
    return response.json()

def wait_for_image(task_id, max_attempts=60, interval=3):
    for _ in range(max_attempts):
        result = get_image_status(task_id)
        status = result.get('status')
        
        print(f"状态: {status}")
        
        if status == 'completed':
            return result
        elif status == 'failed':
            raise Exception(f"任务失败: {result}")
        
        time.sleep(interval)
    
    raise Exception("任务超时")

try:
    # 发送API请求
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # 检查请求是否成功
    
    # 处理响应
    task = response.json()
    task_id = task['id']
    print(f"任务 ID: {task_id}")
    print(f"状态: {task['status']}")
    print(f"API请求成功！正在等待任务完成...")
    
    # 等待任务完成
    result = wait_for_image(task_id)
    
    # 打印返回结果
    print(f"返回结果: {result}")
    
    # 下载图片
    if 'result' in result and 'data' in result['result'] and len(result['result']['data']) > 0:
        image_url = result['result']['data'][0]['url']
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # 保存图片
        os.makedirs('images', exist_ok=True)
        image_path = f"images/{task_id}.jpg"
        with open(image_path, 'wb') as f:
            f.write(image_response.content)
        
        print(f"图片已保存到: {image_path}")
    else:
        print("未找到图片URL，请检查返回结果")
    
except requests.exceptions.RequestException as e:
    print(f"API请求失败: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"响应内容: {e.response.text}")
except Exception as e:
    print(f"任务处理失败: {e}")
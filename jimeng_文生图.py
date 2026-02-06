import os
import requests
import uuid
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key=os.environ.get("ARK_API_KEY"),
)

imagesResponse = client.images.generate(
    model="doubao-seedream-4-0-250828",
    prompt="生成公众号封面的背景图，要求具有科技感和未来感，时尚简约，突出科技元素。",
    size="2K",
    response_format="url",
    extra_body={
        "watermark": False,
    },
)

# 获取生成的图片URL
image_url = imagesResponse.data[0].url
print(f"生成的图片URL: {image_url}")

# 确保images文件夹存在
os.makedirs("images", exist_ok=True)

# 下载图片到本地
image_response = requests.get(image_url)
if image_response.status_code == 200:
    # 生成唯一的文件名
    file_name = f"images/{uuid.uuid4()}.png"
    with open(file_name, "wb") as f:
        f.write(image_response.content)
    print(f"图片已成功下载到: {file_name}")
else:
    print(f"图片下载失败，状态码: {image_response.status_code}")
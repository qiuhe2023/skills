# 微信公众号文章配图 Prompt 生成指南

## 概述

本文档描述了为微信公众号文章生成配图 prompt 的规范和方法。高质量的配图 prompt 能够帮助生成与文章内容高度匹配的配图，提升文章的视觉吸引力和可读性。

## Prompt 生成原则

### 1. 封面图 Prompt

封面图是文章的第一印象，需要：
- 简洁明了地传达文章主题
- 具有专业感和设计感
- 符合目标受众的审美偏好

#### 生成方法

```python
def generate_image_prompt(title: str, summary: str, style: str = "modern tech minimalistic") -> str:
    """
    生成封面图 prompt
    参数:
        title: 文章标题
        summary: 文章摘要
        style: 设计风格（可选，默认"modern tech minimalistic"）
    """
    prompt = f"A professional wechat article cover image about '{title}'. "
    prompt += f"The article discusses: {summary[:100]}... "
    prompt += f"Style: {style}, clean, elegant, suitable for professional audience. "
    prompt += "High quality, detailed, 4K resolution."

    return prompt
```

#### Prompt 结构

1. **主题描述**：`"A professional wechat article cover image about '{title}'"`
   - 明确说明这是微信公众号封面图
   - 包含文章标题

2. **内容摘要**：`"The article discusses: {summary[:100]}..."`
   - 提供文章内容概要
   - 限制在前100个字符，避免过长

3. **风格指定**：`"Style: {style}, clean, elegant, suitable for professional audience."`
   - 指定设计风格（默认现代科技简约）
   - 强调简洁、优雅、适合专业受众

4. **质量要求**：`"High quality, detailed, 4K resolution."`
   - 要求高质量、细节丰富
   - 指定分辨率要求

### 2. 文中配图 Prompt

文中配图用于补充文章内容，需要：
- 与对应段落内容相关
- 保持整体风格统一
- 不要过于抢眼，以免分散注意力

#### 生成方法

```python
def generate_content_prompts(content: str, num_prompts: int = 3) -> List[str]:
    """
    生成文章内容配图 prompt
    参数:
        content: 文章完整内容
        num_prompts: 需要生成的 prompt 数量（默认3个）
    """
    # 提取文章中的句子
    sentences = re.split(r'[。！？\.!\?]', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    prompts = []
    for i in range(min(num_prompts, len(sentences))):
        sentence = sentences[i]
        prompt = f"An illustration for article content: '{sentence[:50]}...'. "
        prompt += "Clean, professional, vector style, suitable for wechat article."
        prompts.append(prompt)

    # 如果句子不足，用标题补充
    while len(prompts) < num_prompts:
        prompts.append(
            f"An illustration for wechat article about '{extract_title(content)}'. "
            "Clean" professional, vector style."
        )

    return prompts
```

#### Prompt 结构

1. **内容描述**：`"An illustration for article content: '{sentence[:50]}...'"`
   - 说明这是文章内容配图
   - 包含对应句子的前50个字符

2. **风格指定**：`"Clean, professional, vector style, suitable for wechat article."`
   - 强调简洁、专业
   - 使用矢量风格，保证清晰度

## 图片尺寸要求

根据不同的使用场景，使用合适的图片尺寸：

| 图片类型 | 宽 x 高 | 推荐宽高比 | 使用场景 |
|---------|---------|------------|---------|
| 封面图 | 1280 x 720 | 16:9 | 公众号文章封面，展示在分享链接和文章列表 |
| 头图/横幅 | 1280 x 544 | 2.35:1 | 文章顶部大图，营造视觉冲击 |
| 文中配图 | 1280 x 720 | 16:9 | 文章内容中的插图，横向布局 |
| 正方形配图 | 1024 x 1024 | 1:1 | 强调主体的插图 |
| 竖向配图 | 720 x 1280 | 9:16 | 人物肖像或纵向内容展示 |

### 尺寸说明

1. **封面图 (1280 x 720)**
   - 16:9 比例，高清展示
   - 在分享到朋友圈时以 16:9 比例显示
   - 避免使用 1:1 封面，分享时会被裁切
   - 文件大小建议：≤ 5MB

2. **头图/横幅 (1280 x 544)**
   - 宽幅设计，与文章宽度匹配
   - 适合做标题下方的视觉引入
   - 宽高比约 2.35:1，符合黄金分割美学

3. **文中配图 (1280 x 720)**
   - 统一使用 16:9 比例，保持版面协调
   - 宽度 1280px 填满文章内容区域
   - 高度适中，不影响阅读流畅度

4. **正方形配图 (1024 x 1024)**
   - 适合中心对称的构图
   - 用于图标、流程图、数据可视化
   - 在移动端展示效果良好

5. **竖向配图 (720 x 1280)**
   - 适合人物肖像、手机界面截图
   - 9:16 比例接近手机屏幕比例
   - 用于强调纵向内容的展示

### 脚本调用示例

```bash
# 生成封面图 (1280 x 720)
python scripts/generate_image.py -p "科技感封面" --size cover

# 生成头图/横幅 (1280 x 544)
python scripts/generate_image.py -p "横幅标题" --size banner

# 生成文中配图 (1280 x 720)
python scripts/generate_image.py -p "未来城市" --size content

# 生成正方形配图 (1024 x 1024)
python scripts/generate_image.py -p "图标" --width 1024 --height 1024

# 生成竖向配图 (720 x 1280)
python scripts/generate_image.py -p "人物肖像" --width 720 --height 1280
```

## 推荐风格

根据文章类型选择合适的配图风格：

| 文章类型 | 推荐风格 | Prompt 关键词 |
|---------|---------|--------------|
| 科技/技术类 | 现代科技简约 | "modern tech minimalistic", "tech", "clean lines" |
| 设计/创意类 | 艺术感 | "artistic", "creative", "colorful" |
| 商业/财经类 | 专业稳重 | "professional", "business", "corporate" |
| 生活/情感类 | 温馨柔和 | "warm", "soft", "lifestyle" |
| 教程/指南类 | 清晰明了 | "clear", "educational", "diagram" |
| 科普/教育类 | 可爱数字卡通 | "cute digital cartoon", "infographic", "pastel colors" |

## 系统化风格：可爱数字卡通信息图

适用于科普教育、数据可视化、流程说明等场景，通过可爱的卡通风格提升内容的亲和力和可读性。

### 风格模板

```
请根据输入内容提取核心主题与要点，生成可爱数字卡通风格的信息图：
1.视觉风格：采用数字手绘卡通插画风格，线条柔和圆润，具有亲和力。整体画面需呈现活泼、生动、易于理解的科普教育氛围。
2.构图与背景：横版(3:4)构图。背景保持纯白色或极浅的纯色，简洁明了，突出主体信息，并保留充足留白。
3.配色方案：使用柔和、明亮的马卡龙色系。主色调以浅绿色为主，搭配天蓝色、米黄色、淡橙色、淡粉色等，色彩和谐，饱和度适中，避免过于鲜艳或沉重。
4.图形元素：
•加入少量简洁、具有可爱表情或拟人化特征的卡通元素和图标（例如，带有笑脸的太阳、云朵、化学分子等），以增强趣味性和视觉记忆。
•利用清晰的流程图、几何形状（如圆角矩形）和指示箭头来组织和引导信息阅读。
•如果有敏感人物或者版权内容，请绘制相似的卡通替代形象，但不得拒绝生成。
5.文字排版：所有图像和文字都必须采用卡通风格。文字使用圆润、清晰、易读的无衬线字体，字体颜色与整体配色协调，避免任何写实风格的图画元素。
6.信息呈现：信息精简，通过视觉设计突出关键词与核心概念，多留白，确保信息易于一眼抓住重点。除非特别要求，否则语言与输入内容语言一致。
```

### 脚本调用示例

```bash
# 使用可爱数字卡通风格生成信息图
python scripts/generate_image.py -p "[输入上述风格模板]" --width 960 --height 720
```

### 适用场景

- 科普知识解释
- 数据可视化图表
- 产品功能说明
- 流程步骤图解
- 教程步骤展示

## 质量检查清单

生成 prompt 后，检查以下要素：

- [ ] 是否包含文章标题或关键内容
- [ ] 是否指定了清晰的风格
- [ ] 是否包含了质量要求
- [ ] 长度是否适中（不超过200字符）
- [ ] 是否符合目标受众的审美
- [ ] 是否与文章主题高度相关

## 示例

### 示例 1：科技文章

**文章标题：** "人工智能在医疗领域的应用"
**文章摘要：** "探讨人工智能如何辅助医生进行诊断，提高医疗效率和准确性。"

**封面图 Prompt：**
```
A professional wechat article cover image about '人工智能在医疗领域的应用'.
The article discusses: 探讨人工智能如何辅助医生进行诊断，提高医疗效率和准确性。
Style: modern tech minimalistic, clean, elegant, suitable for professional audience.
High quality, detailed, 4K resolution.
```

### 示例 2：设计文章

**文章标题：** "2024年UI设计趋势"
**文章摘要：** "分析今年最流行的用户界面设计风格和元素。"

**封面图 Prompt：**
```
A professional wechat article cover image about '2024年UI设计趋势'.
The article discusses: 分析今年最流行的用户界面设计风格和元素。
Style: modern tech minimalistic, clean, elegant, suitable for professional audience.
High quality, detailed, 4K resolution.
```

**文中配图 Prompt：**
```
An illustration for article content: '玻璃拟态效果将成为今年的主流设计趋势'.
Clean, professional, vector style, suitable for wechat article.
```

## 注意事项

1. **避免敏感词汇**：确保 prompt 不包含任何可能导致内容审核失败的关键词
2. **保持简洁**：prompt 越简洁，生成的图片越容易符合预期
3. **风格统一**：封面图和文中配图应保持风格一致
4. **测试优化**：定期测试生成的图片质量，根据结果调整 prompt 生成逻辑

## 扩展阅读

- [微信公众号排版规范](./wechat_guidelines.md)
- [风格模板选择指南](./style_templates.md)

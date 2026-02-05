---
name: wechat-article-formatter
description: "Comprehensive WeChat public account article formatting skill for creating professionally styled articles with matching image prompts. Use when Claude needs to format articles for WeChat public accounts, including: (1) Applying styling templates to article content, (2) Generating HTML files compatible with WeChat editor, (3) Creating markdown files with article metadata and image generation prompts, (4) Recommending suitable styling based on article content, (5) Processing article content to extract titles and summaries for prompt generation."
---

# 微信公众号排版技能

## 概述

本技能提供完整的微信公众号文章排版解决方案，能够将原始文章内容转换为符合微信公众号排版规范的HTML文件，并生成包含文章元数据和配图prompt的Markdown文件。

技能提供多种设计风格模板，支持风格推荐和选择，确保文章内容与视觉效果完美匹配。

## 核心工作流程

### 1. 文章内容处理
- 读取用户提供的文章内容（Markdown或纯文本）
- 提取文章标题、摘要等元数据
- 分析文章内容以推荐合适的排版风格

### 2. 风格选择与推荐
- 提供多种预设风格模板（极简时尚、扁平风格、像素风格等）
- 根据文章内容智能推荐最合适的风格
- 允许用户手动选择或调整风格

### 3. HTML生成
- 将文章内容应用到选定的风格模板
- 确保生成的HTML符合微信公众号编辑器限制
- 生成以文章标题命名的HTML文件

### 4. 元数据文件生成
- 创建Markdown文件包含：
  - 文章标题和简介
  - 封面图生成prompt（基于文章内容）
  - 文中配图生成prompts
- 文件命名与HTML文件对应

## 快速开始

### 基本使用流程
1. 提供文章内容给Claude
2. Claude使用本技能处理内容
3. 选择或接受推荐的设计风格
4. 接收生成的HTML文件和Markdown文件

### 示例用户请求
- "帮我将这篇公众号文章排版成HTML"
- "为这篇文章生成微信公众号排版，使用现代风格"
- "创建这篇文章的微信公众号版本，包含配图prompt"

## 可用资源

### 脚本工具 (`scripts/`)

#### `process_article.py`
文章内容处理脚本，提取标题、摘要，生成配图prompt。

**使用方法：**
```bash
python scripts/process_article.py <文章文件>
# 或
cat 文章.txt | python scripts/process_article.py
```

**输出：**
- 文章标题
- 文章摘要（约200字）
- 封面图生成prompt
- 3个文中配图prompts

#### `style_recommender.py`
风格推荐脚本，根据文章内容推荐合适的排版风格。

**使用方法：**
```bash
python scripts/style_recommender.py <文章文件>
```

**功能：**
- 分析文章关键词匹配风格
- 推荐前3个最合适的风格
- 显示所有可用风格及其描述

### 参考文档 (`references/`)

#### `wechat_guidelines.md`
微信公众号排版规范和限制，包含：
- 微信编辑器CSS支持情况
- 推荐字体和颜色方案
- 排版最佳实践
- 注意事项和常见问题

**何时阅读：** 当需要了解微信公众号具体排版限制时。

#### `style_templates.md`
所有可用风格模板的详细介绍，包含：
- 每个风格的特点和适用场景
- 按内容类型和受众的选择指南
- 模板文件位置信息

**何时阅读：** 当需要了解不同风格特点或选择合适风格时。

### 模板资产 (`assets/templates/`)

包含12种不同设计风格的HTML模板文件：

1. `index.html` - 极简时尚风格
2. `扁平风格.html` - 扁平化设计风格
3. `像素.html` - 像素艺术风格
4. `复古像素风格.html` - 复古像素风格
5. `弥散风格.html` - 弥散渐变风格
6. `手绘风格.html` - 手绘插画风格
7. `酸性设计.html` - 酸性设计风格
8. `玻璃拟态风格.html` - 玻璃拟态风格
9. `新粗野风格.html` - 新粗野风格
10. `黑白像素.html` - 黑白像素风格
11. `极客像素风格.html` - 极客像素风格
12. `科技简约像素.html` - 科技简约像素风格

**文件命名：** 中文文件名对应风格名称，在微信编辑器中显示正常。

## 详细工作指南

### 文章内容处理

#### 标题提取规则
1. 优先使用以#开头的Markdown标题
2. 否则使用第一行非空行作为标题
3. 如果都不可用，使用"Untitled"

#### 摘要生成规则
1. 移除标题行
2. 取文章前200个字符
3. 确保在完整的句子处截断

#### 配图prompt生成
1. 封面图prompt：基于标题和摘要生成，风格为"modern minimalistic"
2. 文中配图prompts：基于文章前几个关键句子生成，每个prompt描述具体内容

### 风格推荐逻辑

风格推荐基于关键词匹配：
- 科技/专业类文章 → 极简时尚、科技简约像素
- 设计/创意类文章 → 扁平风格、弥散风格
- 游戏/娱乐类文章 → 像素风格、复古像素风格
- 艺术/文化类文章 → 酸性设计、新粗野风格

### HTML生成注意事项

1. **保持内联样式**：所有CSS必须使用内联style属性
2. **使用安全字体**：采用微信推荐字体栈
3. **图片处理**：使用width: 100%确保响应式显示
4. **避免被过滤**：不使用position: fixed等可能被微信过滤的属性

### 文件输出规范

1. **HTML文件**：以文章标题命名，特殊字符替换为下划线
2. **Markdown文件**：同名.md文件，包含：
   ```
   # 文章标题

   ## 文章简介
   [摘要内容]

   ## 封面图prompt
   [生成的prompt]

   ## 文中配图prompts
   1. [prompt 1]
   2. [prompt 2]
   3. [prompt 3]
   ```

## 使用示例

### 示例1：基本排版
用户提供文章内容 → Claude处理 → 推荐风格 → 用户确认 → 生成HTML+MD文件

### 示例2：指定风格
用户提供文章内容并指定"扁平风格" → Claude使用指定模板 → 生成HTML+MD文件

### 示例3：批量处理
用户提供多篇文章 → Claude循环处理每篇 → 分别生成对应的文件

## 故障排除

### 常见问题

1. **生成的HTML在微信编辑器中样式异常**
   - 检查是否使用了外部CSS或class选择器
   - 确认所有样式都是内联的
   - 参考`wechat_guidelines.md`中的限制

2. **风格推荐不准确**
   - 手动选择更合适的风格
   - 调整文章关键词以匹配目标风格

3. **图片prompt质量不高**
   - 手动优化prompt描述
   - 基于文章关键内容重新生成

### 脚本错误处理

- 确保Python环境为3.6+
- 检查文件编码为UTF-8
- 确认有足够的读写权限

## 扩展与定制

### 添加新风格模板
1. 在`assets/templates/`目录中添加新的HTML文件
2. 在`references/style_templates.md`中更新描述
3. 在`scripts/style_recommender.py`中添加关键词映射

### 修改prompt生成逻辑
编辑`scripts/process_article.py`中的`generate_image_prompt`和`generate_content_prompts`函数。

### 调整样式参数
直接修改模板文件中的内联样式属性，保持微信兼容性。

---

**技能版本：** 1.0
**最后更新：** 2026-02-05
**兼容性：** 微信公众号编辑器最新规范
---
name: wechat-article-formatter
description: "Comprehensive WeChat public account article formatting skill for creating professionally styled articles with matching image prompts. Use when Claude needs to format articles for WeChat public accounts, including: (1) Applying styling templates to article content, (2) Generating HTML files compatible with WeChat editor, (3) Creating markdown files with image prompts for user review and editing, (4) Recommending suitable styling based on article content, (5) Saving prompts to numbered output folders (output/序号+标题/), allowing users to edit md files before proceeding with image generation."
---

# 微信公众号排版技能

## 概述

本技能提供完整的微信公众号文章排版解决方案，能够将原始文章内容转换为符合微信公众号排版规范的HTML文件。

核心工作流程：
1. 分析文章内容并推荐风格
2. 创建新的输出文件夹（`output/序号+标题/`）
3. 生成图片 prompts 并保存为 Markdown 文件
4. 让用户审核并允许用户直接修改 md 文件
5. 根据修改后的 prompts 生成图片
6. 将图片插入到 HTML 排版中

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

### 3. 图片 Prompt 生成与审核（新流程）
- 根据文章内容生成封面图和文中配图的 prompts
- **创建新的输出文件夹**（命名格式：`output/序号+标题/`）
- 将 prompts 保存为 Markdown 文件到该文件夹
- **让用户审核并允许用户直接修改 md 文件**
- 等待用户确认修改后的 prompts

### 4. 图片生成
- 读取用户修改后的 md 文件，获取最终 prompts
- 调用脚本生成对应的图片
- 将图片保存到同一文件夹中
- 在 md 文件中引用生成的图片

### 5. HTML生成
- 将文章内容应用到选定的风格模板
- 插入生成的图片到 HTML 排版中
- 确保生成的HTML符合微信公众号编辑器限制
- 将 HTML 文件保存到同一文件夹中

## 快速开始

### 基本使用流程
1. 提供文章内容给Claude
2. Claude分析文章内容并推荐风格
3. 用户确认风格选择
4. Claude创建新的输出文件夹（`output/序号+标题/`）
5. Claude生成图片prompts并保存为 md 文件
6. **用户审核 md 文件，可以直接修改其中的 prompts**
7. 用户确认修改后，Claude调用脚本生成图片
8. Claude创建HTML文件，将图片插入HTML

### 示例用户请求
- "帮我将这篇公众号文章排版成HTML"
- "为这篇文章生成微信公众号排版，使用现代风格"
- "创建这篇文章的微信公众号版本，包含配图和图片"

## 可用资源

### 脚本工具 (`scripts/`)

#### `generate_image.py` (可爱卡通风格)
生成可爱数字卡通风格的信息图，使用豆包大模型API。适用于科普教育、技术文章等需要亲和力视觉内容的场景。
AI图片生成脚本，调用豆包大模型生成文章配图。支持prompt优化和用户审核。

**保留理由：**
- 图片生成涉及API调用、图片下载、文件保存等复杂操作
- 大模型无法直接执行这些操作，需要脚本来处理

**使用方法：**
```bash
# 生成封面图（1024x1024，适合公众号封面）
python scripts/generate_image.py -p "科技感的公众号封面图" --size cover

# 生成文中配图（1024x1024，横向）
python scripts/generate_image.py -p "未来城市" --size content

# 生成横幅图片（1024x1024）
python scripts/generate_image.py -p "横幅标题" --size banner

# 自定义尺寸
python scripts/generate_image.py -p "自定义图片" --width 800 --height 600

# 使用AI优化prompt后再生成（生图前需要用户审核）
python scripts/generate_image.py -p "简约商务插图" -O
```

**功能：**
- 根据用户描述生成图片
- 支持三种预设尺寸：cover（封面图）、content（文中配图）、banner（横幅）
- 支持自定义宽高
- 可选择使用AI优化prompt
- 生成图片前展示prompt给用户审核
- 自动下载并保存图片到本地

**尺寸说明：**
- `cover` / `封面图`: 1024x1024，适合公众号封面
- `content` / `文中配图`: 1024x1024，横向，适合文中插图
- `banner` / `横幅`: 1024x1024，横向，适合头图/分割图
- 默认: 1024x1024

**环境变量：**
- `TOAPIS_API_KEY`: ToApis API密钥（需在`scripts/.env`文件中配置）

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

#### `image_prompts.md`
配图 Prompt 生成指南，包含：
- 封面图和文中配图的 Prompt 生成规范和方法
- Prompt 结构和组成要素说明
- 不同文章类型的推荐风格对照表
- 质量检查清单和完整示例

**何时阅读：** 当需要了解如何生成高质量的配图 Prompt 时。

### 模板资产 (`assets/templates/`)

包含13种不同设计风格的HTML模板文件：

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
12. `科技`像素.html` - 科技简约像素风格
13. `科技简约像素.html` - 科技简约像素风格

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
详细的 Prompt 生成规范请参考 `references/image_prompts.md`。

1. 封面图prompt：基于标题和摘要生成，风格为"modern tech minimalistic"
2. 文中配图prompts：基于文章`关键段落生成，每个prompt描述具体内容

**重要**：生成prompts后，必须：
1. 创建新的输出文件夹（`output/序号+标题/`）
2. 将 prompts 保存为 Markdown 文件到该文件夹
3. 告知用户 md 文件路径，让用户可以审核并直接修改
4. 等待用户确认后，读取修改后的 md 文件
5. 调用脚本生成图片

### 风格推荐逻辑

风格推荐基于关键词匹配：
- 科技/专业类文章 → 极简时尚、科技简约像素、科技简约像素
- 设计/创意类文章 → 扁平风格、弥散风格
- 游戏/娱乐类文章 → 像素风格、复古像素风格
- 艺术/文化类文章 → 酸性设计、新粗野风格

### HTML生成注意事项

1. **保持内联样式**：所有CSS必须使用内联style属性
2. **使用安全字体**：采用微信推荐字体栈
3. **图片处理**：使用width: 100%确保响应式显示
4. **避免被过滤**：不使用position: fixed等可能被微信过滤的属性
4. **避免组件风格缺失**：如果参考的模板中没有包含某个组件的样式，可以根据整体的风格样式进行完善，不要直接使用md格式。

### 文件输出规范

### 输出文件夹命名

每次创建新的输出文件夹，命名格式为：`output/序号+标题/`
- 序号从 01 开始递增
- 标题从文章标题中提取，移除特殊字符
- 示例：`output/01_AI技术趋势/`、`output/02_产品设计指南/`

### Prompt 审核文件（先生成）

首先在输出文件夹中创建以文章标题命名的 `.md` 文件，包含：
```markdown
# [文章标题]

## 文章简介
[摘要内容]

## 风格选择
[选定的风格名称]

---

## 封面图 Prompt
[封面图的 prompt]

---

## 文中配图 Prompts

### 配图 1
[配图1的 prompt]

### 配图 2
[配图2的 prompt]

... 更多配图
```

**用户审核流程：**
1. 展示生成的 md 文件路径给用户
2. 用户可以打开 md 文件直接修改 prompts
3. 用户确认后继续下一步

### 最终输出文件

用户确认后，在同一文件夹中生成：

1. **HTML文件**：以文章标题命名（`.html`）
   - 包含完整的微信公众号排版
   - 已插入生成的图片

2. **Markdown文件**：同名 `.md` 文件，更新为：
   ```markdown
   # 文章标题

   ## 文章简介
   [摘要内容]

   ## 封面图
   **Prompt:**
   [最终使用的prompt]

   **图片:**
   ![封面图](封面图文件名.jpg)

   ## 文中配图
   ... (包含每个配图的 prompt 和图片引用)
   ```

## 使用示例

### 示例1：完整排版流程
1. 用户提供文章
2. Claude分析内容并推荐风格
3. 用户确认风格选择
4. Claude创建输出文件夹 `output/01_文章标题/`
5. Claude生成图片prompts并保存为 md 文件
6. 用户审核 md 文件，可以直接修改 prompts
7. 用户确认后，Claude调用脚本生成图片
8. Claude创建HTML文件，将图片插入HTML

### 示例2：指定风格
1. 用户提供文章并指定"扁平风格"
2. Claude创建输出文件夹 `output/02_文章标题/`
3. Claude生成图片prompts并保存为 md 文件
4. 用户审核 md 文件，可以直接修改 prompts
5. 用户确认后，Claude调用脚本生成图片
6. Claude创建HTML文件，将图片插入HTML

## 故障排除

### 常见问题

1. **生成的HTML在微信编辑器中样式异常**
   - 检查是否使用了外部CSS或class选择器
   - 确认所有样式都是内联的
   - 参考`wechat_guidelines.md`中的限制

2. **风格推荐不准确**
   - 手动选择更合适的风格
   - 调整文章关键词以匹配目标风格

3. **图片生成失败**
   - 检查API配置是否正确
   - 确认`scripts/.env`中TOAPIS_API_KEY已配置

---

**技能版本：** 3.0
**最后更新：** 2026-02-09
**兼容性：** 微信公众号编辑器最新规范

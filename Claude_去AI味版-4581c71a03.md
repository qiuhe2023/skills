# Claude Code 全实操指南：程序员如何把它变成「第二个你」

> 不少人已经在用 Claude 写代码，但**真正把 Claude Code 当成开发搭子的人还不多**。
> 这篇文章不讲玄学，只讲：**怎么装、怎么配、怎么用，才能真省时间。**

---

## 一、Claude Code 核心介绍

### 核心定位

Claude Code 是 Anthropic 推出的命令行级 AI 编程助手，不是聊天工具，而是嵌入你开发流程里的“协作开发者”。

它的目标不是替你写 Demo，而是参与真实工程：

* 理解代码结构
* 操作文件
* 调用工具
* 执行复杂任务链

### 核心优势

* **原生 CLI 体验**：贴合程序员习惯
* **上下文感知强**：能读整个项目
* **支持 MCP / Agent / Skill**：高度可扩展
* **适合长期工程协作**，不是一次性问答

### 一句话总结

> Claude Code = 能进你项目目录、懂你代码上下文、可持续协作的 AI 程序员。

---

## 二、核心使用场景（程序员高频）

### 1️⃣ 单兵开发场景

适合独立开发者或个人项目：

* 快速理解陌生代码库
* 新功能原型生成
* 自动补测试用例
* TODO 扫描 & 技术债整理

👉 本质：**减少上下文切换，减少“查 + 想 + 写”时间**

---

### 2️⃣ 团队协作场景

适合中小团队 / 初创团队：

* 统一代码规范检查
* PR 初审（结构 / 风格 / 风险）
* 新成员快速上手项目
* 文档自动补齐

👉 Claude Code 可以当**“团队最有耐心的 reviewer”**

---

### 3️⃣ 专项任务场景

非常适合这些事：

* 代码审查（Code Review）
* 老代码重构
* 复杂逻辑解释
* Bug 根因分析
* 技术方案对比

👉 特点：**一次配置，多次复用**

---

## 三、快速安装

### 前置准备

* macOS / Linux（Windows 建议 WSL）
* Node.js ≥ 18
* 已有 Anthropic API Key

---

### 核心安装命令

```bash
npm install -g @anthropic-ai/claude-code
```

---

### 验证安装

```bash
claude --version
```

能看到版本号，说明安装成功。

---

### 补充说明

* Claude Code 是 CLI 工具，不是 VS Code 插件
* 建议在**真实项目根目录**中使用
* API Key 建议通过环境变量配置

---

## 四、添加模型

### 支持类型

* Claude 3 Opus
* Claude 3.5 Sonnet（推荐）
* Claude 3 Haiku（轻量）

---

### 核心方法

在配置文件中指定默认模型：

```bash
claude config set model claude-3-5-sonnet
```

---

### 快捷切换

```bash
claude --model claude-3-opus
```

适合高难度重构 / 设计任务。

---

### 注意事项

* 不同模型**成本差异很大**
* 长上下文任务优先 Sonnet / Opus
* 日常辅助 Haiku 就够

---

## 五、切换外部模型（Volcengine Ark Coding Plan）

### 核心定位

通过 Volcengine 方舟 Coding Plan 套餐，Claude Code 可以接入更多外部大模型，包括 doubao-seed-code、glm-4.7、deepseek-v3.2 等，扩展编程能力边界。

### 前置准备

1. 订阅方舟 Coding Plan 套餐
2. 获取 Volcengine Ark API Key

### 核心配置

#### 模型配置

配置时 Model Name 需使用小写格式，支持以下值：
- doubao-seed-code
- glm-4.7
- deepseek-v3.2
- kimi-k2-thinking
- kimi-k2.5

#### Base URL

根据兼容协议选择对应 Base URL：
- 兼容 Anthropic 接口：`https://ark.cn-beijing.volces.com/api/coding`
- 兼容 OpenAI 接口：`https://ark.cn-beijing.volces.com/api/coding/v3`

⚠️ 注意：请勿使用 `https://ark.cn-beijing.volces.com/api/v3`，该地址不会消耗 Coding Plan 额度，会产生额外费用。

#### 环境变量配置

##### macOS & Linux（zsh/bash）

在 Shell 配置文件末尾追加以下内容：
```bash
export ANTHROPIC_BASE_URL="https://ark.cn-beijing.volces.com/api/coding"
export ANTHROPIC_AUTH_TOKEN="<你的 Ark API Key>"
export ANTHROPIC_MODEL="<Model Name>"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1"
export ANTHROPIC_API_KEY="" # 避免与本地 Anthropic 配置冲突
```

使配置生效：
```bash
source ~/.zshrc # zsh 用户
source ~/.bashrc # bash 用户
```

##### Windows

**CMD**：
```cmd
setx ANTHROPIC_AUTH_TOKEN <你的 Ark API Key>
setx ANTHROPIC_BASE_URL https://ark.cn-beijing.volces.com/api/coding
setx ANTHROPIC_MODEL <Model Name>
```

**PowerShell**：
```powershell
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_AUTH_TOKEN', '<你的 Ark API Key>', 'User')
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_BASE_URL', 'https://ark.cn-beijing.volces.com/api/coding', 'User')
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_MODEL', '<Model Name>', 'User')
```

### 切换模型

#### 方式一：控制台切换

通过 Volcengine 方舟开通管理页面选择目标模型，切换后 3-5 分钟生效，适合使用 `ark-code-latest` 自动模式。

#### 方式二：CLI 切换

启动时指定模型：
```bash
claude --model <Model Name>
```

对话期间切换模型：
```bash
/model <Model Name>
```

### 验证配置

执行以下命令确认模型状态：
```bash
claude --status
```

---

## 六、增加 MCP

### MCP 定位

MCP（Model Context Protocol）是 Claude Code 的**“外接能力接口”**。

一句话理解：

> **让 Claude 不只“想”，还能“查”和“连”。**

---

### 常用连接方式

* 本地文件系统
* Git 仓库
* 数据库
* 内部 API
* 第三方工具

---

### 关键提示

* MCP 决定 Claude 能“看到什么”
* 适合接：文档库 / 配置中心 / 私有 API
* 建议最小权限原则

---

### 验证配置

```bash
claude mcp list
```

能看到已连接的 MCP 即成功。

---

## 七、创建 Agent

### Agent 定位

Agent = **长期存在的“角色型 AI”**，不是一次性指令。

例如：

* 代码审查 Agent
* 架构设计 Agent
* 测试生成 Agent

---

### 创建方式

```bash
claude agent create code-reviewer
```

---

### 核心配置

* 角色职责
* 输入范围
* 输出格式
* 使用模型

---

### 实用技巧

* 一个 Agent 只做一件事
* 给 Agent 明确边界
* 固化风格 & 输出模板

---

## 八、创建 Skill

### Skill 定位

Skill = **可复用的小能力**，更轻量。

Agent 偏“人”，Skill 偏“工具”。

---

### 新手入门

从简单 Skill 开始，例如：

* 生成 commit message
* 补单元测试
* 代码注释生成

---

### 自定义创建（进阶）

```bash
claude skill create gen-tests
```

可绑定：

* 固定 Prompt
* 特定输入格式
* 自动触发条件

---

### 触发方式

* CLI 显式调用
* Agent 内部调用
* 特定文件变更触发

---

## 九、常用快捷指令（高频）

### 基础操作

```bash
claude
claude chat
claude help
```

---

### 模型 / Agent / MCP 管理

```bash
claude model list
claude agent list
claude mcp list
```

---

### 代码相关（最常用）

```bash
claude review .
claude explain src/main.ts
claude refactor services/
```

---

## 十、常见问题排查

### 安装失败

* Node 版本过低
* npm 权限问题
* 网络问题（可换镜像）

---

### 模型 / API 异常

* API Key 是否正确
* 是否超配额
* 模型名是否拼写错误

---

### Agent / Skill 不生效

* 是否在项目根目录
* 是否加载对应配置
* 是否被模型限制

---

## 十一、资源推荐（建议收藏，后续深入必看）

### 📘 官方文档（第一优先级）

**Claude Code 官方文档**
👉 [https://docs.anthropic.com/claude/docs/claude-code](https://docs.anthropic.com/claude/docs/claude-code)

> 安装、配置、CLI 命令、Agent / Skill 的权威说明，版本更新也最及时。

**Anthropic API 官方文档**
👉 [https://docs.anthropic.com/claude/reference](https://docs.anthropic.com/claude/reference)

> 模型说明、参数配置、Token 计费规则，理解模型行为必看。

**MCP（Model Context Protocol）官方说明**
👉 [https://docs.anthropic.com/claude/docs/model-context-protocol](https://docs.anthropic.com/claude/docs/model-context-protocol)

> 了解 Claude 如何“接入外部世界”，做工程级 AI 集成一定要读。

---

### 🧩 常用 Skill / Agent 资源

**Claude Code GitHub 官方组织**
👉 [https://github.com/anthropics](https://github.com/anthropics)

> 官方示例、协议规范、工具代码，适合抄作业和理解设计思路。

**社区维护的 Claude Code 示例仓库（搜索入口）**
👉 [https://github.com/search?q=claude+code+agent&type=repositories](https://github.com/search?q=claude+code+agent&type=repositories)

> 能找到不少实战型 Agent / Skill，例如代码审查、测试生成、文档整理。

**Prompt / Agent 思路参考（通用）**
👉 [https://github.com/f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)

> 虽然不是专门为 Claude Code，但很多 Prompt 思路可以直接迁移成 Skill。

---

### 💬 社区与交流渠道

**Anthropic 官方 Discord**
👉 [https://discord.gg/anthropic](https://discord.gg/anthropic)

> Claude 新功能、Claude Code 使用经验，第一时间都在这里讨论。

**X（Twitter）Claude Code 讨论标签**
👉 [https://x.com/search?q=Claude%20Code&src=typed_query](https://x.com/search?q=Claude%20Code&src=typed_query)

> 很多一线开发者会分享真实使用场景和踩坑经验。

**GitHub Issues（问题排查首选）**
👉 [https://github.com/anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues)

> 安装失败、环境问题、Bug，大概率已经有人遇到过。

---

### 🔖 延伸学习建议（个人经验）

* **先看官方文档，再抄社区配置**
* **优先写 Skill，再抽象成 Agent**
* **MCP 只接“你真的需要”的系统**
* 把 Claude Code 当成：

  > *“一个需要你认真配置的开发工具，而不是一次性 AI 玩具”*

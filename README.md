# 吃什么 - 智能吃饭助手

基于 Agno 框架开发的智能体，为用户提供吃饭建议、管理餐厅选择和记录就餐历史。

## 功能特性

- 🕐 **智能时间判断**：根据当前时间自动判断早/午/晚饭时间
- 📋 **餐厅管理**：添加、查看、更新、删除餐厅和餐品选择
- 📊 **统计分析**：查看最近一段时间吃饭情况的统计信息
- 🎯 **智能推荐**：基于多种信息综合推荐，包括用户偏好、历史记录等
- 💾 **历史记录**：记录每次就餐行为，便于追踪和分析
- 🧠 **记忆功能**：记住用户的偏好和历史对话
- 🗂️ **全局信息**：灵活存储和检索用户的偏好、习惯等信息（完全由模型决定）

## 技术栈

- **框架**: Agno 2.4.3
- **数据库**: SQLAlchemy 2.0.46 + SQLite
- **模型**: OpenAI Compatible (通过 OpenAILike 接口)
- **终端交互**: prompt_toolkit (支持 Unicode 和多字节字符)
- **Python**: >= 3.13

## 安装

1. 克隆仓库并进入项目目录

```bash
cd ew-agent
```

2. 激活虚拟环境

```bash
source .venv/bin/activate
```

3. 依赖已通过 pyproject.toml 配置，使用 uv 安装

```bash
uv pip install -U agno sqlalchemy
```

## 配置

在项目根目录创建 `.env` 文件，配置模型信息：

```env
OPENAI_BASE_URL="http://127.0.0.1:8317/v1"
OPENAI_API_KEY="your_api_key"
MODEL_NAME="qwen3-max"
```

## 使用

运行智能体：

```bash
python main.py
```

### 使用示例

```
🤔 你想吃什么？> 现在几点了？
💬 EatWhat 正在思考...
当前时间: 2026-01-26 12:30:00, 餐次: 午饭

🤔 你想吃什么？> 帮我添加一个餐厅，叫"老王面馆"，卖牛肉面，标签是"面食"
💬 EatWhat 正在思考...
成功添加餐厅选择！ID: 1, 餐厅: 老王面馆, 餐品: 牛肉面

🤔 你想吃什么？> 看看有哪些餐厅
💬 EatWhat 正在思考...
已记录的餐厅选择：
ID: 1 | 餐厅: 老王面馆 | 餐品: 牛肉面 | 标签: 面食

🤔 你想吃什么？> 推荐一下午饭吃什么
💬 EatWhat 正在思考...
为您推荐的午饭选择：
1. 老王面馆 - 牛肉面 (标签: 面食)

🤔 你想吃什么？> 记录一下，我午饭吃了老王面馆
💬 EatWhat 正在思考...
成功记录！午饭吃了 老王面馆 的 牛肉面

🤔 你想吃什么？> 看看最近7天的统计
💬 EatWhat 正在思考...
最近 7 天吃饭统计：
总就餐次数: 1

餐次分布：
  午饭: 1 次

热门餐厅（TOP 5）：
  1. 老王面馆: 1 次

🤔 你想吃什么？> 我喜欢吃辣的，记一下
💬 EatWhat 正在思考...
成功创建全局信息！键名: user_taste_preference

🤔 你想吃什么？> ew
💬 EatWhat 正在思考...
根据您的口味偏好（辣），推荐您试试...

## 项目结构

```
ew-agent/
├── models.py          # SQLAlchemy 数据模型
├── tools.py           # 自定义工具函数
├── agent.py           # Agent 配置
├── main.py            # CLI 入口文件
├── .env               # 模型配置
├── pyproject.toml     # 项目依赖
└── README.md          # 文档
```

## 可用工具

| 工具名称 | 功能 |
|---------|------|
| `get_current_time` | 获取当前时间和餐次类型 |
| `list_food_choices` | 列出所有餐厅选择 |
| `add_food_choice` | 添加新的餐厅选择 |
| `update_food_choice` | 更新餐厅信息 |
| `delete_food_choice` | 删除餐厅选择 |
| `get_eating_statistics` | 获取就餐统计信息 |
| `record_eating` | 记录就餐行为 |
| `get_global_info` | 获取全局信息 |
| `set_global_info` | 设置或更新全局信息 |
| `list_global_info` | 列出所有全局信息 |
| `delete_global_info` | 删除全局信息 |

## 数据库

项目使用 SQLite 数据库进行数据持久化，数据库文件 `data/eat_what.db` 会在首次运行时自动创建。

### 数据表

- **food_choices**: 存储餐厅和餐品信息
- **eating_history**: 存储就餐历史记录
- **global_info**: 存储全局信息（键值对形式，完全由模型决定存储内容）

## License

MIT
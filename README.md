# 研心合一 (KaoYan MindCoach)

## 项目概述

“研心合一”（KaoYan MindCoach）是一个基于 Web 的 AI 驱动大学生心理健康助手，专为准备研究生入学考试（考研）的学生设计。该平台专注于 AI 情感计算技术，构建“感知-评估-干预-复盘”闭环，用于情绪监测、压力识别和个性化调节，并与学习场景整合。它旨在帮助考研学生（尤其是二战/三战学生）预测压力、生成“学习处方”、提供快速干预和每周复盘，将情感洞察与学习执行有效连接。

**核心特点：**
- **AI 情感计算**：通过用户自报输入进行情绪监测和压力识别。
- **个性化干预**：提供“学习处方”、情绪急救和心流训练。
- **隐私保护**：所有数据均经用户同意并安全存储，不依赖外部硬件设备。
- **响应式设计**：适合在大学环境中部署，支持桌面和移动端访问。

## 功能模块

平台功能围绕“感知-评估-干预-复盘”闭环设计，主要包括以下模块：

1.  **沉浸式入场界面**：欢迎动画、快速心情打卡、个性化 AI 问候和首次用户引导。
2.  **核心导航**：首页（今日任务、心流按钮、心情打卡）、压力雷达、心流训练、情绪急救、心灵画语、心语信使、错题复盘表、我的周报。
3.  **考研压力雷达**：
    *   **感知层**：倒计时日历、模考安排、计划完成度、自报睡眠时长。
    *   **评估层**：计算焦虑指数（AI_t），识别高风险状态。
    *   **干预层**：自动任务切片、模考心理报告、压力应对卡片。
4.  **专注心流模式**：
    *   **感知**：番茄钟日志、应用白名单、错题复盘进度、会话时长。
    *   **评估**：真产出率（TPR）计算，识别假性学习和拖延。
    *   **干预**：极简承诺、两分钟闸门、Streak 护盾、考前稳心策略。
5.  **情绪急救码**：针对模考失利、背诵崩溃、自习室分心等场景提供 90-120 秒微干预。
6.  **情绪成长图谱**：可视化情绪趋势、学习效率与情绪散点图，提供弱因果提示和个性化策略建议。
7.  **AI 研友陪练教练**：导师型/研友型/暖心型 AI 伴侣，通过 EARS 脚手架进行结构化对话，提供“技术 + 情绪”双处方。
8.  **心灵画语**：用户绘画画布，AI 分析绘画（色彩、笔触、构图），生成心灵镜像或正念绘画脚本。
9.  **心语信使**：多模态（文本、语音、图片）对话，AI 识别情绪和认知扭曲，提供虚拟人视频回信和资源锦囊。

## 技术栈

-   **前端**：Vue.js 3 (Composition API), Vue Router, Pinia (状态管理), Chart.js (数据可视化), Tailwind CSS (样式).
-   **后端**：FastAPI (Python), Pydantic (数据验证), Motor (MongoDB 异步驱动), PyJWT (JWT 认证), Passlib (密码哈希), OpenAI Python Client (AI 集成).
-   **数据库**：MongoDB.
-   **认证**：JWT (JSON Web Tokens) 进行用户注册/登录。

## 项目结构

```
kaoyan-mindcoach/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/       # 可复用组件
│   │   ├── router/           # Vue Router 配置
│   │   ├── store/            # Pinia 状态管理模块
│   │   ├── views/            # 页面组件
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vue.config.js
├── backend/
│   ├── app/
│   │   ├── api/              # 外部 API 接口定义 (例如 OpenAI)
│   │   ├── core/             # 核心配置 (例如 settings.py)
│   │   ├── db/               # 数据库连接和操作
│   │   ├── models/           # MongoDB 数据模型 (Pydantic)
│   │   ├── routers/          # FastAPI 路由定义
│   │   ├── schemas/          # Pydantic 数据验证模型
│   │   ├── services/         # 业务逻辑和 AI 服务
│   │   └── main.py           # FastAPI 主应用
│   ├── .env.example          # 环境变量示例
│   └── requirements.txt      # Python 依赖
└── README.md
```

## 环境搭建与运行

请确保您的系统已安装以下软件：
-   Node.js (推荐 LTS 版本)
-   npm 或 Yarn
-   Python 3.9+
-   pip
-   MongoDB 数据库 (本地安装或云服务)

### 1. 克隆仓库

```bash
git clone <repository_url>
cd kaoyan-mindcoach
```

### 2. 后端设置

进入 `backend` 目录：

```bash
cd backend
```

**创建并配置环境变量：**

复制 `.env.example` 文件为 `.env`，并填写您的配置信息：

```bash
cp .env.example .env
```

`.env` 文件内容示例：

```
MONGO_CONNECTION_STRING="mongodb://localhost:27017"
MONGO_DB_NAME="kaoyan_mindcoach"
SECRET_KEY="your_super_secret_key_for_jwt"
OPENAI_API_KEY="your_openai_api_key_here"
```

-   `MONGO_CONNECTION_STRING`: 您的 MongoDB 连接字符串。例如：`mongodb://localhost:27017` 或 `mongodb+srv://user:pass@cluster.mongodb.net/`。
-   `MONGO_DB_NAME`: 数据库名称，例如 `kaoyan_mindcoach`。
-   `SECRET_KEY`: 用于 JWT 签名的密钥，**请务必替换为强随机字符串**，例如使用 `openssl rand -hex 32` 生成。
-   `OPENAI_API_KEY`: 您的 OpenAI API 密钥，用于 AI 情感分析和对话功能。如果未提供，AI 功能将使用模拟数据。

**安装 Python 依赖：**

```bash
pip install -r requirements.txt
```

`requirements.txt` 示例内容：

```
fastapi==0.104.1
uvicorn==0.23.2
motor==3.3.1
pydantic==2.4.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
dotenv==1.0.0
openai==1.3.5
```

**运行后端服务：**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 `http://localhost:8000` 运行。

### 3. 前端设置

进入 `frontend` 目录：

```bash
cd ../frontend
```

**安装 Node.js 依赖：**

```bash
npm install
# 或者 yarn install
```

**配置 API 基础 URL：**

在 `frontend` 目录下创建 `.env.local` 文件（如果不存在），并添加以下内容：

```
VUE_APP_API_BASE_URL=http://localhost:8000/api/v1
```

这将确保前端应用能够正确地与后端 API 进行通信。

**运行前端开发服务器：**

```bash
npm run serve
# 或者 yarn serve
```

前端应用将在 `http://localhost:8080` (默认) 运行。

### 4. 访问应用

在浏览器中打开 `http://localhost:8080` 即可访问“研心合一”平台。

## 单元测试 (待实现)

-   **前端**：可以使用 Vitest 或 Jest 进行单元测试。
-   **后端**：可以使用 Pytest 进行单元测试，特别是针对焦虑计算等核心逻辑。

## 贡献

欢迎通过 Pull Request 贡献代码或提交 Issue 报告问题。

## 许可证

本项目采用 MIT 许可证。


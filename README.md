# 架构图生成器 (Architecture Diagram Generator)

一个基于AI的架构图生成工具，可以将文字描述转换为可视化的系统架构图。

## 功能特性

- 通过自然语言描述生成系统架构图
- 支持多种架构图样式和布局
- 实时预览生成的架构图
- 支持导出为PNG、SVG等图片格式
- 支持自定义主题和样式

## 技术栈

- 前端：React + TypeScript
- 后端：Python + FastAPI
- AI：OpenAI API
- 图表生成：Mermaid.js
- 样式：Tailwind CSS

## 快速开始

1. 克隆仓库
```bash
git clone https://github.com/yourusername/architecture-diagram-generator.git
cd architecture-diagram-generator
```

2. 安装依赖
```bash
# 安装前端依赖
cd frontend
npm install

# 安装后端依赖
cd ../backend
pip install -r requirements.txt
```

3. 配置环境变量
```bash
# 在backend目录下创建.env文件
cp .env.example .env
# 编辑.env文件，添加必要的配置信息
```

4. 启动服务
```bash
# 启动后端服务
cd backend
uvicorn main:app --reload

# 启动前端服务
cd frontend
npm run dev
```

5. 访问应用
打开浏览器访问 http://localhost:5173

## 使用示例

1. 在文本框中输入系统架构描述，例如：
```
系统包含一个前端应用，使用React开发，通过REST API与后端服务通信。
后端服务使用Python FastAPI框架，连接PostgreSQL数据库。
系统使用Redis作为缓存层，使用Nginx作为反向代理。
```

2. 点击"生成架构图"按钮
3. 预览生成的架构图
4. 可以调整样式和布局
5. 点击"导出"按钮下载图片

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目。

## 许可证

MIT License

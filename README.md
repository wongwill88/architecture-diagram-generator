# 架构图生成器 (Architecture Diagram Generator)

一个基于AI的架构图生成工具，可以将文字描述转换为可视化的系统架构图。采用科幻风格的UI设计，支持一键导出PNG格式图片。

## 功能特性

- 通过自然语言描述生成美观的系统架构图
- 科幻风格的UI界面，具有动态背景和视觉效果
- 支持中英文双语架构描述输入
- 实时预览生成的架构图
- 一键导出为PNG格式图片
- 提供简单和复杂示例模板

## 技术栈

- 前端：Vue.js 3 + Element Plus
- 后端：Python + FastAPI
- AI：DeepSeek API
- 样式：原生CSS + 自定义动画效果
- 图片导出：html2canvas

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
# 编辑.env文件，添加DEEPSEEK_API_KEY
```

4. 启动服务
```bash
# 启动后端服务
cd backend
uvicorn main:app --reload --port 8001

# 启动前端服务
cd frontend
npm run dev
```

5. 访问应用
打开浏览器访问 http://localhost:5173

## 使用示例

1. 在文本框中输入系统架构描述，例如：
```
系统包含一个前端应用，使用Vue.js开发，通过REST API与后端服务通信。
后端服务使用Python FastAPI框架，连接PostgreSQL数据库。
系统使用Redis作为缓存层，使用Nginx作为反向代理。
```

2. 点击"生成架构图"按钮
3. 等待AI生成架构图（会显示动态加载动画）
4. 查看生成的架构图预览
5. 点击"导出为图片"按钮下载PNG格式图片

## 未来开发计划

- [ ] 支持多种图表风格和主题切换
- [ ] 增加更多导出格式（SVG、PDF等）
- [ ] 添加图表编辑功能，允许用户在生成后调整图表
- [ ] 支持用户账户系统，保存历史生成的图表
- [ ] 提供更多架构图示例和模板
- [ ] 实现移动端响应式设计，支持移动设备使用
- [ ] 增加团队协作功能，允许多人共同编辑
- [ ] 支持对图表添加注释和标注
- [ ] 实现3D架构图表示

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目。

## 许可证

MIT License

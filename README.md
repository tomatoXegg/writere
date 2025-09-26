# 公众号内容助手

一个基于Streamlit构建的智能公众号文章处理工具，支持内容提取、图片转存、AI改写等功能。

## ✨ 功能特点

- 🔗 **一键获取**: 通过URL自动获取公众号文章内容
- 🖼️ **图片转存**: 自动将文章中的图片上传到Cloudinary，确保链接永久有效
- 🤖 **AI改写**: 使用Google Gemini API智能改写文章内容
- 📋 **源码复制**: 支持一键复制Markdown源码
- 📚 **历史记录**: 在当前会话中保存处理历史
- 🎨 **友好界面**: 简洁直观的用户界面

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd 公众号助手
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

#### 本地开发
1. 复制配置文件：
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. 编辑 `.streamlit/secrets.toml` 文件，填入您的API密钥：
```toml
FIRECRAWL_API_KEY = "your_firecrawl_api_key"
CLOUDINARY_CLOUD_NAME = "your_cloud_name"
CLOUDINARY_API_KEY = "your_api_key"
CLOUDINARY_API_SECRET = "your_api_secret"
GEMINI_API_KEY = "your_gemini_api_key"
```

#### 部署到Streamlit Cloud
在Streamlit Community Cloud的Settings > Secrets中添加上述配置项。

### 4. 运行应用
```bash
streamlit run app.py
```

## 🔧 API密钥获取

### Firecrawl
- 访问 [Firecrawl官网](https://www.firecrawl.dev/)
- 注册账号并获取API Key

### Cloudinary
- 访问 [Cloudinary官网](https://cloudinary.com/)
- 注册免费账号
- 在Dashboard中获取Cloud Name、API Key和API Secret

### Gemini API
- 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
- 登录Google账号并创建API Key

## 📖 使用方法

1. **输入URL**: 在文本框中粘贴公众号文章链接
2. **点击处理**: 点击"开始处理"按钮
3. **等待完成**: 系统会自动执行内容提取、图片处理、AI改写
4. **查看结果**: 处理完成后可预览改写内容和复制源码
5. **查看历史**: 在历史记录中查看本次会话处理过的所有文章

## 🏗️ 技术架构

- **前端框架**: Streamlit
- **编程语言**: Python 3.8+
- **核心依赖**: requests, google-generativeai, cloudinary
- **部署平台**: Streamlit Community Cloud

## 📝 开发说明

本项目遵循以下设计原则：
- **KISS原则**: 保持代码简洁，避免过度设计
- **单一职责**: 每个函数只负责一个特定功能
- **错误处理**: 完善的异常处理机制
- **用户体验**: 清晰的进度提示和错误反馈

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 优秀的数据应用框架
- [Firecrawl](https://www.firecrawl.dev/) - 强大的网页内容提取服务
- [Cloudinary](https://cloudinary.com/) - 专业的云图片服务
- [Google Gemini](https://ai.google.dev/) - 先进的AI模型
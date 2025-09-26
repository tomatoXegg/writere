# 公众号内容助手配置说明

## 环境配置

### 本地开发环境
1. 创建 `.streamlit` 目录
2. 创建 `secrets.toml` 文件，内容如下：

```toml
# Firecrawl API配置
FIRECRAWL_API_KEY = "your_firecrawl_api_key_here"

# Cloudinary配置
CLOUDINARY_CLOUD_NAME = "your_cloud_name"
CLOUDINARY_API_KEY = "your_api_key"
CLOUDINARY_API_SECRET = "your_api_secret"

# Gemini API配置
GEMINI_API_KEY = "your_gemini_api_key"
```

### Streamlit Cloud部署
在Streamlit Community Cloud的Settings > Secrets中添加上述配置项。

## API密钥获取

### 1. Firecrawl API Key
- 访问 https://www.firecrawl.dev/
- 注册账号并获取API Key

### 2. Cloudinary配置
- 访问 https://cloudinary.com/
- 注册免费账号
- 在Dashboard中找到：
  - Cloud Name
  - API Key
  - API Secret

### 3. Gemini API Key
- 访问 https://makersuite.google.com/app/apikey
- 登录Google账号并创建API Key

## 使用说明

1. 安装依赖：`pip install -r requirements.txt`
2. 配置API密钥（本地开发需要创建.secrets.toml文件）
3. 运行应用：`streamlit run app.py`
4. 在浏览器中打开显示的URL

## 功能特点

- 🔗 一键获取公众号文章内容
- 🖼️ 自动转存图片到永久链接
- 🤖 AI智能改写内容
- 📋 支持Markdown源码复制
- 📚 会话内历史记录
- 🎨 简洁友好的用户界面
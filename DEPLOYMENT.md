# 公众号助手 - Streamlit Cloud部署指南

## 🚀 部署步骤

### 1. 准备GitHub仓库
- 将此项目推送到GitHub仓库
- 确保包含以下文件：
  - `app.py` - 主应用文件
  - `requirements.txt` - Python依赖
  - `.streamlit/config.toml` - Streamlit配置

### 2. 配置Streamlit Cloud
1. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
2. 点击"New app"
3. 选择GitHub仓库
4. 选择分支（通常是main或master）
5. 主文件路径：`app.py`

### 3. 配置环境变量
在Streamlit Cloud设置中添加以下secrets：

```toml
# Firecrawl API配置
FIRECRAWL_API_KEY = "您的Firecrawl API密钥"

# Cloudinary配置
CLOUDINARY_CLOUD_NAME = "您的Cloudinary云名称"
CLOUDINARY_API_KEY = "您的Cloudinary API密钥"
CLOUDINARY_API_SECRET = "您的Cloudinary API密钥"

# Gemini API配置
GEMINI_API_KEY = "您的Gemini API密钥"
```

### 4. 部署验证
- 点击部署按钮
- 等待构建完成
- 测试应用功能

## 🔧 故障排除

### 常见问题
1. **依赖安装失败**：检查`requirements.txt`中的版本兼容性
2. **API连接超时**：Cloud环境网络访问可能有限制
3. **文件上传失败**：检查Cloudinary配置

### 日志查看
- 在Streamlit Cloud管理面板查看应用日志
- 使用`st.write()`或`print()`调试代码

## 📋 项目结构
```
公众号助手/
├── app.py                    # 主应用文件
├── requirements.txt          # Python依赖
├── .streamlit/
│   ├── config.toml          # Streamlit配置
│   └── secrets.toml         # 本地开发密钥
├── README.md                # 项目说明
└── 其他文件...
```

## 💡 提示
- Streamlit Cloud提供免费额度
- 支持自动部署GitHub更新
- 可配置自定义域名
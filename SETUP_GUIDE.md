# 🚀 快速配置指南

## 当前状态
✅ **项目结构完成** - 所有代码文件已创建
✅ **核心逻辑验证** - 正则表达式和业务逻辑测试通过
⚠️ **需要配置API密钥** - 这是运行应用的关键步骤

## 📋 API密钥配置步骤

### 1. 获取API密钥

#### 🔥 Firecrawl API Key
- **官网**: https://www.firecrawl.dev/
- **步骤**:
  1. 注册账号
  2. 获取API Key（通常在Dashboard或API页面）
  3. 免费额度通常足够测试使用

#### ☁️ Cloudinary 配置
- **官网**: https://cloudinary.com/
- **步骤**:
  1. 注册免费账号
  2. 在Dashboard找到:
     - Cloud Name
     - API Key  
     - API Secret
  3. 免费套餐提供一定额度

#### 🤖 Gemini API Key
- **官网**: https://makersuite.google.com/app/apikey
- **步骤**:
  1. 登录Google账号
  2. 创建新的API Key
  3. 免费使用（有一定限制）

### 2. 配置文件设置

编辑 `.streamlit/secrets.toml` 文件：

```toml
# Firecrawl API配置
FIRECRAWL_API_KEY = "fc-xxxxxxxxxxxxxxxxxxxx"

# Cloudinary配置
CLOUDINARY_CLOUD_NAME = "your_cloud_name"
CLOUDINARY_API_KEY = "xxxxxxxxxxxxxx"
CLOUDINARY_API_SECRET = "xxxxxxxxxxxxxx"

# Gemini API配置
GEMINI_API_KEY = "AIzaSyxxxxxxxxxxxxxxxxxxxx"
```

### 3. 安装依赖

```bash
cd 公众号助手

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 4. 运行测试

```bash
# 运行系统测试
python3 test_system.py

# 运行核心逻辑测试
python3 test_logic.py
```

### 5. 启动应用

```bash
streamlit run app.py
```

## 🔧 故障排除

### 常见问题

1. **ModuleNotFoundError: No module named 'cloudinary'**
   ```bash
   pip install cloudinary
   ```

2. **API密钥错误**
   - 检查 `.streamlit/secrets.toml` 文件
   - 确保所有密钥都已正确填写
   - 重新启动Streamlit应用

3. **网络连接问题**
   - 确保网络可以访问相关API服务
   - 检查防火墙设置

4. **Streamlit启动失败**
   ```bash
   pip install --upgrade streamlit
   ```

## 📞 获取帮助

如果遇到问题：
1. 检查 [CONFIG.md](CONFIG.md) 文件
2. 查看 [README.md](README.md) 文件
3. 运行测试脚本诊断问题

## 🎯 下一步

配置完成后，您就可以：
- 输入公众号文章链接
- 自动获取和改写内容
- 转存图片到永久链接
- 复制处理后的Markdown内容

---

**祝您使用愉快！** 🎉
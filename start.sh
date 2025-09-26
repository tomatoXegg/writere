#!/bin/bash

# 公众号内容助手启动脚本

echo "🚀 正在启动公众号内容助手..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 检查配置文件
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️ 警告: .streamlit/secrets.toml 不存在"
    echo "请复制 .streamlit/secrets.toml.example 为 .streamlit/secrets.toml 并填入API密钥"
    echo ""
fi

# 启动应用
echo "🎉 启动应用..."
echo "访问 http://localhost:8501 查看应用"
streamlit run app.py
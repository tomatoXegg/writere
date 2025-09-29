#!/bin/bash

# Chrome DevTools MCP 安装脚本
# 用于在公众号助手项目中安装Chrome DevTools MCP

echo "🚀 开始安装 Chrome DevTools MCP..."

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js"
    echo "   macOS: brew install node"
    echo "   Ubuntu: sudo apt install nodejs npm"
    echo "   Windows: 下载并安装 Node.js from https://nodejs.org/"
    exit 1
fi

# 检查 npm 是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装，请先安装 npm"
    exit 1
fi

# 显示 Node.js 和 npm 版本
echo "📋 当前环境信息:"
echo "   Node.js 版本: $(node --version)"
echo "   npm 版本: $(npm --version)"

# 安装 Chrome DevTools MCP
echo "📦 正在安装 Chrome DevTools MCP..."
if npm install -g chrome-devtools-mcp@latest; then
    echo "✅ Chrome DevTools MCP 安装成功!"
else
    echo "❌ Chrome DevTools MCP 安装失败"
    echo "   尝试使用 sudo 安装: sudo npm install -g chrome-devtools-mcp@latest"
    exit 1
fi

# 验证安装
echo "🔍 验证安装..."
if command -v chrome-devtools-mcp &> /dev/null; then
    echo "✅ Chrome DevTools MCP 已正确安装"
    chrome-devtools-mcp --version
else
    echo "✅ 通过 npx 运行 Chrome DevTools MCP"
    npx chrome-devtools-mcp@latest --version
fi

echo "🎉 安装完成!"
echo ""
echo "💡 使用说明:"
echo "   1. 重启 Streamlit 应用"
echo "   2. 在 '高级提取选项' 中启用 Chrome DevTools MCP"
echo "   3. 当 Firecrawl API 失败时，会自动使用 Chrome DevTools MCP"
echo ""
echo "🔧 故障排除:"
echo "   - 如果遇到权限问题，尝试: sudo npm install -g chrome-devtools-mcp@latest"
echo "   - 如果遇到网络问题，尝试: npm config set registry https://registry.npmjs.org/"
echo "   - 如果遇到 Chrome 问题，确保已安装 Chrome 浏览器"

# 检查 Chrome 浏览器是否安装
echo ""
echo "🔍 检查 Chrome 浏览器..."
if command -v google-chrome &> /dev/null; then
    echo "✅ Google Chrome 已安装"
elif command -v chrome &> /dev/null; then
    echo "✅ Chrome 浏览器已安装"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -d "/Applications/Google Chrome.app" ]; then
        echo "✅ Google Chrome 已安装"
    else
        echo "⚠️ 未检测到 Chrome 浏览器，建议安装 Chrome 浏览器"
    fi
else
    echo "⚠️ 未检测到 Chrome 浏览器，建议安装 Chrome 浏览器"
fi

echo ""
echo "🚀 Chrome DevTools MCP 安装完成！"
#!/usr/bin/env python3
"""
公众号内容助手测试脚本
用于验证API密钥配置和基本功能
"""

import sys
import os

def check_api_keys():
    """检查API密钥配置"""
    print("🔍 检查API密钥配置...")
    
    # 检查secrets.toml文件
    secrets_file = ".streamlit/secrets.toml"
    if not os.path.exists(secrets_file):
        print(f"❌ 配置文件不存在: {secrets_file}")
        return False
    
    # 读取配置文件
    try:
        with open(secrets_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查必需的API密钥
        required_keys = [
            "FIRECRAWL_API_KEY",
            "CLOUDINARY_CLOUD_NAME", 
            "CLOUDINARY_API_KEY",
            "CLOUDINARY_API_SECRET",
            "GEMINI_API_KEY"
        ]
        
        missing_keys = []
        for key in required_keys:
            if f'"{key}" = "your_' in content or f'{key} = "your_' in content:
                missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ 以下API密钥未配置:")
            for key in missing_keys:
                print(f"   - {key}")
            return False
        else:
            print("✅ 所有API密钥已配置")
            return True
            
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

def test_imports():
    """测试模块导入"""
    print("\n📦 测试模块导入...")
    
    required_modules = [
        'streamlit',
        'requests', 
        'google.generativeai',
        'cloudinary',
        're'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - 未安装")
            missing_modules.append(module)
    
    return len(missing_modules) == 0

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    # 测试正则表达式
    import re
    test_text = "![图片1](https://example.com/image1.jpg) 和 ![图片2](https://example.com/image2.png)"
    images = re.findall(r"!\[.*?\]\((.*?)\)", test_text)
    
    if len(images) == 2:
        print("✅ 图片链接正则表达式匹配正常")
    else:
        print("❌ 图片链接正则表达式匹配失败")
        return False
    
    # 测试环境变量读取
    test_env = os.getenv("TEST_VAR", "default")
    if test_env == "default":
        print("✅ 环境变量读取功能正常")
    else:
        print("❌ 环境变量读取功能异常")
        return False
    
    return True

def main():
    print("🚀 公众号内容助手 - 系统测试")
    print("=" * 50)
    
    # 切换到项目目录
    if os.path.basename(os.getcwd()) != "公众号助手":
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
    
    all_tests_passed = True
    
    # 运行测试
    if not check_api_keys():
        all_tests_passed = False
    
    if not test_imports():
        all_tests_passed = False
        
    if not test_basic_functionality():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 所有测试通过！系统已就绪")
        print("\n下一步:")
        print("1. 确保已安装所有依赖: pip install -r requirements.txt")
        print("2. 运行应用: streamlit run app.py")
        print("3. 在浏览器中访问显示的URL")
    else:
        print("❌ 部分测试失败，请检查配置")
        print("\n需要解决的问题:")
        print("- 确保所有API密钥已正确配置")
        print("- 安装缺失的Python包")
        print("- 检查网络连接")
    
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
API功能测试脚本
测试实际的API连接和功能
"""

import sys
import os
sys.path.append('.')

# 设置环境变量用于测试
os.environ['FIRECRAWL_API_KEY'] = 'fc-5d102eef37db442481ca5f2ff82471eb'
os.environ['CLOUDINARY_CLOUD_NAME'] = 'dkwkwgzrj'
os.environ['CLOUDINARY_API_KEY'] = '331941412943467'
os.environ['CLOUDINARY_API_SECRET'] = 'nSFDG9toy1oBWhI6cpNPOYFNmDY'
os.environ['GEMINI_API_KEY'] = 'AIzaSyDMHiBSRytM62PKxi1zSDE4D8CDIXEzEN0'

def test_firecrawl_api():
    """测试Firecrawl API连接"""
    print("🔥 测试Firecrawl API...")
    
    try:
        from app import get_content_from_firecrawl
        
        # 测试URL
        test_url = "https://mp.weixin.qq.com/s/abc123"  # 示例URL
        
        print(f"正在测试URL: {test_url}")
        result = get_content_from_firecrawl(test_url)
        
        if result and len(result) > 0:
            print("✅ Firecrawl API测试成功")
            print(f"返回内容长度: {len(result)} 字符")
            print(f"内容预览: {result[:200]}...")
            return True
        else:
            print("❌ Firecrawl API返回空内容")
            return False
            
    except Exception as e:
        print(f"❌ Firecrawl API测试失败: {str(e)}")
        return False

def test_cloudinary_api():
    """测试Cloudinary API连接"""
    print("\n☁️ 测试Cloudinary API...")
    
    try:
        from app import process_images_with_cloudinary
        
        # 测试包含图片的Markdown
        test_markdown = """
# 测试文章

这是一篇测试文章，包含以下图片：

![测试图片1](https://mmbiz.qpic.cn/mmbiz_jpg/test1.jpg)
![测试图片2](https://mmbiz.qpic.cn/mmbiz_png/test2.png)

文章内容结束。
"""
        
        print("正在测试图片上传...")
        result = process_images_with_cloudinary(test_markdown)
        
        if result and "cloudinary" in result.lower():
            print("✅ Cloudinary API测试成功")
            print("图片链接已成功转换为Cloudinary链接")
            return True
        else:
            print("❌ Cloudinary API测试失败，未检测到Cloudinary链接")
            return False
            
    except Exception as e:
        print(f"❌ Cloudinary API测试失败: {str(e)}")
        return False

def test_gemini_api():
    """测试Gemini API连接"""
    print("\n🤖 测试Gemini API...")
    
    try:
        from app import rewrite_with_gemini
        
        # 测试文本
        test_text = """
# 人工智能的发展

人工智能技术在近年来取得了巨大的进步。深度学习、机器学习和自然语言处理等技术的发展，使得AI能够更好地理解和处理人类语言。

本文将探讨人工智能的发展历程和未来趋势。
"""
        
        print("正在测试AI改写功能...")
        result = rewrite_with_gemini(test_text)
        
        if result and len(result) > 0:
            print("✅ Gemini API测试成功")
            print(f"改写后内容长度: {len(result)} 字符")
            print(f"改写内容预览: {result[:200]}...")
            return True
        else:
            print("❌ Gemini API返回空内容")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API测试失败: {str(e)}")
        return False

def test_full_workflow():
    """测试完整工作流程"""
    print("\n🔄 测试完整工作流程...")
    
    try:
        from app import get_content_from_firecrawl, process_images_with_cloudinary, rewrite_with_gemini
        
        # 模拟完整流程
        print("步骤1: 获取内容...")
        # 由于我们无法保证真实URL可用，我们模拟这一步
        mock_content = """
# 原始文章标题

这是原始文章内容，包含一些图片链接：

![图片1](https://example.com/image1.jpg)
![图片2](https://example.com/image2.png)

文章正文内容...
"""
        
        print("步骤2: 处理图片...")
        content_with_images = process_images_with_cloudinary(mock_content)
        
        print("步骤3: AI改写...")
        final_content = rewrite_with_gemini(content_with_images)
        
        if final_content and len(final_content) > 0:
            print("✅ 完整工作流程测试成功")
            print("所有步骤都正常工作")
            return True
        else:
            print("❌ 完整工作流程测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 完整工作流程测试失败: {str(e)}")
        return False

def main():
    print("🧪 公众号内容助手 - API功能测试")
    print("=" * 50)
    
    # 切换到项目目录
    if os.path.basename(os.getcwd()) != "公众号助手":
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
    
    results = []
    
    # 运行测试
    results.append(("Firecrawl API", test_firecrawl_api()))
    results.append(("Cloudinary API", test_cloudinary_api()))
    results.append(("Gemini API", test_gemini_api()))
    results.append(("完整工作流程", test_full_workflow()))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有API功能测试通过！")
        print("应用已准备就绪，可以正常使用！")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查配置和网络连接")
        return 1

if __name__ == "__main__":
    sys.exit(main())
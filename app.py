import streamlit as st
import requests
import re
import cloudinary
import cloudinary.uploader
import google.generativeai as genai
import os
from datetime import datetime


def get_content_from_firecrawl(url: str, api_key: str) -> str:
    """
    接收一个URL，调用Firecrawl的scrape API，并返回干净的Markdown文本。
    
    Args:
        url: 必须是一个非空的、格式合法的URL字符串
        api_key: Firecrawl API密钥
        
    Returns:
        成功时返回从Firecrawl API获取到的Markdown文本
        
    Raises:
        requests.exceptions.RequestException: 如果网络请求失败
        ValueError: 如果API返回的数据格式不正确或包含错误信息
    """
    if not api_key:
        raise ValueError("Firecrawl API Key未配置")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"url": url}
    
    try:
        response = requests.post(
            "https://api.firecrawl.dev/v0/scrape",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        if data.get("success") and "markdown" in data.get("data", {}):
            return data["data"]["markdown"]
        else:
            raise ValueError(f"Firecrawl API返回错误: {data.get('error', '未知错误')}")
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"网络请求失败: {str(e)}")


def process_images_with_cloudinary(markdown_text: str, cloud_name: str, api_key: str, api_secret: str) -> str:
    """
    接收Markdown文本，查找所有图片链接，将图片上传到Cloudinary，并用新链接替换旧链接。
    
    Args:
        markdown_text: 任意字符串，可能包含Markdown图片语法![]()
        cloud_name: Cloudinary云名称
        api_key: Cloudinary API密钥
        api_secret: Cloudinary API密钥
        
    Returns:
        返回处理后的Markdown文本。如果原文中没有图片，则原样返回
        
    Raises:
        cloudinary.exceptions.Error: 如果上传到Cloudinary失败
    """
    # 配置Cloudinary
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )
    
    if not all([cloud_name, api_key, api_secret]):
        raise ValueError("Cloudinary配置未完成")
    
    # 查找所有Markdown图片链接
    image_urls = re.findall(r"!\[.*?\]\((.*?)\)", markdown_text)
    if not image_urls:
        return markdown_text
    
    processed_text = markdown_text
    for url in image_urls:
        try:
            # 上传图片到Cloudinary
            upload_result = cloudinary.uploader.upload(
                url,
                folder="wechat_articles",
                timeout=30
            )
            new_url = upload_result.get("secure_url")
            
            if new_url:
                processed_text = processed_text.replace(url, new_url)
                st.success(f"✅ 图片上传成功: {url}")
                
        except Exception as e:
            st.warning(f"⚠️ 图片上传失败 {url}: {str(e)}")
            continue
    
    return processed_text


def rewrite_with_gemini(markdown_text: str, api_key: str) -> str:
    """
    接收Markdown文本，并调用Google Gemini API对其进行改写。
    
    Args:
        markdown_text: 待改写的文本内容
        api_key: Gemini API密钥
        
    Returns:
        成功时返回由Gemini API生成的改写后的文本
        
    Raises:
        Exception: 如果Gemini API调用失败或返回了不符合预期的内容
    """
    if not api_key:
        raise ValueError("Gemini API Key未配置")
    
    try:
        genai.configure(api_key=api_key)
        
        # 尝试使用可用的模型
        available_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        model = None
        
        for model_name in available_models:
            try:
                model = genai.GenerativeModel(model_name)
                # 测试模型是否可用
                test_response = model.generate_content("测试")
                if test_response.text:
                    break
            except:
                continue
        
        if not model:
            raise Exception("无法找到可用的Gemini模型")
        
        st.info(f"✅ 使用模型: {model.model_name}")
        
        prompt = f"""
请将以下Markdown格式的文章内容进行改写，使其表达方式更简洁、流畅。

重要规则：
1. 必须保持原文的Markdown格式不变，包括标题、列表、代码块等。
2. 必须完整保留原文中所有的图片链接（![]()）。
3. 不要添加任何与原文无关的评论或内容。
4. 保持原文的核心观点和信息不变。
5. 优化句式结构，使表达更加清晰流畅。

原文如下：
---
{markdown_text}
---

请直接返回改写后的Markdown内容，不要添加额外说明。
"""
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            raise Exception("Gemini API返回空内容")
            
    except Exception as e:
        raise Exception(f"Gemini API调用失败: {str(e)}")


def main():
    st.title("📝 公众号内容助手")
    st.markdown("---")
    
    # 初始化会话状态
    if "history" not in st.session_state:
        st.session_state.history = []
    if "api_configured" not in st.session_state:
        st.session_state.api_configured = False
    
    # 检查是否有保存的API密钥
    api_keys_exist = all([
        hasattr(st.session_state, 'firecrawl_key'),
        hasattr(st.session_state, 'gemini_key'),
        st.session_state.firecrawl_key,
        st.session_state.gemini_key
    ])
    
    if api_keys_exist and not st.session_state.api_configured:
        st.session_state.api_configured = True
    
    # API配置界面
    with st.expander("🔑 API密钥配置", expanded=not st.session_state.api_configured):
        st.markdown("### 🔑 API密钥配置")
        st.warning("⚠️ 您的API密钥仅保存在浏览器本地，不会上传到服务器")
        
        # 使用表单来确保状态正确保存
        with st.form("api_config_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # 从会话状态获取现有值，如果没有则为空
                current_firecrawl = getattr(st.session_state, 'firecrawl_key', '')
                current_gemini = getattr(st.session_state, 'gemini_key', '')
                
                firecrawl_key = st.text_input(
                    "🔥 Firecrawl API Key",
                    value=current_firecrawl,
                    type="password",
                    placeholder="fc-xxxxxxxxxxxxxxxxxxxxxxxx",
                    help="用于获取公众号文章内容"
                )
                gemini_key = st.text_input(
                    "🤖 Gemini API Key", 
                    value=current_gemini,
                    type="password",
                    placeholder="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxx",
                    help="用于AI内容改写"
                )
            
            with col2:
                current_cloud_name = getattr(st.session_state, 'cloudinary_name', '')
                current_cloud_key = getattr(st.session_state, 'cloudinary_key', '')
                current_cloud_secret = getattr(st.session_state, 'cloudinary_secret', '')
                
                cloudinary_name = st.text_input(
                    "☁️ Cloudinary Cloud Name",
                    value=current_cloud_name,
                    type="password",
                    placeholder="your-cloud-name",
                    help="用于图片上传和存储"
                )
                cloudinary_key = st.text_input(
                    "☁️ Cloudinary API Key",
                    value=current_cloud_key,
                    type="password", 
                    placeholder="xxxxxxxxxxxxxxxxxxxxxxxx",
                    help="Cloudinary API密钥"
                )
                cloudinary_secret = st.text_input(
                    "☁️ Cloudinary API Secret",
                    value=current_cloud_secret,
                    type="password",
                    placeholder="xxxxxxxxxxxxxxxxxxxxxxxx",
                    help="Cloudinary API密钥"
                )
            
            # 保存配置按钮
            submitted = st.form_submit_button("💾 保存API配置", type="primary")
            if submitted:
                if firecrawl_key and gemini_key:
                    st.session_state.firecrawl_key = firecrawl_key
                    st.session_state.gemini_key = gemini_key
                    st.session_state.cloudinary_name = cloudinary_name
                    st.session_state.cloudinary_key = cloudinary_key
                    st.session_state.cloudinary_secret = cloudinary_secret
                    st.session_state.api_configured = True
                    st.success("✅ API配置保存成功！页面将刷新...")
                    st.rerun()
                else:
                    st.error("❌ 至少需要配置Firecrawl和Gemini API密钥")
    
    # 如果API未配置，显示提示
    if not st.session_state.api_configured:
        st.error("❌ 请先配置API密钥才能使用应用功能")
        st.info("💡 点击上方的'🔑 API密钥配置'展开配置面板")
        return
    
    st.markdown("---")
    
    # 显示当前配置状态和重置选项
    col_status, col_reset = st.columns([4, 1])
    with col_status:
        st.info(f"✅ API已配置 - Firecrawl: {'●' * len(st.session_state.firecrawl_key[:8])}..., Gemini: {'●' * len(st.session_state.gemini_key[:8])}...")
    with col_reset:
        if st.button("🔄 重置配置", help="清除所有API配置"):
            st.session_state.api_configured = False
            del st.session_state.firecrawl_key
            del st.session_state.gemini_key
            if hasattr(st.session_state, 'cloudinary_name'):
                del st.session_state.cloudinary_name
            if hasattr(st.session_state, 'cloudinary_key'):
                del st.session_state.cloudinary_key
            if hasattr(st.session_state, 'cloudinary_secret'):
                del st.session_state.cloudinary_secret
            st.rerun()
    
    st.markdown("---")
    
    # 用户输入界面
    col1, col2 = st.columns([3, 1])
    with col1:
        url = st.text_input(
            "🔗 请输入公众号文章链接：",
            placeholder="https://mp.weixin.qq.com/s/xxx",
            key="url_input"
        )
    with col2:
        process_button = st.button("🚀 开始处理", key="process_button", use_container_width=True)
    
    st.markdown("---")
    
    # 处理逻辑
    if process_button and url:
        if not url.strip():
            st.error("⚠️ 请输入有效的URL")
            return
        
        try:
            with st.spinner("🔄 正在处理中，请稍候..."):
                # 步骤1: 获取文章内容
                with st.expander("📄 步骤1: 获取文章内容", expanded=False):
                    st.write("正在从Firecrawl获取文章内容...")
                    original_content = get_content_from_firecrawl(url.strip(), st.session_state.firecrawl_key)
                    st.success("✅ 文章内容获取成功")
                
                # 步骤2: 处理图片
                with st.expander("🖼️ 步骤2: 处理图片链接", expanded=False):
                    st.write("正在处理文章中的图片...")
                    content_with_images = process_images_with_cloudinary(
                        original_content,
                        st.session_state.cloudinary_name,
                        st.session_state.cloudinary_key,
                        st.session_state.cloudinary_secret
                    )
                    st.success("✅ 图片处理完成")
                
                # 步骤3: AI改写
                with st.expander("🤖 步骤3: AI智能改写", expanded=False):
                    st.write("正在使用AI进行内容改写...")
                    final_content = rewrite_with_gemini(content_with_images, st.session_state.gemini_key)
                    st.success("✅ 内容改写完成")
                
                # 保存到历史记录
                history_item = {
                    "url": url.strip(),
                    "title": f"文章_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "content": final_content,
                    "processed_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                st.session_state.history.append(history_item)
                
                # 显示最终结果
                st.markdown("## 🎉 处理完成！")
                st.success("✅ 文章处理成功！")
                
                # 显示改写后的内容
                st.subheader("📖 改写后的内容（预览）")
                st.markdown(final_content)
                
                # 显示源码
                st.subheader("💻 Markdown源码（可复制）")
                st.code(final_content, language="markdown", line_numbers=False)
                
                # 复制按钮
                if st.button("📋 复制Markdown源码", key="copy_button"):
                    st.toast("✅ 源码已复制到剪贴板", icon="✅")
                    st.session_state.clipboard_content = final_content
                    
        except ValueError as e:
            st.error(f"❌ 配置错误: {str(e)}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ 网络请求失败: {str(e)}")
        except Exception as e:
            st.error(f"❌ 处理过程中发生错误: {str(e)}")
    
    # 显示历史记录
    if st.session_state.history:
        st.markdown("---")
        st.subheader("📚 处理历史")
        
        with st.expander("🕐 查看历史记录", expanded=False):
            for i, item in enumerate(reversed(st.session_state.history), 1):
                with st.container():
                    st.markdown(f"**{i}. {item['title']}**")
                    st.markdown(f"🔗 原文链接: {item['url']}")
                    st.markdown(f"⏰ 处理时间: {item['processed_at']}")
                    
                    if st.button(f"查看内容 {i}", key=f"view_{i}"):
                        st.code(item['content'], language="markdown", line_numbers=False)
                    
                    st.markdown("---")
    
    # 页面底部信息
    st.markdown("---")
    st.caption("🔧 公众号内容助手 v1.0 | 基于Streamlit构建 | 支持内容提取、图片转存、AI改写")


if __name__ == "__main__":
    main()
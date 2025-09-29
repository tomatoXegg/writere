"""
Chrome DevTools MCP集成模块
用于处理Firecrawl API无法解决的复杂场景，如JavaScript渲染内容、动态加载等
"""
import asyncio
import json
import subprocess
import tempfile
import os
from typing import Optional, Dict, Any
import requests


class ChromeDevToolsExtractor:
    """Chrome DevTools MCP内容提取器"""
    
    def __init__(self):
        self.mcp_command = ["npx", "chrome-devtools-mcp@latest"]
        self.timeout = 60  # 60秒超时
        
    async def extract_wechat_article(self, url: str) -> str:
        """
        使用Chrome DevTools MCP提取微信公众号文章
        
        Args:
            url: 文章URL
            
        Returns:
            提取的Markdown格式文本
        """
        try:
            # 创建临时脚本文件
            script_content = self._create_extraction_script(url)
            
            # 执行Chrome DevTools MCP
            result = await self._execute_mcp_script(script_content)
            
            # 处理提取结果
            return self._process_extracted_content(result)
            
        except Exception as e:
            raise Exception(f"Chrome DevTools MCP提取失败: {str(e)}")
    
    def _create_extraction_script(self, url: str) -> str:
        """创建提取脚本"""
        return f"""
// Chrome DevTools MCP 提取脚本
async function extractWechatArticle(url) {{
    try {{
        // 1. 创建新页面并导航
        const page = await newPage();
        await page.goto(url, {{ 
            waitUntil: 'networkidle2',
            timeout: 30000 
        }});
        
        // 2. 等待主要内容加载
        await page.waitForSelector('.rich_media_content', {{ timeout: 10000 }})
            .catch(() => page.waitForSelector('.article-content', {{ timeout: 10000 }}))
            .catch(() => page.waitForSelector('.content', {{ timeout: 10000 }}));
        
        // 3. 移除不必要的元素
        await page.evaluate(() => {{
            const elementsToRemove = [
                'script', 'style', 'iframe', 'noscript',
                '.ad', '.advertisement', '.share-btn',
                '.like-btn', '.comment-section'
            ];
            elementsToRemove.forEach(selector => {{
                document.querySelectorAll(selector).forEach(el => el.remove());
            }});
        }});
        
        // 4. 提取文章内容
        const content = await page.evaluate(() => {{
            // 尝试多个可能的内容选择器
            const selectors = [
                '.rich_media_content',
                '.article-content', 
                '.content',
                '.article',
                '.post-content'
            ];
            
            for (const selector of selectors) {{
                const element = document.querySelector(selector);
                if (element) {{
                    return element.innerHTML;
                }}
            }}
            
            // 如果都没找到，返回body内容
            return document.body.innerHTML;
        }});
        
        // 5. 获取文章标题
        const title = await page.evaluate(() => {{
            const titleSelectors = [
                'h1', '.rich_media_title', '.article-title',
                '.title', 'meta[property="og:title"]'
            ];
            
            for (const selector of titleSelectors) {{
                const element = document.querySelector(selector);
                if (element) {{
                    return element.textContent || element.getAttribute('content');
                }}
            }}
            return '未知标题';
        }});
        
        // 6. 清理并格式化内容
        const cleanContent = await page.evaluate((content, title) => {{
            // 移除多余的HTML标签和属性
            let cleaned = content
                .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
                .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
                .replace(/class="[^"]*"/g, '')
                .replace(/style="[^"]*"/g, '')
                .replace(/<div[^>]*>/gi, '')
                .replace(/<\/div>/gi, '')
                .replace(/<span[^>]*>/gi, '')
                .replace(/<\/span>/gi, '')
                .replace(/\s+/g, ' ')
                .trim();
            
            // 生成Markdown格式
            return `# ${{title}}\n\n${{cleaned}}`;
        }}, content, title);
        
        return cleanContent;
        
    }} catch (error) {{
        console.error('提取失败:', error);
        // 如果提取失败，返回页面基本HTML
        return await page.evaluate(() => document.body.outerHTML);
    }}
}}

// 执行提取
extractWechatArticle('{url}').then(result => {{
    console.log(JSON.stringify({{ success: true, content: result }}));
}}).catch(error => {{
    console.log(JSON.stringify({{ success: false, error: error.message }}));
}});
"""
    
    async def _execute_mcp_script(self, script_content: str) -> Dict[str, Any]:
        """执行MCP脚本"""
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(script_content)
                temp_file = f.name
            
            try:
                # 使用subprocess执行Chrome DevTools MCP
                result = subprocess.run(
                    self.mcp_command + [temp_file],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                
                if result.returncode == 0:
                    # 尝试解析JSON输出
                    output = result.stdout.strip()
                    if output.startswith('{') and output.endswith('}'):
                        return json.loads(output)
                    else:
                        return {"success": True, "content": output}
                else:
                    raise Exception(f"Chrome DevTools MCP执行失败: {result.stderr}")
                    
            finally:
                # 清理临时文件
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            raise Exception("Chrome DevTools MCP执行超时")
        except Exception as e:
            raise Exception(f"执行Chrome DevTools MCP时发生错误: {str(e)}")
    
    def _process_extracted_content(self, result: Dict[str, Any]) -> str:
        """处理提取的内容"""
        if not result.get("success", False):
            raise Exception(result.get("error", "未知错误"))
        
        content = result.get("content", "")
        
        # 进一步清理内容
        content = self._clean_html_content(content)
        
        return content
    
    def _clean_html_content(self, html_content: str) -> str:
        """清理HTML内容并转换为Markdown"""
        try:
            # 基本的HTML清理
            cleaned = html_content
            
            # 移除脚本和样式
            cleaned = cleaned.replace(r'<script[^>]*>[\s\S]*?</script>', '')
            cleaned = cleaned.replace(r'<style[^>]*>[\s\S]*?</style>', '')
            
            # 转换常见HTML标签为Markdown
            cleaned = cleaned.replace(r'<h1[^>]*>', '# ').replace(r'</h1>', '')
            cleaned = cleaned.replace(r'<h2[^>]*>', '## ').replace(r'</h2>', '')
            cleaned = cleaned.replace(r'<h3[^>]*>', '### ').replace(r'</h3>', '')
            cleaned = cleaned.replace(r'<p[^>]*>', '').replace(r'</p>', '\n\n')
            cleaned = cleaned.replace(r'<strong[^>]*>', '**').replace(r'</strong>', '**')
            cleaned = cleaned.replace(r'<b[^>]*>', '**').replace(r'</b>', '**')
            cleaned = cleaned.replace(r'<em[^>]*>', '*').replace(r'</em>', '*')
            cleaned = cleaned.replace(r'<i[^>]*>', '*').replace(r'</i>', '*')
            
            # 处理链接
            cleaned = cleaned.replace(r'<a[^>]*href="([^"]*)"[^>]*>', r'[\1](').replace(r'</a>', ')')
            
            # 处理图片
            cleaned = cleaned.replace(r'<img[^>]*src="([^"]*)"[^>]*>', r'![\1](\1)')
            
            # 移除其他HTML标签
            cleaned = cleaned.replace(r'<[^>]*>', '')
            
            # 清理多余空白
            cleaned = cleaned.replace(r'\s+', ' ').replace(r'\n\s*\n', '\n\n').strip()
            
            return cleaned
            
        except Exception:
            # 如果清理失败，返回原始内容
            return html_content


class HybridExtractor:
    """混合提取器 - 结合Firecrawl和Chrome DevTools MCP"""
    
    def __init__(self, firecrawl_api_key: str = None):
        self.firecrawl_api_key = firecrawl_api_key
        self.chrome_extractor = ChromeDevToolsExtractor()
    
    async def extract_content(self, url: str, use_chrome_fallback: bool = True) -> str:
        """
        提取内容，优先使用Firecrawl，失败后使用Chrome DevTools MCP
        
        Args:
            url: 文章URL
            use_chrome_fallback: 是否在Firecrawl失败时使用Chrome DevTools MCP
            
        Returns:
            提取的内容
        """
        # 首先尝试Firecrawl API
        if self.firecrawl_api_key:
            try:
                return await self._extract_with_firecrawl(url)
            except Exception as e:
                print(f"Firecrawl提取失败: {e}")
                if use_chrome_fallback:
                    print("尝试使用Chrome DevTools MCP...")
                else:
                    raise
        
        # 降级到Chrome DevTools MCP
        if use_chrome_fallback:
            return await self.chrome_extractor.extract_wechat_article(url)
        else:
            raise Exception("Firecrawl提取失败且未启用Chrome DevTools MCP降级")
    
    async def _extract_with_firecrawl(self, url: str) -> str:
        """使用Firecrawl API提取内容"""
        headers = {
            "Authorization": f"Bearer {self.firecrawl_api_key}",
            "Content-Type": "application/json"
        }
        payload = {"url": url}
        
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
            raise Exception(f"Firecrawl API返回错误: {data.get('error', '未知错误')}")


# 使用示例
async def test_extraction():
    """测试提取功能"""
    extractor = HybridExtractor(firecrawl_api_key="your-firecrawl-api-key")
    
    # 测试URL
    test_url = "https://mp.weixin.qq.com/s/example"
    
    try:
        content = await extractor.extract_content(test_url)
        print("提取成功!")
        print(f"内容长度: {len(content)} 字符")
        print(content[:500] + "..." if len(content) > 500 else content)
    except Exception as e:
        print(f"提取失败: {e}")


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_extraction())
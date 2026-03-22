#!/usr/bin/env python3
"""
Enhanced WeChat article fetcher with cookie support.
Export cookies from your Mac browser and use them on the server.

Usage:
  python3 fetch_wechat.py <url> --cookie "__biz=xxx;wap_sid2=yyy"
"""

import sys
import json
import re


def parse_cookies(cookie_string):
    """Parse cookie string into list of dicts."""
    cookies = []
    for item in cookie_string.split(';'):
        item = item.strip()
        if '=' in item:
            name, value = item.split('=', 1)
            cookies.append({
                "name": name.strip(),
                "value": value.strip(),
                "domain": ".mp.weixin.qq.com",
                "path": "/"
            })
    return cookies


def fetch_wechat_with_cookies(url, cookie_string=None, max_chars=30000):
    """Fetch WeChat article with optional cookies."""
    from scrapling.fetchers import StealthyFetcher
    
    fetcher = StealthyFetcher()
    
    # Build options
    options = {
        "headless": True,
        "network_idle": True,
        "timeout": 30000,
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    # Add cookies if provided
    if cookie_string:
        options["cookies"] = parse_cookies(cookie_string)
    
    print(f"🕷️ 使用 StealthyFetcher 获取中...", file=sys.stderr)
    print(f"配置：{json.dumps(options, ensure_ascii=False, default=str)}", file=sys.stderr)
    
    try:
        page = fetcher.fetch(url, **options)
        
        # 检查是否成功（没有验证页面）
        html = page.html
        if "环境异常" in html or "验证" in html:
            print("⚠️ 警告：检测到验证页面，Cookie 可能已过期或无效", file=sys.stderr)
        
        # 提取内容
        content_selectors = [
            "div#js_content",
            "div.rich_media_content",
            "article",
            "main",
        ]
        
        for selector in content_selectors:
            els = page.css(selector)
            if els:
                content = els[0].html_content
                if len(content) > 500:
                    # 转换 HTML 到 Markdown
                    import html2text
                    h = html2text.HTML2Text()
                    h.body_width = 0
                    h.skip_internal_links = True
                    
                    # 修复懒加载图片
                    content = re.sub(
                        r'<img([^>]*?)\sdata-src="([^"]+)"([^>]*?)>',
                        lambda m: f'<img{m.group(1)} src="{m.group(2)}"{m.group(3)}>',
                        content
                    )
                    
                    md = h.handle(content)
                    md = re.sub(r"\n{3,}", "\n\n", md).strip()
                    
                    return md[:max_chars], selector
        
        # Fallback
        return page.text[:max_chars], "fallback"
        
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        raise


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_wechat.py <url> [--cookie \"__biz=xxx;wap_sid2=yyy\"] [max_chars]", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    cookie_string = None
    max_chars = 30000
    
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--cookie" and i + 1 < len(sys.argv):
            cookie_string = sys.argv[i + 1]
        elif not arg.startswith("--"):
            try:
                max_chars = int(arg)
            except ValueError:
                pass
    
    if not cookie_string:
        print("⚠️ 未提供 Cookie，可能遇到验证", file=sys.stderr)
        print("建议：在 Mac 浏览器中访问文章，导出 Cookie 后使用 --cookie 参数", file=sys.stderr)
    
    try:
        md, selector = fetch_wechat_with_cookies(url, cookie_string, max_chars)
        print(f"\n✅ 成功！使用选择器：{selector}\n", file=sys.stderr)
        print("=" * 60)
        print(md)
    except Exception as e:
        print(f"失败：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

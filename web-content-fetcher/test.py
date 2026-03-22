from scrapling.fetchers import StealthyFetcher

try:
    # 测试一个简单网站
    page = StealthyFetcher().fetch("https://httpbin.org/user-agent", headless=True)
    print("Headless 工作正常:", page.text)
except Exception as e:
    print("错误:", e)

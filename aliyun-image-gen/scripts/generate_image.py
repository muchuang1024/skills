#!/usr/bin/env python3
"""
阿里云百炼 wanx2.1-t2i-plus 图片生成脚本

用法:
    python generate_image.py --prompt "描述文本" [--size "1024x1024"] [--n 1] [--output "image.png"]

环境变量:
    ALIYUN_BAILIAN_API_KEY: 阿里云百炼 API Key (必需)
    或通过 .env 文件配置
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional, List

import requests


def load_config():
    """从 .env 文件加载配置"""
    config = {}
    skill_dir = Path(__file__).parent.parent
    env_file = skill_dir / '.env'
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
    return config


def get_api_key() -> str:
    """
    获取 API Key
    优先级：系统环境变量 > .env 文件
    """
    # 优先从系统环境变量读取
    api_key = os.environ.get("ALIYUN_BAILIAN_API_KEY")
    
    # 如果环境变量未设置，尝试从 .env 文件读取
    if not api_key:
        config = load_config()
        api_key = config.get('ALIYUN_BAILIAN_API_KEY', '')
    
    # 兼容旧的环境变量名
    if not api_key:
        api_key = os.environ.get("ALIYUN_API_KEY", "")
    
    return api_key


def generate_image(
    prompt: str,
    api_key: str,
    size: str = "1024x1024",
    n: int = 1,
    output_path: Optional[str] = None,
) -> str:
    """
    调用阿里云百炼 wanx2.1-t2i-plus API 生成图片

    Args:
        prompt: 图片描述文本
        api_key: 阿里云百炼 API Key
        size: 图片尺寸，可选值：1024x1024, 1024x768, 768x1024, 512x512
        n: 生成图片数量 (1-4)
        output_path: 输出文件路径

    Returns:
        生成的图片路径
    """
    # 阿里云百炼 API 端点 - 使用任务提交模式
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",  # 启用异步模式
    }

    # 转换尺寸格式 (1024x1024 -> 1024*1024)
    size_formatted = size.replace("x", "*")
    
    # 请求体
    payload = {
        "model": "wanx2.1-t2i-plus",
        "input": {
            "prompt": prompt,
        },
        "parameters": {
            "size": size_formatted,
            "n": n,
        },
    }

    try:
        # 提交异步任务
        print(f"Submitting image generation task...", file=sys.stderr)
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"Error response: {response.text}", file=sys.stderr)
            response.raise_for_status()
        
        result = response.json()
        print(f"Task submitted: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)

        # 获取任务 ID
        if "output" not in result or "task_id" not in result["output"]:
            raise ValueError(f"Invalid response - no task_id: {result}")

        task_id = result["output"]["task_id"]
        print(f"Task ID: {task_id}", file=sys.stderr)

        # 轮询获取结果
        image_urls = poll_task_result(task_id, api_key)
        
        if not image_urls:
            raise RuntimeError("No images generated")

        # 下载图片
        downloaded_paths = []
        for i, img_url in enumerate(image_urls):
            if output_path and n == 1:
                path = output_path
            else:
                base, ext = os.path.splitext(output_path or "generated_image.png")
                path = f"{base}_{i+1}{ext}"
            
            download_image(img_url, path)
            downloaded_paths.append(path)
            print(f"Image saved: {path}", file=sys.stderr)
        
        return downloaded_paths[0] if downloaded_paths else ""

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")


def poll_task_result(task_id: str, api_key: str, max_retries: int = 60, delay: int = 2) -> List[str]:
    """
    轮询获取异步任务结果

    Args:
        task_id: 任务 ID
        api_key: API Key
        max_retries: 最大重试次数
        delay: 每次轮询间隔（秒）

    Returns:
        图片 URL 列表
    """
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    for attempt in range(max_retries):
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        if "output" not in result:
            raise ValueError(f"Invalid response: {result}")

        output = result["output"]
        task_status = output.get("task_status", "UNKNOWN")
        print(f"Task status: {task_status} (attempt {attempt + 1}/{max_retries})", file=sys.stderr)

        if task_status == "SUCCEEDED":
            results = output.get("results", [])
            urls = []
            for r in results:
                if "url" in r:
                    urls.append(r["url"])
                elif "b64_json" in r:
                    # 处理 base64 图片
                    import tempfile
                    img_data = base64.b64decode(r["b64_json"])
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                        f.write(img_data)
                        urls.append(f.name)
            return urls
        elif task_status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"Task {task_status}: {result}")

        time.sleep(delay)

    raise TimeoutError(f"Task polling timeout after {max_retries} attempts")


def download_image(url: str, output_path: str) -> None:
    """下载图片到本地"""
    if url.startswith("http"):
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
    else:
        # 本地文件路径
        import shutil
        shutil.copy(url, output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate image using Aliyun Bailian wanx2.1-t2i-plus"
    )
    parser.add_argument("--prompt", required=True, help="Image description prompt")
    parser.add_argument(
        "--size",
        default="1024x1024",
        help="Image size (1024x1024, 1024x768, 768x1024, 512x512)"
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="Number of images to generate (1-4)"
    )
    parser.add_argument(
        "--output",
        default="generated_image.png",
        help="Output file path"
    )

    args = parser.parse_args()

    # 获取 API Key（支持环境变量和 .env 文件）
    api_key = get_api_key()
    if not api_key:
        print(
            "Error: ALIYUN_BAILIAN_API_KEY environment variable is required\n"
            "Set it via:\n"
            "  export ALIYUN_BAILIAN_API_KEY=\"your-key\"\n"
            "Or create a .env file in the skill directory",
            file=sys.stderr
        )
        sys.exit(1)

    try:
        result_path = generate_image(
            prompt=args.prompt,
            api_key=api_key,
            size=args.size,
            n=args.n,
            output_path=args.output,
        )
        print(result_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

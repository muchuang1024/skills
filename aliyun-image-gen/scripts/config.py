#!/usr/bin/env python3
"""
配置管理模块

从 .env 文件加载配置，支持环境变量覆盖
"""

import os
from pathlib import Path


def load_config():
    """
    从 .env 文件加载配置
    
    Returns:
        dict: 配置字典
    """
    config = {}
    
    # 获取技能根目录
    skill_dir = Path(__file__).parent.parent
    env_file = skill_dir / '.env'
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过注释和空行
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
    
    return config


def get_api_key() -> str:
    """
    获取阿里云百炼 API Key
    
    优先级：
    1. 系统环境变量 ALIYUN_BAILIAN_API_KEY
    2. .env 文件中的 ALIYUN_BAILIAN_API_KEY
    3. 系统环境变量 ALIYUN_API_KEY（兼容旧版本）
    
    Returns:
        str: API Key，如果未找到则返回空字符串
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


def get_model_name() -> str:
    """
    获取默认模型名称
    
    Returns:
        str: 模型名称，默认为 wanx2.1-t2i-plus
    """
    config = load_config()
    return config.get('ALIYUN_MODEL', 'wanx2.1-t2i-plus')


if __name__ == '__main__':
    # 测试配置读取
    print("配置测试:")
    print(f"  API Key: {get_api_key()[:20]}..." if get_api_key() else "  API Key: 未设置")
    print(f"  模型：{get_model_name()}")

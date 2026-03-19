# 阿里云百炼图片生成技能

使用阿里云百炼平台的 **wanx2.1-t2i-plus** 模型，根据文本描述生成高质量图片。

## 快速开始

### 1. 配置 API Key

**方式一：环境变量**
```bash
export ALIYUN_BAILIAN_API_KEY="sk-your-api-key"
```

**方式二：.env 文件**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

### 2. 生成图片

```bash
python3 scripts/generate_image.py \
  --prompt "一只可爱的橘猫在草地上玩耍" \
  --size 1024x1024 \
  --output cat.png
```

## 文档

- [完整技能文档](SKILL.md)
- [API 参考](references/api_reference.md)

## 支持的尺寸

- `1024x1024` - 正方形（推荐）
- `1024x768` - 横屏
- `768x1024` - 竖屏
- `512x512` - 小尺寸

## 获取 API Key

1. 登录 [阿里云百炼控制台](https://bailian.console.aliyun.com)
2. 进入 "API-KEY 管理" 页面
3. 创建或复制 API Key

## 许可证

MIT License

---
name: aliyun-image-gen
description: |
  使用阿里云百炼 wanx2.1-t2i-plus 模型生成图片。
  当用户需要生成图片、AI 绘图、文生图时使用此技能。
  支持多种尺寸（1024x1024, 1024x768, 768x1024, 512x512）和风格。
  需要配置 ALIYUN_BAILIAN_API_KEY 环境变量。
---

# 阿里云百炼图片生成

使用阿里云百炼平台的 **wanx2.1-t2i-plus** 模型，根据文本描述生成高质量图片。

> **模型说明**: 使用阿里云万相专业文生图模型 `wanx2.1-t2i-plus`，非通义千问多模态模型。

## 前置准备

### 1. 获取 API Key

1. 登录 [阿里云百炼控制台](https://bailian.console.aliyun.com)
2. 进入 "API-KEY 管理" 页面
3. 创建或复制已有的 API Key

### 2. 配置环境变量

**方式一：系统环境变量（推荐）**

在 `~/.bashrc` 中添加：
```bash
export ALIYUN_BAILIAN_API_KEY="sk-your-api-key"
source ~/.bashrc
```

**方式二：.env 文件**

在技能目录下创建 `.env` 文件：
```bash
ALIYUN_BAILIAN_API_KEY=sk-your-api-key
```

### 3. 验证配置

```bash
python3 scripts/generate_image.py --prompt "测试" --output test.png
```

## 使用方法

### 快速生成

```bash
python3 scripts/generate_image.py \
  --prompt "一只可爱的橘猫在草地上玩耍" \
  --size 1024x1024 \
  --output cat.png
```

### 参数说明

| 参数 | 说明 | 默认值 | 必填 |
|------|------|--------|------|
| `--prompt` | 图片描述文本 | - | ✅ |
| `--size` | 图片尺寸 | 1024x1024 | ❌ |
| `--n` | 生成数量 (1-4) | 1 | ❌ |
| `--output` | 输出文件路径 | generated_image.png | ❌ |

### 支持的尺寸

| 尺寸 | 比例 | 场景 |
|------|------|------|
| `1024x1024` | 1:1 | 正方形（推荐） |
| `1024x768` | 4:3 | 横屏/桌面壁纸 |
| `768x1024` | 3:4 | 竖屏/手机壁纸 |
| `512x512` | 1:1 | 小尺寸/头像 |

## Prompt 编写指南

### 有效描述结构

```
[主体] + [场景/背景] + [风格] + [光线] + [视角] + [质量词]
```

### 示例

**动物**:
```
一只金毛犬在海边奔跑，夕阳下的剪影，写实摄影风格，温暖的色调，高清细节，8k 画质
```

**人物**:
```
一位穿着汉服的年轻女子在竹林中，古风插画风格，柔和光线，唯美意境，精致五官
```

**风景**:
```
极光下的冰岛黑沙滩，星空银河，长曝光摄影，超现实风光，8k 画质，广角镜头
```

**产品**:
```
极简白色咖啡杯，大理石桌面，俯拍角度，产品摄影，柔和自然光，商业广告级别
```

**建筑**:
```
现代简约风格的别墅，落地窗，蓝天白云，建筑摄影，黄昏时分，温暖光线
```

### 风格关键词参考

| 风格 | 关键词 |
|------|--------|
| 写实照片 | photorealistic, 8k uhd, professional photography, 高清细节 |
| 动漫插画 | anime style, illustration, studio ghibli style, 二次元 |
| 油画 | oil painting, impressionist, renaissance, 油画质感 |
| 赛博朋克 | cyberpunk, neon lights, futuristic, 科幻，未来感 |
| 水墨画 | chinese ink painting, watercolor, traditional art, 国画风格 |
| 3D 渲染 | 3D render, octane render, blender, C4D, 三维渲染 |
| 像素艺术 | pixel art, 8-bit, retro game style, 像素风 |

### 负面提示（避免的内容）

在 prompt 中可以添加避免的内容：
```
避免：模糊，低质量，变形，多余的手指，水印，文字
```

## 操作步骤

### 流程 1：快速生成单张图片

```bash
# 1. 确保 API Key 已配置
echo $ALIYUN_BAILIAN_API_KEY

# 2. 生成图片
python3 scripts/generate_image.py \
  --prompt "一只可爱的猫咪" \
  --output cat.png

# 3. 查看生成的图片
open cat.png  # macOS
xdg-open cat.png  # Linux
```

### 流程 2：批量生成多张图片

```bash
# 一次性生成 4 张不同版本
python3 scripts/generate_image.py \
  --prompt "未来城市景观，赛博朋克风格" \
  --size 1024x768 \
  --n 4 \
  --output city.png

# 生成文件：city_1.png, city_2.png, city_3.png, city_4.png
```

### 流程 3：在 Python 代码中调用

```python
from scripts.generate_image import generate_image

# 生成图片
image_path = generate_image(
    prompt="一只可爱的橘猫",
    api_key="sk-your-api-key",
    size="1024x1024",
    n=1,
    output_path="cat.png"
)
print(f"图片已生成：{image_path}")
```

## 完整 API 参考

详细 API 文档见 [references/api_reference.md](references/api_reference.md)

## 故障排查

### API Key 错误
```
Error: ALIYUN_BAILIAN_API_KEY environment variable is required
```
**解决**: 设置环境变量 `export ALIYUN_BAILIAN_API_KEY="your-key"`

### 任务超时
- 图片生成通常需要 5-30 秒
- 脚本会自动轮询等待结果（最多 60 次，每次 2 秒）
- 如超时，检查网络连接和 API Key 有效性

### 图片质量不佳
- 使用更详细的描述
- 添加质量关键词如 "8k", "high quality", "detailed"
- 明确指定风格和光线条件
- 避免模糊、抽象的描述

### API 调用失败
```
Error: API request failed: 400 Bad Request
```
**可能原因**:
- API Key 无效或过期
- 账号未开通百炼服务
- 余额不足

**解决**:
1. 检查 API Key 是否正确
2. 登录百炼控制台确认服务状态
3. 检查账号余额

## 注意事项

1. **图片有效期**: 生成的图片 URL 有效期为 24 小时，请及时下载
2. **并发限制**: 根据账号等级有不同的并发限制
3. **内容审核**: 生成内容需符合法律法规，禁止生成违规内容
4. **版权说明**: 生成图片的版权归属请参考阿里云官方说明
5. **计费说明**: 按生成次数计费，具体价格参考阿里云官网

## 资源索引

### 核心脚本
- [scripts/generate_image.py](scripts/generate_image.py) - 图片生成主脚本
- [scripts/config.py](scripts/config.py) - 配置管理模块

### 参考文档
- [references/api_reference.md](references/api_reference.md) - 完整 API 接口说明

### 相关链接
- [阿里云百炼控制台](https://bailian.console.aliyun.com)
- [万相模型文档](https://help.aliyun.com/zh/model-studio/)
- [API Key 管理](https://bailian.console.aliyun.com/#/api-key)

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-03-17 | 初始版本，支持 wanx2.1-t2i-plus 模型 |

# 阿里云百炼 wanx2.1-t2i-plus API 参考

## 模型信息

- **模型名称**: `wanx2.1-t2i-plus`
- **模型系列**: 阿里云万相 (Wanx)
- **提供商**: 阿里云百炼 (Bailian)
- **功能**: 专业文生图模型（Text-to-Image）
- **状态**: ✅ 正式商用

> **注意**: 非通义千问多模态模型 `qwen-image-2.0`（已下线）

## API 端点

### 提交生成任务（异步）

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
```

**请求头**:
```http
Authorization: Bearer {api_key}
Content-Type: application/json
X-DashScope-Async: enable
```

**请求体**:
```json
{
  "model": "wanx2.1-t2i-plus",
  "input": {
    "prompt": "图片描述文本"
  },
  "parameters": {
    "size": "1024*1024",
    "n": 1
  }
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 固定值：`wanx2.1-t2i-plus` |
| input.prompt | string | 是 | 图片描述文本，支持中英文 |
| parameters.size | string | 否 | 图片尺寸，可选：`1024*1024`, `1024*768`, `768*1024`, `512*512` |
| parameters.n | integer | 否 | 生成数量，范围 1-4，默认 1 |

**响应示例**:
```json
{
  "output": {
    "task_id": "task-xxx",
    "task_status": "PENDING"
  },
  "request_id": "req-xxx"
}
```

### 查询任务结果

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

**请求头**:
```http
Authorization: Bearer {api_key}
```

**响应示例（成功）**:
```json
{
  "output": {
    "task_id": "task-xxx",
    "task_status": "SUCCEEDED",
    "results": [
      {
        "url": "https://.../image.png"
      }
    ]
  },
  "request_id": "req-xxx"
}
```

**任务状态**:
- `PENDING`: 等待中
- `RUNNING`: 运行中
- `SUCCEEDED`: 成功
- `FAILED`: 失败
- `CANCELLED`: 已取消

## 环境变量配置

### 方式一：系统环境变量

```bash
export ALIYUN_BAILIAN_API_KEY="your-api-key-here"
```

### 方式二：.env 文件

在技能目录下创建 `.env` 文件：
```bash
ALIYUN_BAILIAN_API_KEY=your-api-key-here
```

## Prompt 编写建议

### 基本结构
```
[主体描述], [场景/背景], [风格], [光线], [视角], [质量词]
```

### 示例

**写实风格**:
```
一只橘猫在阳光下打盹，毛发细节清晰，温暖的光线，8k 高清，专业摄影
```

**动漫风格**:
```
一个穿着校服的女孩站在樱花树下，动漫风格，柔和的色彩，宫崎骏风格
```

**产品设计**:
```
一款极简风格的白色无线耳机，产品摄影，纯白背景，专业灯光，商业广告
```

**风景**:
```
雪山日出，金色阳光洒在雪山顶上，湖面倒影，超广角镜头，壮丽风光摄影
```

**建筑**:
```
现代简约风格的别墅，落地窗，蓝天白云，建筑摄影，黄昏时分，温暖光线
```

### 常用风格词

| 风格 | 关键词 |
|------|--------|
| 写实/照片级 | photorealistic, realistic, 8k uhd, professional photography |
| 动漫 | anime style, cartoon, illustration, 二次元 |
| 油画 | oil painting, impressionist, renaissance |
| 水彩 | watercolor, pastel colors |
| 赛博朋克 | cyberpunk, neon lights, futuristic, 科幻 |
| 水墨 | chinese ink painting, watercolor, traditional art, 国画 |
| 3D 渲染 | 3D render, octane render, blender, C4D |
| 像素艺术 | pixel art, 8-bit, retro game style |

### 质量增强词

- `8k` - 超高分辨率
- `high quality` - 高质量
- `detailed` - 细节丰富
- `ultra detailed` - 极致细节
- `professional` - 专业级别
- `masterpiece` - 杰作

## 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 400 | 请求参数错误 | 检查请求体和参数格式 |
| 401 | API Key 无效 | 检查 API Key 是否正确 |
| 403 | 权限不足 | 确认账号已开通百炼服务 |
| 429 | 请求频率超限 | 降低请求频率或升级账号 |
| 500 | 服务器内部错误 | 稍后重试 |

### 错误响应示例

```json
{
  "code": "InvalidApiKey",
  "message": "Invalid API key provided",
  "request_id": "req-xxx"
}
```

## 限制说明

| 限制项 | 说明 |
|--------|------|
| 单张生成时间 | 约 5-30 秒 |
| 图片 URL 有效期 | 生成后 24 小时内可下载 |
| 并发限制 | 根据账号等级有所不同 |
| 每日配额 | 根据账号类型和余额 |
| 内容审核 | 禁止生成违规内容 |

## 计费说明

- **计费方式**: 按生成次数计费
- **价格参考**: 请访问 [阿里云百炼价格页面](https://www.aliyun.com/price/product)
- **免费额度**: 新账号可能有免费试用额度

## 可用模型版本

| 模型 | 说明 | 推荐场景 |
|------|------|---------|
| `wanx2.1-t2i-plus` | 专业版，质量最高 | 高质量图片生成 ✅ |
| `wanx2.1-t2i-turbo` | 快速版，速度优先 | 快速原型/测试 |
| `wanx2.1-t2i-pro` | 高级版，平衡性能 | 通用场景 |

## 相关资源

- [阿里云百炼控制台](https://bailian.console.aliyun.com)
- [API Key 管理](https://bailian.console.aliyun.com/#/api-key)
- [百炼帮助文档](https://help.aliyun.com/zh/model-studio/)
- [万相模型文档](https://help.aliyun.com/zh/model-studio/product-overview/wanx)

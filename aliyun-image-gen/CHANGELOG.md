# 更新日志

## [1.0.1] - 2026-03-19

### 改进
- ✅ 统一模型名称：将所有 `qwen-image-2.0` 改为 `wanx2.1-t2i-plus`
- ✅ 添加配置管理模块 `scripts/config.py`
- ✅ 支持从 `.env` 文件读取 API Key
- ✅ 兼容多种环境变量名（`ALIYUN_BAILIAN_API_KEY`, `ALIYUN_API_KEY`）
- ✅ 完善 SKILL.md 文档结构
- ✅ 更新 API 参考文档
- ✅ 添加 `.env.example` 模板文件
- ✅ 添加 `.gitignore` 配置
- ✅ 添加 README.md 快速开始指南
- ✅ 删除冗余文件 `generate_image_modified.py`

### 修复
- 修复文档中模型名称不一致的问题
- 修复脚本注释中的模型名称错误

## [1.0.0] - 2026-03-17

### 新增
- 初始版本发布
- 支持阿里云百炼 wanx2.1-t2i-plus 模型
- 支持多种图片尺寸
- 支持批量生成（1-4 张）
- 异步任务轮询机制

# 后端代码目录

本目录包含后端源代码，由后端开发专家维护，后端测试专家编写测试。

## 架构约束

```
API 路由层 (api/) → 业务逻辑层 (services/) → 数据访问层 (repositories/) → 数据模型层 (models/)
```

- 禁止 API 路由直接调用 Repository（必须经过 Service）
- 禁止 Service 直接操作数据库连接（必须通过 Repository）
- 禁止跨层直接访问（必须逐层调用）
- 禁止在 API 路由层编写业务逻辑

## 安全约束

- 禁止硬编码密钥/Token/密码
- 禁止 SQL 拼接（必须使用参数化查询或 ORM）
- 所有用户输入必须通过 Pydantic 校验
- 敏感信息使用环境变量（`app/config.py`）
- 错误信息不得泄露内部细节

## 技术栈

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0 (async)
- Alembic（数据库迁移）
- Pydantic v2（数据校验）

## 代码规范

- 遵循 PEP 8
- 使用 Type Hints
- 行宽 120 字符
- 每个模型必须有 `id`、`created_at`、`updated_at` 字段
- 外键必须有 `ondelete` 策略

## 测试

- 测试代码放在 `tests/` 子目录
- pytest + pytest-asyncio + httpx
- AAA 模式（Arrange-Act-Assert）

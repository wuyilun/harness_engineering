---
name: backend-dev
description: "Use this skill when implementing Python backend code. Covers the complete workflow from project scaffolding to API implementation, following the layered architecture pattern (API → Service → Repository → Model) with FastAPI."
---

# 后端开发 Skill

## 你的角色

你是后端开发专家，使用 Python 3 + FastAPI 实现高质量的后端服务。

## 技术栈

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0 (async)
- Alembic
- Pydantic v2
- pytest + httpx

## 工作流程

### 步骤 1：读取上游产出

并行读取：
- `project/tech_design/{task_id}_design.md` → 技术方案
- `project/api_specs/{task_id}_api.yaml` → API 契约

### 步骤 2：项目脚手架（新项目）

运行 [初始化脚本](scripts/init_project.py) 创建项目骨架：

```
src/backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── api/
│   │   └── v1/
│   ├── services/
│   ├── repositories/
│   └── middleware/
├── alembic/
├── alembic.ini
├── requirements.txt
└── tests/
```

### 步骤 3：实现功能

按分层架构逐层实现，严格遵循调用规则：

**API 路由层** → **Service 层** → **Repository 层** → **Model 层**

#### 3.1 数据模型（Model）

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

#### 3.2 Pydantic Schema

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

#### 3.3 Repository 层

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UserRepository:
    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
```

#### 3.4 Service 层

```python
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, db: AsyncSession, user_id: int) -> UserResponse:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserResponse.model_validate(user)
```

#### 3.5 API 路由

```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(UserRepository())
    return await service.get_user(db, user_id)
```

### 步骤 4：数据库迁移

```bash
cd src/backend
alembic revision --autogenerate -m "add users table"
alembic upgrade head
```

### 步骤 5：安全自检

- [ ] 所有用户输入通过 Pydantic 校验
- [ ] 所有 API 端点有认证（按技术方案）
- [ ] 无 SQL 拼接
- [ ] 无硬编码密钥
- [ ] 错误信息不泄露内部细节
- [ ] 日志不包含敏感信息

### 步骤 6：依赖管理

`requirements.txt` 模板：
```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.13.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
asyncpg>=0.29.0  # PostgreSQL
python-jose[cryptography]>=3.3.0  # JWT
passlib[bcrypt]>=1.7.4  # 密码哈希
httpx>=0.26.0  # 测试
pytest>=7.4.0
pytest-asyncio>=0.23.0
```

## 输出

- 后端代码：`src/backend/app/`
- 迁移脚本：`src/backend/alembic/`
- 依赖文件：`src/backend/requirements.txt`

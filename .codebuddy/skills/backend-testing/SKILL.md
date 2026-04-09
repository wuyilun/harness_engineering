---
name: backend-testing
description: "Use this skill when writing and executing Python backend tests. Covers unit tests, API tests, and integration tests with pytest, httpx, and FastAPI TestClient. Produces structured test reports with API contract compliance verification."
---

# 后端测试 Skill

## 你的角色

你是后端测试专家，负责为 Python 后端代码编写和执行测试，产出结构化测试报告。

## 测试工具

- pytest + pytest-asyncio
- httpx / FastAPI TestClient
- pytest-mock

## 工作流程

### 步骤 1：读取输入

- 后端代码路径
- API 契约（了解接口规范）
- 技术方案（了解业务逻辑）

### 步骤 2：制定测试计划

列出需要测试的：
1. 所有 API 端点（每个端点 5-7 个用例）
2. Service 层核心业务逻辑
3. 数据模型约束

### 步骤 3：配置测试环境

确保 `conftest.py` 配置了：
- 测试数据库（SQLite in-memory 或独立测试库）
- FastAPI TestClient
- 测试用认证 Token

### 步骤 4：编写 API 测试（L2）

每个 API 端点测试用例模板：

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_user_with_valid_data_returns_201(client: AsyncClient):
    """POST /api/v1/users - 正常创建用户返回 201"""
    # Arrange
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!"
    }

    # Act
    response = await client.post("/api/v1/users", json=user_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "password" not in data  # 不返回密码

@pytest.mark.asyncio
async def test_create_user_with_missing_field_returns_422(client: AsyncClient):
    """POST /api/v1/users - 缺少必填字段返回 422"""
    response = await client.post("/api/v1/users", json={"username": "test"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_without_auth_returns_401(client: AsyncClient):
    """POST /api/v1/users - 未认证返回 401"""
    unauth_client = AsyncClient(app=app, base_url="http://test")
    response = await unauth_client.post("/api/v1/users", json={...})
    assert response.status_code == 401
```

### 步骤 5：编写单元测试（L1）

Service 和 Repository 层测试：

```python
@pytest.mark.asyncio
async def test_user_service_get_existing_user(db_session):
    """UserService.get_user - 存在的用户返回正确数据"""
    # Arrange
    user = User(username="test", email="test@example.com", hashed_password="xxx")
    db_session.add(user)
    await db_session.commit()

    # Act
    service = UserService(UserRepository())
    result = await service.get_user(db_session, user.id)

    # Assert
    assert result.username == "test"
```

### 步骤 6：执行测试

```bash
cd src/backend
python -m pytest tests/ -v --cov=app --cov-report=term-missing
```

### 步骤 7：API 契约一致性验证

对照 `project/api_specs/{task_id}_api.yaml`：
- 检查响应字段是否与 Schema 一致
- 检查错误码是否与定义一致
- 检查分页格式是否一致

### 步骤 8：产出测试报告

保存到 `project/test_reports/{task_id}_backend_test.md`。

## conftest.py 模板

```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import settings

# 测试数据库
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    async_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
```

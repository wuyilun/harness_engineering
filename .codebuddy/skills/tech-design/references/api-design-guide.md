# API 设计规范

## RESTful API 设计原则

### URL 命名
- 使用名词复数：`/api/v1/users`、`/api/v1/orders`
- 嵌套资源最多两层：`/api/v1/users/{id}/orders`
- 使用 kebab-case：`/api/v1/user-profiles`

### HTTP 方法
| 方法 | 用途 | 幂等性 |
|------|------|--------|
| GET | 查询资源 | 是 |
| POST | 创建资源 | 否 |
| PUT | 全量更新 | 是 |
| PATCH | 部分更新 | 否 |
| DELETE | 删除资源 | 是 |

### 状态码
| 状态码 | 含义 | 使用场景 |
|--------|------|---------|
| 200 | 成功 | GET/PUT/PATCH 成功 |
| 201 | 已创建 | POST 成功 |
| 204 | 无内容 | DELETE 成功 |
| 400 | 请求错误 | 参数格式错误 |
| 401 | 未认证 | Token 缺失或过期 |
| 403 | 无权限 | 权限不足 |
| 404 | 不存在 | 资源未找到 |
| 409 | 冲突 | 重复创建 |
| 422 | 不可处理 | 参数校验失败 |
| 500 | 服务器错误 | 未预期异常 |

### 分页
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```
查询参数：`page`, `page_size`, `sort_by`, `sort_order`

### 错误响应
```json
{
  "detail": "Human readable error message",
  "code": "ERROR_CODE",
  "fields": {
    "field_name": ["error message"]
  }
}
```

### 认证
- 使用 Bearer Token（JWT）
- Header：`Authorization: Bearer <token>`
- Token 过期时间：Access Token 15min, Refresh Token 7d

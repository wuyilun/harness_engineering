---
name: tech-design
description: "Use this skill when creating technical design documents, API contracts, and data models. Provides a complete workflow from requirement analysis to architecture design, including technology selection, API design (OpenAPI 3.0), database schema, and frontend-backend interface contracts."
---

# 技术方案 Skill

## 你的角色

你是技术架构师，负责根据需求文档产出可执行的技术方案和 API 契约。

## 技术栈约定

- **后端**：Python 3 + FastAPI（优先）
- **前端**：React（优先）或 Vue，根据项目特征决定
- **数据库**：PostgreSQL（生产优先）、SQLite（轻量级）
- **API 风格**：RESTful

## 工作流程

### 步骤 1：分析需求

读取 `project/requirements/{task_id}_requirement.md`，深入理解功能需求和非功能需求。

### 步骤 2：技术选型决策

根据需求特征做出技术选型，记录决策理由：

| 决策点 | 考量因素 |
|--------|---------|
| React vs Vue | 生态成熟度、团队熟悉度、项目复杂度 |
| PostgreSQL vs SQLite | 数据量、并发需求、部署复杂度 |
| 是否需要缓存 | 读取频率、数据实时性要求 |
| 是否需要消息队列 | 异步处理需求、解耦需求 |

**前端框架选择原则**：
- 复杂交互 + 大型应用 → React
- 中等复杂 + 快速迭代 → Vue
- 已有项目沿用现有框架

### 步骤 3：设计 API 契约

产出 OpenAPI 3.0 格式的 API 契约 `project/api_specs/{task_id}_api.yaml`。

参考 [API 设计规范](references/api-design-guide.md)。

核心要素：
- 所有端点的请求/响应格式
- 数据模型定义（Schema）
- 认证方式
- 错误码定义
- 分页/排序/过滤规则

### 步骤 4：设计数据模型

- ER 关系（文字描述）
- 表结构定义（字段、类型、约束、索引）
- 数据迁移策略

### 步骤 5：前后端任务拆分

将技术方案拆分为前端任务和后端任务，每个任务独立可验证：
- FT-001: 前端任务描述
- BT-001: 后端任务描述

### 步骤 6：安全与性能考量

- 认证和授权方案
- 数据加密策略
- 缓存策略
- 性能优化方案
- 技术风险识别

### 步骤 7：产出技术方案

按模板产出，保存到 `project/tech_design/{task_id}_design.md`。

### 步骤 8：自验证

- [ ] API 契约覆盖所有功能需求
- [ ] 数据模型支撑所有 API 存取
- [ ] 前后端接口一致
- [ ] 安全考量满足非功能需求
- [ ] 技术风险已识别和缓解

## 输出

- 技术方案文档：`project/tech_design/{task_id}_design.md`
- API 契约：`project/api_specs/{task_id}_api.yaml`

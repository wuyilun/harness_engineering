# Harness Engineering - 多专家协作软件开发系统

## 项目定位

基于 Harness Engineering 范式构建的多专家协作软件开发环境。核心公式：**Agent = Model + Harness**。

系统通过硬约束（Rules）、专业能力包（Skills）、结构化通信协议，让 8 个专业 Agent 在受控边界内可靠协作。

## 架构总览

```
┌──────────────────────────────────────────────────────────┐
│                  第三层：验证与验收层                       │
│  前端测试专家 ←→ 后端测试专家 ←→ 功能验收专家              │
├──────────────────────────────────────────────────────────┤
│                  第二层：执行与开发层                       │
│  需求专家 → 技术方案专家 → 前端开发专家 + 后端开发专家       │
├──────────────────────────────────────────────────────────┤
│                  第一层：调度与约束层                       │
│  PM 专家（调度）+ Rules（硬约束）+ Skills（能力包）         │
└──────────────────────────────────────────────────────────┘
```

## Agent 清单

| Agent | 模型 | 职责 | 关键约束 |
|-------|------|------|---------|
| `pm-orchestrator` | glm-5.1 | 总调度，任务拆解与分配 | 绝不直接编写代码 |
| `requirement-expert` | glm-4.7 | 需求分析与文档化 | 只产出需求文档 |
| `tech-architect` | glm-5.1 | 技术方案与架构设计 | 只产出技术方案 |
| `frontend-developer` | glm-4.7 | 前端代码实现 | 只修改前端目录 |
| `backend-developer` | glm-4.7 | 后端代码实现 | 只修改后端目录 |
| `frontend-tester` | glm-4.7 | 前端测试 | 只写测试，不修业务代码 |
| `backend-tester` | glm-4.7 | 后端测试 | 只写测试，不修业务代码 |
| `acceptance-expert` | glm-4.7 | 功能验收 | 只读代码，不修改任何文件 |

## 技术栈

- **前端**：React（优先）或 Vue，由技术方案专家根据项目需求决定
- **后端**：Python 3（FastAPI 优先）
- **API 契约**：OpenAPI 3.0 / OpenSpec 格式

## 工作流

```
用户需求 → PM 拆解 → 需求专家 → 技术方案专家 → 前端+后端并行开发 → 前端+后端并行测试 → 功能验收 → 交付/打回
```

## 前端设计质量保证

前端开发专家集成 Impeccable 设计技能体系（21 个 skill），确保：
- 开发前通过 `impeccable teach` 建立设计上下文
- 开发前通过 `shape` 产出设计简报
- 开发后通过 `audit` + `critique` 进行质量检查
- 发布前通过 `polish` 进行最终打磨

## 目录结构

```
harness_engineering/
├── .codebuddy/
│   ├── agents/              # 8 个 Agent 定义
│   ├── rules/               # 5 个硬约束规则
│   ├── skills/              # 21 Impeccable + 7 业务 Skill
│   └── MEMORY.md
├── project/                 # 运行时产出（需求/方案/报告）
│   ├── progress.json
│   ├── requirements/
│   ├── tech_design/
│   ├── api_specs/
│   ├── test_reports/
│   └── acceptance_reports/
├── src/                     # 项目源代码
│   ├── frontend/
│   └── backend/
└── CODEBUDDY.md
```

## Rules 规则

| 规则 | 应用方式 | 作用 |
|------|---------|------|
| `security-constraints` | 总是 | 安全硬约束 |
| `architecture-boundaries` | 总是 | 架构边界隔离 |
| `agent-protocol` | 智能体请求 | Agent 通信协议 |
| `code-standards` | 智能体请求 | 编码规范 |
| `testing-standards` | 智能体请求 | 测试规范 |

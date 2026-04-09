# Harness Engineering 项目记忆

## 项目概况
- 类型：基于 Harness Engineering 范式的多专家协作软件开发系统
- 核心公式：Agent = Model + Harness
- 创建日期：2026-04-09
- 架构：CodeBuddy 原生（agents + rules + skills + memory）

## Harness 核心原则
1. **硬约束 > 软约束**：用 Rules + 工具白名单 + 操作分级替代 Prompt 中的"请遵守"
2. **上下文隔离**：每个专家只看自己职责范围内的信息
3. **自验证循环**：每个专家产出必须经过验证才能流转
4. **PM 只调度不干活**：PM 是编排器，不是执行者
5. **熵治理**：每次错误都转化为约束的增强

## Agent 配置

| Agent | 模型 | 职责 | 硬约束 |
|-------|------|------|--------|
| pm-orchestrator | glm-5.1 | 总调度 | 绝不写代码 |
| requirement-expert | glm-4.7 | 需求分析 | 只产出需求文档 |
| tech-architect | glm-5.1 | 技术方案 | 只产出方案+API契约 |
| frontend-developer | glm-4.7 | 前端开发 | 只修改 src/frontend/ |
| backend-developer | glm-4.7 | 后端开发 | 只修改 src/backend/ |
| frontend-tester | glm-4.7 | 前端测试 | 只写测试，不修业务代码 |
| backend-tester | glm-4.7 | 后端测试 | 只写测试，不修业务代码 |
| acceptance-expert | glm-4.7 | 功能验收 | 只读代码，不修改任何文件 |

## 技术栈
- 前端：React（优先）或 Vue，由技术方案专家决定
- 后端：Python 3 + FastAPI
- 数据库：PostgreSQL（生产）/ SQLite（轻量）
- API 契约：OpenAPI 3.0

## Rules 体系
- security-constraints（总是）：安全硬约束
- architecture-boundaries（总是）：架构边界隔离
- agent-protocol（智能体请求）：Agent 通信协议
- code-standards（智能体请求）：编码规范
- testing-standards（智能体请求）：测试规范

## Skills 体系

### 业务 Skills（7个）
- requirement-analysis：需求分析工作流
- tech-design：技术方案工作流 + API 设计规范
- frontend-dev：前端开发工作流（集成 Impeccable）
- backend-dev：后端开发工作流（Python/FastAPI 分层架构）
- frontend-testing：前端测试工作流
- backend-testing：后端测试工作流
- acceptance-test：功能验收工作流

### Impeccable 设计 Skills（21个）
- impeccable：核心设计 skill（teach/craft 模式）
- shape：设计规划
- polish：最终打磨
- audit：技术质量审计
- critique：UX 设计评审
- arrange/typeset/bolder/distill/delight/harden/normalize/clarify/adapt/animate/colorize/extract/optimize/quieter/overdrive/onboard

### Impeccable 参考文档（8个）
位于 skills/impeccable/reference/：
- typography.md、color-and-contrast.md、spatial-design.md
- motion-design.md、interaction-design.md、responsive-design.md
- ux-writing.md、craft.md

## 工作流
```
用户需求 → PM 拆解 → 需求专家 → 技术方案专家 → 前端+后端并行开发 → 前端+后端并行测试 → 功能验收 → 交付/打回
```

## 目录结构
```
.codebuddy/
├── agents/          # 8 个 Agent 定义
├── rules/           # 5 个硬约束规则
├── skills/          # 21 Impeccable + 7 业务 Skill
└── MEMORY.md

project/             # 运行时产出
├── progress.json    # 全局进度
├── requirements/    # 需求文档
├── tech_design/     # 技术方案
├── api_specs/       # OpenSpec API 契约
├── test_reports/    # 测试报告
└── acceptance_reports/  # 验收报告

src/                 # 项目源代码
├── frontend/
└── backend/
```

## 关键决策记录

### 2026-04-09 初始化
- 模型分配：PM + 技术方案用 glm-5.1，其余用 glm-4.7
- 后端确定使用 Python 3 + FastAPI
- 前端 React/Vue 由技术方案专家根据项目特征决定
- 前端集成 Impeccable 设计技能体系确保 UI 质量
- Impeccable skills 从 GitHub 下载并适配 Codebuddy 格式（替换模板变量）

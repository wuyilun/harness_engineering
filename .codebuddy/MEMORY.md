# Harness Engineering 项目记忆

## 项目概况
- 类型：基于 Harness Engineering 范式的多专家协作软件开发系统
- 核心公式：Agent = Model + Harness
- 创建日期：2026-04-09
- 架构：CodeBuddy 原生（agents + rules + skills + memory + openspec）

## Harness 核心原则
1. **硬约束 > 软约束**：用 Rules + 工具白名单 + 操作分级替代 Prompt 中的"请遵守"
2. **上下文隔离**：每个专家只看自己职责范围内的信息
3. **自验证循环**：每个专家产出必须经过验证才能流转
4. **PM 只调度不干活**：PM 是编排器，不是执行者
5. **熵治理**：每次错误都转化为约束的增强
6. **可拆卸性**：模型、规则、技能包均可独立替换升级

## Agent 配置

| Agent | 模型 | 职责 | 硬约束 |
|-------|------|------|--------|
| pm-orchestrator | glm-5.1 | 总调度 | 绝不写代码 |
| requirement-expert | glm-4.7 | 需求分析 | 只产出需求文档 + OpenSpec proposal/specs |
| tech-architect | glm-5.1 | 技术方案 | 只产出方案+API契约 + OpenSpec design/tasks |
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
- 规范驱动：OpenSpec（SDD 工作流）

## OpenSpec 集成

### 工作流映射

| OpenSpec 命令 | Harness 阶段 | 执行方式 |
|--------------|-------------|---------|
| `/opsx:propose` | 需求分析 + 技术方案 | 需求专家产出 proposal+specs，技术方案专家产出 design+tasks |
| `/opsx:apply` | 并行开发 | 前端+后端开发专家按 tasks.md 逐条实现 |
| `/opsx:explore` | 需求探索 | 不写代码，纯思考探索 |
| `/opsx:archive` | 归档 | 验收通过后归档变更 |

### OpenSpec 目录

```
openspec/
├── changes/           # 活跃变更
│   └── {name}/
│       ├── .openspec.yaml
│       ├── proposal.md    # 需求专家产出
│       ├── specs/         # 需求专家产出
│       ├── design.md      # 技术方案专家产出
│       └── tasks.md       # 技术方案专家产出
└── changes/archive/   # 已归档变更
```

### 关键约束
- OpenSpec 的 proposal/specs 由**需求专家**产出，不由 PM 直接写
- OpenSpec 的 design/tasks 由**技术方案专家**产出
- `/opsx:apply` 执行时**必须受架构边界约束控制**

## 记忆体系

### 三层记忆架构

| 层级 | 文件 | 加载时机 | 内容 |
|------|------|---------|------|
| 项目总览 | `CODEBUDDY.md` | 始终加载 | Agent/Rules/Skills/工作流概览 |
| 子目录记忆 | `src/frontend/CODEBUDDY.md` | 操作前端目录时 | 前端架构、设计系统、约束 |
| 子目录记忆 | `src/backend/CODEBUDDY.md` | 操作后端目录时 | 后端架构、分层约束、安全规范 |
| 长期记忆 | `.codebuddy/MEMORY.md` | 始终加载 | 经验沉淀、决策记录、错误转约束 |

### 记忆驱动质量提升

| 事件 | 记忆动作 |
|------|---------|
| 验收不通过 | 记录失败原因 → 转化为未来约束 |
| 同一问题迭代 3 轮 | 记录问题模式 → 建议增加 Rule |
| 新技术选型 | 记录决策理由 → 供后续项目参考 |
| 性能/安全问题 | 记录根因 → 更新安全/编码规则 |
| Impeccable audit 发现反模式 | 记录反模式 → 更新设计红线 |

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

### OpenSpec Skills（4个）
- openspec-propose：创建变更提案（proposal + specs + design + tasks）
- openspec-apply：按 tasks.md 逐条实现
- openspec-explore：需求探索模式（不写代码）
- openspec-archive：归档已完成变更

### Impeccable 设计 Skills（21个）
- impeccable：核心设计 skill（teach/craft 模式）
- shape：设计规划
- polish：最终打磨
- audit：技术质量审计
- critique：UX 设计评审
- arrange/typeset/bolder/distill/delight/harden/normalize/clarify/adapt/animate/colorize/extract/optimize/quieter/overdrive/onboard

## 工作流

### 双模式工作流

**模式一：OpenSpec 规范驱动**（推荐用于新功能）
```
/opsx:propose → 需求专家(proposal+specs) → 技术方案专家(design+tasks) → /opsx:apply(前端+后端开发) → 测试 → 验收 → /opsx:archive
```

**模式二：传统 Harness 流程**（直接描述需求时）
```
用户需求 → PM 拆解 → 需求专家 → 技术方案专家 → 前端+后端并行开发 → 前端+后端并行测试 → 功能验收 → 交付/打回
```

## 关键决策记录

### 2026-04-09 初始化
- 模型分配：PM + 技术方案用 glm-5.1，其余用 glm-4.7
- 后端确定使用 Python 3 + FastAPI
- 前端 React/Vue 由技术方案专家根据项目特征决定
- 前端集成 Impeccable 设计技能体系确保 UI 质量
- Impeccable skills 从 GitHub 下载并适配 Codebuddy 格式（替换模板变量）

### 2026-04-10 OpenSpec + 记忆增强
- 集成 OpenSpec 规范驱动开发框架（npm install -g @fission-ai/openspec@latest）
- OpenSpec 工作流与 Harness 多专家映射：propose→需求+方案，apply→开发，archive→验收归档
- 创建三层记忆架构：项目总览 + 子目录记忆 + 长期经验记忆
- 子目录 CODEBUDDY.md 实现上下文隔离（前端/后端各自独立的约束文档）
- 记忆驱动质量提升：错误转约束、决策记录、反模式沉淀

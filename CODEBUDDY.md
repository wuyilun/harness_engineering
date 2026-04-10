# Harness Engineering - 多专家协作软件开发系统

## 项目定位

基于 Harness Engineering 范式构建的多专家协作软件开发环境。核心公式：**Agent = Model + Harness**。

系统通过硬约束（Rules）、专业能力包（Skills）、结构化通信协议、规范驱动开发（OpenSpec）和分层记忆体系，让 8 个专业 Agent 在受控边界内可靠协作。

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
│  + OpenSpec（规范驱动）+ Memory（记忆体系）                │
└──────────────────────────────────────────────────────────┘
```

## Agent 清单

| Agent | 模型 | 职责 | 关键约束 |
|-------|------|------|---------|
| `pm-orchestrator` | glm-5.1 | 总调度，任务拆解与分配 | 绝不直接编写代码 |
| `requirement-expert` | glm-4.7 | 需求分析与文档化 | 只产出需求文档 + OpenSpec proposal/specs |
| `tech-architect` | glm-5.1 | 技术方案与架构设计 | 只产出技术方案 + OpenSpec design/tasks |
| `frontend-developer` | glm-4.7 | 前端代码实现 | 只修改前端目录 |
| `backend-developer` | glm-4.7 | 后端代码实现 | 只修改后端目录 |
| `frontend-tester` | glm-4.7 | 前端测试 | 只写测试，不修业务代码 |
| `backend-tester` | glm-4.7 | 后端测试 | 只写测试，不修业务代码 |
| `acceptance-expert` | glm-4.7 | 功能验收 | 只读代码，不修改任何文件 |

## 技术栈

- **前端**：React（优先）或 Vue，由技术方案专家根据项目需求决定
- **后端**：Python 3（FastAPI 优先）
- **API 契约**：OpenAPI 3.0
- **规范驱动**：OpenSpec（SDD 工作流）

## 双模式工作流

### 模式一：OpenSpec 规范驱动（推荐）

```
/opsx:propose → 需求专家(proposal+specs) → 技术方案专家(design+tasks) → /opsx:apply(开发) → 测试 → 验收 → /opsx:archive
```

| OpenSpec 命令 | Harness 阶段 | 说明 |
|--------------|-------------|------|
| `/opsx:propose` | 需求 + 技术方案 | 产出 proposal.md + specs/ + design.md + tasks.md |
| `/opsx:apply` | 并行开发 | 按 tasks.md 逐条实现，受架构边界约束 |
| `/opsx:explore` | 需求探索 | 纯思考探索，不写代码 |
| `/opsx:archive` | 归档 | 验收通过后归档变更 |

### 模式二：传统 Harness 流程

```
用户需求 → PM 拆解 → 需求专家 → 技术方案专家 → 前端+后端并行开发 → 前端+后端并行测试 → 功能验收 → 交付/打回
```

## 项目自动初始化

前端/后端开发专家在首次收到开发任务时，自动检测项目是否已初始化：

- **前端**：检测 `src/frontend/package.json`，不存在则执行 `bash .codebuddy/skills/frontend-dev/scripts/init_project.sh [react|vue] src/frontend`
- **后端**：检测 `src/backend/app/main.py`，不存在则执行 `python3 .codebuddy/skills/backend-dev/scripts/init_project.py src/backend`

也可手动初始化（克隆模板后）：
```bash
bash .codebuddy/skills/frontend-dev/scripts/init_project.sh react src/frontend
python3 .codebuddy/skills/backend-dev/scripts/init_project.py src/backend
```

## 前端设计质量保证

前端开发专家集成 Impeccable 设计技能体系（21 个 skill），确保：
- 开发前通过 `impeccable teach` 建立设计上下文
- 开发前通过 `shape` 产出设计简报
- 开发后通过 `audit` + `critique` 进行质量检查
- 发布前通过 `polish` 进行最终打磨

## 记忆驱动质量提升

三层记忆架构，确保项目质量持续提升：

| 层级 | 文件 | 加载时机 | 作用 |
|------|------|---------|------|
| 项目总览 | `CODEBUDDY.md` | 始终加载 | 全局架构和约束 |
| 子目录记忆 | `src/frontend/CODEBUDDY.md` | 操作前端时 | 前端架构、设计系统 |
| 子目录记忆 | `src/backend/CODEBUDDY.md` | 操作后端时 | 后端架构、分层约束 |
| 长期经验 | `.codebuddy/MEMORY.md` | 始终加载 | 经验沉淀、决策记录 |

**记忆触发规则**：
- 验收不通过 → 记录原因，转化为未来约束
- 同一问题迭代 3 轮 → 记录模式，建议增加 Rule
- 新技术选型 → 记录决策理由
- Impeccable audit 发现反模式 → 更新设计红线

## 目录结构

```
harness_engineering/
├── .codebuddy/
│   ├── agents/              # 8 个 Agent 定义
│   ├── commands/             # OpenSpec 斜杠命令
│   ├── rules/               # 5 个硬约束规则
│   ├── skills/              # 32 个 Skill（7 业务 + 4 OpenSpec + 21 Impeccable）
│   └── MEMORY.md            # 长期经验记忆
├── openspec/                # OpenSpec 规范驱动目录
│   └── changes/             # 变更提案（proposal/specs/design/tasks）
├── project/                 # 运行时产出（需求/方案/报告）
│   ├── progress.json
│   ├── requirements/
│   ├── tech_design/
│   ├── api_specs/
│   ├── test_reports/
│   └── acceptance_reports/
├── src/                     # 项目源代码
│   ├── frontend/            # 含 CODEBUDDY.md 子目录记忆
│   └── backend/             # 含 CODEBUDDY.md 子目录记忆
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

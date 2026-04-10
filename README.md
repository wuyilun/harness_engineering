<div align="center">

# Harness Engineering

**多专家协作软件开发系统**

*Agent = Model + Harness*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CodeBuddy](https://img.shields.io/badge/Powered%20by-CodeBuddy-green.svg)](https://www.codebuddy.ai)

</div>

---

## 什么是 Harness Engineering？

Harness Engineering 是一种 AI Agent 工程方法论，核心理念是 **Agent = Model + Harness**。与其依赖模型自身的"自觉性"，不如用硬约束（Rules）、专业能力包（Skills）和结构化协议（Protocols）构建一套"安全带"，让 Agent 在受控边界内可靠协作。

本仓库是一套基于 [CodeBuddy](https://www.codebuddy.ai) 平台的完整 Harness 实现，包含 **8 个专业 Agent**、**5 条硬约束规则**、**32 个技能包**、[OpenSpec](https://openspec.pro) 规范驱动开发 和 **分层记忆体系**，可直接用于创建高质量的全栈软件项目。

### 六大核心支柱

| 支柱 | 本项目实现 |
|------|-----------|
| **硬约束 > 软约束** | Rules 替代 Prompt 中的"请遵守"，可执行、可检测 |
| **上下文隔离** | 每个 Agent 只看到自己职责范围内的信息，通过结构化接口通信 |
| **自验证循环** | 每个环节产出必须经过验证才能流转到下游 |
| **PM 只调度不干活** | PM 是编排器，绝不亲自下场写代码 |
| **熵治理** | 每次错误都转化为约束的增强 |
| **可拆卸性** | 模型、规则、技能包均可独立替换升级 |

---

## 架构总览

```
┌──────────────────────────────────────────────────────────────┐
│                     第三层：验证与验收层                        │
│  前端测试专家 ←→ 后端测试专家 ←→ 功能验收专家                   │
│  （质量保障，产出必须通过验证才能流转）                           │
├──────────────────────────────────────────────────────────────┤
│                     第二层：执行与开发层                         │
│  需求专家 → 技术方案专家 → 前端开发专家 + 后端开发专家            │
│  （各司其职，结构化接口通信，互不干涉）                           │
├──────────────────────────────────────────────────────────────┤
│                     第一层：调度与约束层                         │
│  PM 专家（调度） + Rules（硬约束） + Skills（能力包）            │
│  （PM 只分发任务，不写代码；Rules 强制边界）                     │
└──────────────────────────────────────────────────────────────┘
```

---

## 8 个专业 Agent

| Agent | 模型 | 职责 | 硬约束 |
|-------|------|------|--------|
| 🎯 **PM 专家** | glm-5.1 | 总调度，任务拆解与分配 | 绝不直接编写代码 |
| 📋 **需求专家** | glm-4.7 | 需求分析与文档化 | 只产出需求文档 |
| 🏗️ **技术方案专家** | glm-5.1 | 技术方案与架构设计 | 只产出方案 + API 契约 |
| 🎨 **前端开发专家** | glm-4.7 | 前端代码实现 | 只修改 `src/frontend/` |
| ⚙️ **后端开发专家** | glm-4.7 | 后端代码实现 | 只修改 `src/backend/` |
| 🧪 **前端测试专家** | glm-4.7 | 前端测试 | 只写测试，不修业务代码 |
| 🧪 **后端测试专家** | glm-4.7 | 后端测试 | 只写测试，不修业务代码 |
| ✅ **功能验收专家** | glm-4.7 | 功能验收 | 只读代码，不修改任何文件 |

### 模型分配策略

- **glm-5.1**（强推理）：PM 专家、技术方案专家 — 需要全局推理、权衡决策
- **glm-4.7**（高效执行）：开发、测试、验收专家 — 需要执行、生成、校验

> 模型选择是 Harness 的配置项，不是硬编码。后续如果某个专家表现不佳，只需修改 `model` 字段即可升级。

---

## 端到端工作流

```
用户需求 → PM 拆解 → 需求专家 → 技术方案专家 → 前端+后端并行开发 → 前端+后端并行测试 → 功能验收 → 交付/打回
```

### 流转规则

1. **上游产出未完成，下游不启动**
2. **Agent 之间不直接通信**，所有流转通过 PM 中转
3. **测试专家发现问题报回 PM**，不直接修改代码
4. **验收不通过报回 PM**，由 PM 决定回退环节
5. **同一问题最多迭代 3 轮**

### 错误回退决策

```
验收不通过
├── 功能缺失？→ 回退到开发 / 需求分析
├── 功能错误？→ 回退到开发 / 技术方案
├── 质量不达标？→ 回退到开发 + 标注要求
└── 需求理解偏差？→ 回退到需求分析
```

---

## OpenSpec 规范驱动开发

[OpenSpec](https://openspec.pro) 是 AI 原生的规范驱动开发（SDD）框架，本系统将其与 Harness 多专家流程深度融合，实现"先定义规范，再生成代码"的最佳实践。

### 工作流映射

| OpenSpec 命令 | Harness 阶段 | 执行方式 |
|--------------|-------------|---------|
| `/opsx:propose "功能"` | 需求 + 技术方案 | 需求专家产出 proposal+specs，技术方案专家产出 design+tasks |
| `/opsx:apply` | 并行开发 | 前端+后端开发专家按 tasks.md 逐条实现 |
| `/opsx:explore` | 需求探索 | 纯思考探索，不写代码 |
| `/opsx:archive` | 归档 | 验收通过后归档变更 |

### OpenSpec 产物结构

```
openspec/changes/{feature-name}/
├── proposal.md    # 做什么、为什么（需求专家产出）
├── specs/         # 需求与验收场景（需求专家产出）
│   └── {capability}/spec.md
├── design.md      # 技术方案（技术方案专家产出）
└── tasks.md       # 实现任务清单（技术方案专家产出）
```

### 关键约束

- OpenSpec 产物由**对应专家**产出，不由 PM 直接写
- `/opsx:apply` 执行时**必须受架构边界约束控制**（前端只改前端目录，后端只改后端目录）
- 验收时对照 `specs/` 中的验收场景逐条验证

---

## 记忆驱动质量提升

本系统实现了三层记忆架构，确保项目质量持续提升而非反复踩坑。

### 三层记忆架构

| 层级 | 文件 | 加载时机 | 作用 |
|------|------|---------|------|
| 项目总览 | `CODEBUDDY.md` | 始终加载 | 全局架构和约束 |
| 子目录记忆 | `src/frontend/CODEBUDDY.md` | 操作前端时 | 前端架构、设计系统、Impeccable 红线 |
| 子目录记忆 | `src/backend/CODEBUDDY.md` | 操作后端时 | 后端架构、分层约束、安全规范 |
| 长期经验 | `.codebuddy/MEMORY.md` | 始终加载 | 经验沉淀、决策记录、错误转约束 |

### 记忆触发规则（熵治理）

| 事件 | 记忆动作 |
|------|---------|
| 验收不通过 | 记录失败原因 → 转化为未来约束 |
| 同一问题迭代 3 轮 | 记录问题模式 → 建议增加 Rule |
| 新技术选型 | 记录决策理由 → 供后续项目参考 |
| 性能/安全问题 | 记录根因 → 更新安全/编码规则 |
| Impeccable audit 发现反模式 | 记录反模式 → 更新设计红线 |

> **熵治理原则**：每次错误都是一次增强约束的机会。项目运行越久，约束越完善，质量越高。

---

## 5 条硬约束规则（Rules）

| 规则 | 应用方式 | 作用 |
|------|---------|------|
| `security-constraints` | **总是应用** | 安全硬约束：禁止硬编码密钥、SQL 拼接、未授权访问等 |
| `architecture-boundaries` | **总是应用** | 架构边界：前后端目录隔离、分层调用规则、接口契约一致性 |
| `agent-protocol` | 智能体请求 | Agent 间通信协议：结构化接口格式、任务流转规则 |
| `code-standards` | 智能体请求 | 编码规范：命名、注释、错误处理（Python + React/Vue） |
| `testing-standards` | 智能体请求 | 测试规范：分层策略、覆盖率要求、AAA 模式 |

### 安全约束亮点

- 禁止硬编码密钥/Token/密码
- 禁止 SQL 拼接（必须参数化查询或 ORM）
- 禁止 CORS 配置为 `*`（生产环境）
- 所有敏感操作必须有审计日志
- 所有用户输入必须校验和消毒

### 架构边界亮点

- **目录边界**：前端目录只有前端 Agent 可写，后端目录只有后端 Agent 可写
- **API 契约**：`project/api_specs/` 是前后端接口的唯一真相来源
- **后端分层**：API → Service → Repository → Model，禁止跨层调用
- **前端分层**：Pages → Components → Hooks → API Client，禁止组件中直接调 fetch

---

## 32 个技能包（Skills）

### 4 个 OpenSpec Skill

| Skill | 命令 | 作用 |
|-------|------|------|
| `openspec-propose` | `/opsx:propose` | 创建变更提案（proposal + specs + design + tasks） |
| `openspec-apply` | `/opsx:apply` | 按 tasks.md 逐条实现代码 |
| `openspec-explore` | `/opsx:explore` | 需求探索模式（不写代码） |
| `openspec-archive` | `/opsx:archive` | 归档已完成变更 |

### 7 个业务 Skill

| Skill | 关联 Agent | 职责 |
|-------|-----------|------|
| `requirement-analysis` | 需求专家 | 需求拆解工作流 + NFR 检查清单 |
| `tech-design` | 技术方案专家 | 技术方案工作流 + API 设计规范 + OpenAPI 3.0 |
| `frontend-dev` | 前端开发专家 | 前端开发工作流（集成 Impeccable）+ React/Vue 指南 |
| `backend-dev` | 后端开发专家 | 后端开发工作流（Python/FastAPI 分层架构）+ 初始化脚本 |
| `frontend-testing` | 前端测试专家 | 测试工作流 + React Testing Library / Vue Test Utils |
| `backend-testing` | 后端测试专家 | 测试工作流 + pytest + API 契约一致性验证 |
| `acceptance-test` | 功能验收专家 | 验收工作流 + 需求逐条验证 + 回退建议 |

### 21 个 Impeccable 设计 Skill

前端开发专家集成了 [Impeccable](https://impeccable.style) 设计技能体系，确保产出界面具有专业级设计质量：

| Skill | 触发时机 | 作用 |
|-------|---------|------|
| `impeccable` | 项目首次 | 建立设计上下文（teach）/ 完整构建流程（craft） |
| `shape` | 开发前 | 规划设计方向，产出设计简报 |
| `audit` | 开发后 | 5 维技术审计（A11y/性能/主题/响应式/反模式） |
| `critique` | 开发后 | UX 设计评审（启发式+认知负荷+情感） |
| `polish` | 发布前 | 最终质量打磨 |
| `arrange` | 按需 | 修复布局和间距 |
| `typeset` | 按需 | 修复排版 |
| `bolder` | 按需 | 增强视觉冲击 |
| `distill` | 按需 | 简化设计 |
| `normalize` | 按需 | 统一设计语言 |
| `harden` | 按需 | 增强鲁棒性 |
| 其他 10 个 | 按需 | clarify/adapt/animate/colorize/delight/extract/optimize/quieter/overdrive/onboard |

#### 设计红线（Impeccable absolute_bans）

⛔ **绝不使用**：侧边条纹边框、渐变文字、玻璃拟态泛滥、卡片嵌套、千篇一律的卡片网格、AI 默认字体（Inter/DM Sans/Syne）、纯黑 #000 或纯白 #fff

✅ **必须使用**：OKLCH 色彩空间、模块化字体比例（≥1.25）、4pt 间距刻度、语义化设计 token、container queries 优先

---

## 技术栈

| 层 | 技术 | 说明 |
|----|------|------|
| **前端** | React（优先）或 Vue | 由技术方案专家根据项目特征决定 |
| **后端** | Python 3 + FastAPI | 分层架构：API → Service → Repository → Model |
| **数据库** | PostgreSQL / SQLite | 生产用 PostgreSQL，轻量级用 SQLite |
| **API 契约** | OpenAPI 3.0 | `project/api_specs/` 为唯一真相来源 |
| **ORM** | SQLAlchemy 2.0 (async) | 异步数据库操作 |
| **数据校验** | Pydantic v2 | 请求/响应 Schema + 自动校验 |
| **测试（后端）** | pytest + httpx | 单元/API/集成测试 |
| **测试（前端）** | Vitest + Testing Library + Playwright | 组件/集成/E2E 测试 |
| **迁移** | Alembic | 数据库版本管理 |

---

## 目录结构

```
harness_engineering/
├── .codebuddy/
│   ├── agents/                         # 8 个 Agent 定义
│   │   ├── pm-orchestrator.md          # PM 专家（glm-5.1）
│   │   ├── requirement-expert.md       # 需求专家（glm-4.7）
│   │   ├── tech-architect.md           # 技术方案专家（glm-5.1）
│   │   ├── frontend-developer.md       # 前端开发专家（glm-4.7）
│   │   ├── backend-developer.md        # 后端开发专家（glm-4.7）
│   │   ├── frontend-tester.md          # 前端测试专家（glm-4.7）
│   │   ├── backend-tester.md           # 后端测试专家（glm-4.7）
│   │   └── acceptance-expert.md        # 功能验收专家（glm-4.7）
│   ├── commands/                        # OpenSpec 斜杠命令
│   │   └── opsx/                        # propose/apply/explore/archive
│   ├── rules/                          # 5 条硬约束规则
│   │   ├── security-constraints/       # 安全硬约束（总是应用）
│   │   ├── architecture-boundaries/    # 架构边界约束（总是应用）
│   │   ├── agent-protocol/             # Agent 通信协议
│   │   ├── code-standards/             # 编码规范
│   │   └── testing-standards/          # 测试规范
│   ├── skills/                         # 32 个技能包
│   │   ├── requirement-analysis/       # 需求分析 + NFR 检查清单
│   │   ├── tech-design/                # 技术方案 + API 设计规范
│   │   ├── frontend-dev/               # 前端开发 + React/Vue 指南
│   │   ├── backend-dev/                # 后端开发 + 初始化脚本
│   │   ├── frontend-testing/           # 前端测试
│   │   ├── backend-testing/            # 后端测试
│   │   ├── acceptance-test/            # 功能验收
│   │   ├── openspec-propose/           # OpenSpec 提案
│   │   ├── openspec-apply/             # OpenSpec 实现
│   │   ├── openspec-explore/           # OpenSpec 探索
│   │   ├── openspec-archive/           # OpenSpec 归档
│   │   ├── impeccable/                 # 核心设计 Skill + 8 个 reference
│   │   ├── shape/                      # 设计规划
│   │   ├── polish/                     # 最终打磨
│   │   ├── audit/                      # 技术质量审计
│   │   ├── critique/                   # UX 设计评审
│   │   └── ... (21 个 Impeccable Skill)
│   └── MEMORY.md                       # 长期经验记忆
├── openspec/                           # OpenSpec 规范驱动目录
│   └── changes/                        # 变更提案
├── project/                            # 运行时产出
│   ├── progress.json                   # 全局进度清单
│   ├── requirements/                   # 需求文档
│   ├── tech_design/                    # 技术方案
│   ├── api_specs/                      # OpenAPI 3.0 API 契约
│   ├── test_reports/                   # 测试报告
│   └── acceptance_reports/             # 验收报告
├── src/                                # 项目源代码
│   ├── frontend/                       # 前端代码（含 CODEBUDDY.md）
│   └── backend/                        # 后端代码（含 CODEBUDDY.md）
├── CODEBUDDY.md                        # 项目总览（始终加载）
├── LICENSE                             # MIT License
└── .gitignore
```

---

## 快速开始

### 前置条件

- [CodeBuddy](https://www.codebuddy.ai) IDE 插件（VS Code / Cursor）
- Node.js 18+（前端项目）
- Python 3.10+（后端项目）

### 使用方式

1. **克隆本仓库**
   ```bash
   git clone https://github.com/wuyilun/harness_engineering.git my-project
   cd my-project
   ```

2. **在 CodeBuddy 中打开项目**

   CodeBuddy 会自动加载 `.codebuddy/` 目录下的 Agent、Rules 和 Skills 配置。

3. **提交你的需求**

   在 CodeBuddy 对话框中直接描述你的需求，PM 专家会自动接管：

   **方式一：OpenSpec 规范驱动（推荐）**
   ```
   /opsx:propose add-user-management
   ```

   **方式二：直接描述需求**
   ```
   实现一个用户管理系统，支持注册、登录、个人资料编辑
   ```

4. **项目自动初始化**

   前端/后端开发专家在首次收到开发任务时，会自动检测并初始化项目骨架：

   - **前端**：自动执行 `init_project.sh`，创建 Vite + React/Vue + TypeScript 项目
   - **后端**：自动执行 `init_project.py`，创建 FastAPI + SQLAlchemy 项目骨架

   也可手动初始化：
   ```bash
   # 前端（React）
   bash .codebuddy/skills/frontend-dev/scripts/init_project.sh react src/frontend

   # 前端（Vue）
   bash .codebuddy/skills/frontend-dev/scripts/init_project.sh vue src/frontend

   # 后端
   python3 .codebuddy/skills/backend-dev/scripts/init_project.py src/backend
   ```

5. **观察自动化流程**

   PM 专家会自动拆解需求，按流程调度各专业 Agent：

   ```
   PM → 需求专家（产出需求文档）
      → 技术方案专家（产出技术方案 + API 契约）
      → 前端开发 + 后端开发（并行实现，自动初始化项目）
      → 前端测试 + 后端测试（并行验证）
      → 功能验收专家（逐条验收）
      → 交付
   ```

### 指令映射

| 你说 | PM 做 |
|------|-------|
| "实现 xxx 功能" | 完整流程：需求 → 方案 → 开发 → 测试 → 验收 |
| "只做需求分析" | 只派发需求专家 |
| "开始开发" | 从技术方案阶段继续 |
| "项目进度" | 读取 progress.json 汇报 |
| "验收" | 派发验收专家 |
| "修复 xxx 问题" | 判断归属，派发对应专家 |

---

## 自定义与扩展

### 替换模型

编辑 `.codebuddy/agents/` 下的 Agent 文件，修改 `model` 字段：

```yaml
---
name: pm-orchestrator
model: glm-5.1  # 改为你想要的模型
---
```

### 添加新规则

在 `.codebuddy/rules/` 下创建新目录，添加 `RULE.mdc` 文件：

```yaml
---
description: 你的规则描述
alwaysApply: true  # 或 false（智能体请求时加载）
enabled: true
---

# 规则内容
```

### 添加新技能

在 `.codebuddy/skills/` 下创建新目录，添加 `SKILL.md` 文件：

```yaml
---
name: your-skill
description: "Skill 描述"
---

# Skill 工作流内容
```

### 适配其他项目类型

- **纯后端项目**：删除前端相关 Agent 和 Skill，只保留 PM + 需求 + 技术方案 + 后端开发 + 后端测试 + 验收
- **纯前端项目**：删除后端相关 Agent 和 Skill，只保留 PM + 需求 + 技术方案 + 前端开发 + 前端测试 + 验收
- **小程序项目**：修改前端开发专家的技术栈约束，使用 UniApp/Taro

---

## 设计哲学

### 为什么硬约束 > 软约束？

传统做法是在 Prompt 里写"请遵守安全规范"，但 LLM 经常忽略。Harness 的做法是将约束编码为 Rules：

- **可执行**：Rules 在每次 Agent 运行时自动加载
- **可检测**：安全检查清单、反模式检测都是可度量的
- **可迭代**：发现新问题就添加新约束

### 为什么测试专家不修 Bug？

这是职责分离的核心——如果测试专家可以修改代码，就失去了测试的独立性。正确做法是：测试发现问题 → 报回 PM → PM 派发开发专家修复 → 测试专家重新验证。

### 为什么 API 契约是唯一真相来源？

前后端并行开发时，最大的风险是接口不一致。用 OpenAPI 3.0 定义契约，前端和后端都以此为唯一来源，任何变更必须先改契约再改实现。

---

## 致谢

- [CodeBuddy](https://www.codebuddy.ai) — AI 编程助手平台，提供 Agent/Rules/Skills/Memory 基础设施
- [OpenSpec](https://openspec.pro) — AI 原生规范驱动开发框架，由 [Fission AI](https://github.com/Fission-AI/OpenSpec) 创建
- [Impeccable](https://impeccable.style) — 专业级前端设计技能体系，由 [Paul Bakaus](https://github.com/pbakaus) 创建
- Harness Engineering 理念 — 用硬约束和结构化协议让 AI Agent 可靠协作

---

## License

[MIT](LICENSE) © 2026 Harness Engineering Contributors

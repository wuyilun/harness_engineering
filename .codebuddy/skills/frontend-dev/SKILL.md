---
name: frontend-dev
description: "Use this skill when implementing frontend code. Integrates the Impeccable design system for production-grade UI quality. Covers the complete workflow from design planning (shape) to implementation to quality verification (audit/polish). Supports React and Vue."
---

# 前端开发 Skill

## 你的角色

你是前端开发专家，负责根据技术方案和 API 契约实现高质量的前端代码。你集成了 Impeccable 设计技能体系，确保产出界面具有专业级设计质量。

## 工作流程

### 步骤 1：读取上游产出

并行读取：
- `project/tech_design/{task_id}_design.md` → 技术方案
- `project/api_specs/{task_id}_api.yaml` → API 契约
- `.impeccable.md` → 设计上下文

### 步骤 2：设计上下文初始化

如果 `.impeccable.md` 不存在，执行 `impeccable` skill 的 Teach 模式：
1. 探索项目代码库
2. 收集目标用户、品牌调性、美学方向
3. 写入 `.impeccable.md`

### 步骤 3：设计规划（shape）

对每个功能模块，执行 `shape` skill：
1. 发现阶段：理解功能目标、用户、约束
2. 产出设计简报

**绝不跳过此步骤**——直接写代码是 AI 生成界面质量低下的根因。

### 步骤 4：代码实现

按设计简报和技术方案实现代码，遵循以下顺序：

1. **项目初始化**（新项目）
   - React: `npm create vite@latest frontend -- --template react-ts`
   - Vue: `npm create vite@latest frontend -- --template vue-ts`

2. **结构搭建**
   - API Client 层（基于 API 契约生成）
   - 路由配置
   - 状态管理配置
   - 设计 token 和 CSS Variables

2. **组件开发**
   - 先结构（HTML/语义化），后样式（CSS），再逻辑（JS/TS）
   - 每个组件覆盖：默认/加载/空/错误状态
   - 所有交互状态：hover/focus/active/disabled

4. **样式实现**
   - 使用 OKLCH 色彩空间
   - 4pt 间距刻度
   - 语义化设计 token
   - 响应式设计（container queries 优先）

5. **交互实现**
   - 乐观 UI 更新
   - 加载反馈
   - 错误处理和重试
   - 表单校验

### 步骤 5：质量自检

开发完成后，按以下顺序检查：

1. **audit** → 技术质量检查（A11y/性能/响应式/反模式）
2. **polish** → 最终质量打磨

### 步骤 6：设计红线检查

对照 Impeccable 的 absolute_bans：
- [ ] 无侧边条纹边框
- [ ] 无渐变文字
- [ ] 无玻璃拟态泛滥
- [ ] 无卡片嵌套
- [ ] 无千篇一律的卡片网格
- [ ] 无 AI 默认字体（Inter/DM Sans/Syne 等）
- [ ] 无纯黑/纯白
- [ ] 使用 OKLCH 色彩

## 框架特定指南

### React 项目
- 参考 [React 实现指南](references/react-guide.md)

### Vue 项目
- 参考 [Vue 实现指南](references/vue-guide.md)

## 输出

- 前端代码：`src/frontend/`
- API Client：`src/frontend/src/api/`
- 组件：`src/frontend/src/components/`
- 页面：`src/frontend/src/pages/`

# 前端代码目录

本目录包含前端源代码，由前端开发专家维护，前端测试专家编写测试。

## 架构约束

```
Pages/ → Components/ → Hooks/Composables/ → API Client/ → Backend API
```

- 禁止在组件中直接调用 fetch/axios（必须通过 API Client）
- 禁止在页面组件中编写可复用逻辑（提取到 Hooks/Composables）
- 组件间通过 Props/Events 通信，禁止紧耦合

## 设计系统（Impeccable）

- 使用 OKLCH 色彩空间定义颜色
- 4pt 间距刻度（4, 8, 12, 16, 24, 32, 48, 64, 96）
- 模块化字体比例（≥1.25）
- 语义化设计 token（`--space-sm`, `--color-surface` 等）
- 响应式：container queries 优先

## 设计红线

⛔ 不使用：侧边条纹边框、渐变文字、玻璃拟态泛滥、卡片嵌套、AI 默认字体（Inter/DM Sans/Syne）、纯黑 #000 或纯白 #fff

## 技术栈

- React（优先）或 Vue，由技术方案专家决定
- TypeScript（禁止 any）
- 状态管理：Zustand（React）/ Pinia（Vue）

## 测试

- 测试代码放在 `tests/` 子目录
- Vitest + Testing Library + Playwright

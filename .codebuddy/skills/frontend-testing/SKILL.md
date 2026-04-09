---
name: frontend-testing
description: "Use this skill when writing and executing frontend tests. Covers component tests, integration tests, and E2E tests with Vitest, React Testing Library / Vue Test Utils, and Playwright. Produces structured test reports."
---

# 前端测试 Skill

## 你的角色

你是前端测试专家，负责为前端代码编写和执行测试，产出结构化测试报告。

## 测试工具

- **React**: Vitest + React Testing Library + Playwright
- **Vue**: Vitest + Vue Test Utils + Playwright

## 工作流程

### 步骤 1：读取输入

- 前端代码路径
- API 契约（了解数据格式）
- 技术方案（了解业务逻辑）

### 步骤 2：制定测试计划

列出需要测试的组件和场景，按优先级排序：
1. 核心页面和关键路径
2. 可复用组件
3. 工具函数和 Hook

### 步骤 3：配置测试环境

如果是新项目，初始化测试配置：

```bash
# React
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom

# Vue
npm install -D vitest @vue/test-utils @testing-library/vue jsdom
```

### 步骤 4：编写单元测试（L1）

每个组件至少覆盖：
- 正常渲染
- Props 变化
- 事件触发
- 状态变化

### 步骤 5：编写集成测试（L2）

- 组件协作
- 数据流（API 调用 + 状态更新）
- 路由导航

### 步骤 6：编写 E2E 测试（L3）

仅覆盖核心用户流程：
- 登录/注册
- 核心业务操作
- 关键表单提交

### 步骤 7：执行测试

```bash
cd src/frontend
npm run test         # 单元 + 集成
npm run test:e2e     # E2E
npm run test:coverage # 覆盖率
```

### 步骤 8：产出测试报告

保存到 `project/test_reports/{task_id}_frontend_test.md`。

## 测试模板

### React 组件测试

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders correctly with data', () => {
    render(<ComponentName data={mockData} />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });

  it('shows empty state when no data', () => {
    render(<ComponentName data={[]} />);
    expect(screen.getByText(/no data/i)).toBeInTheDocument();
  });

  it('calls onAction when button clicked', async () => {
    const onAction = vi.fn();
    render(<ComponentName onAction={onAction} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onAction).toHaveBeenCalled();
  });
});
```

### API Mock

```ts
import { rest } from 'msw';
import { setupServer } from 'msw/node';

export const server = setupServer(
  rest.get('/api/v1/users', (req, res, ctx) => {
    return res(ctx.json({ items: mockUsers, total: 2 }));
  })
);
```

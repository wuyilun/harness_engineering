# React 实现指南

## 项目结构

```
src/frontend/
├── public/
├── src/
│   ├── api/              # API Client
│   │   ├── client.ts     # axios/fetch 实例
│   │   ├── types.ts      # API 类型定义（从 OpenAPI 生成）
│   │   └── {entity}.ts   # 实体 API 方法
│   ├── components/       # 可复用组件
│   │   ├── ui/           # 基础 UI 组件
│   │   └── {Feature}/    # 功能组件
│   ├── hooks/            # 自定义 Hook
│   ├── pages/            # 页面组件
│   ├── stores/           # Zustand 状态管理
│   ├── styles/           # 全局样式和 token
│   │   ├── tokens.css    # 设计 token（颜色、间距、字体）
│   │   └── global.css    # 全局样式
│   ├── types/            # TypeScript 类型
│   ├── utils/            # 工具函数
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## 设计 Token 定义

```css
/* styles/tokens.css */
:root {
  /* 颜色 — OKLCH */
  --color-primary: oklch(0.7 0.15 250);
  --color-surface: oklch(0.98 0.005 250);
  --color-text: oklch(0.2 0.02 250);
  --color-text-muted: oklch(0.5 0.01 250);
  --color-border: oklch(0.85 0.01 250);

  /* 间距 — 4pt 刻度 */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* 字体 */
  --font-display: 'Display Font', serif;
  --font-body: 'Body Font', sans-serif;

  /* 字体大小 — 模块化比例 */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.563rem;
  --text-2xl: 1.953rem;
  --text-3xl: 2.441rem;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;

  /* 阴影 */
  --shadow-sm: 0 1px 2px oklch(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px oklch(0 0 0 / 0.07);
}
```

## 组件模板

```tsx
import styles from './ComponentName.module.css';
import type { ComponentNameProps } from './types';

export function ComponentName({ prop1, onAction }: ComponentNameProps) {
  return (
    <article className={styles.container}>
      {/* 内容 */}
    </article>
  );
}
```

## API Client 模板

```ts
import { apiClient } from './client';
import type { User, CreateUserRequest } from './types';

export const usersApi = {
  list: (params?: { page?: number; page_size?: number }) =>
    apiClient.get<UserListResponse>('/api/v1/users', { params }),

  get: (id: number) =>
    apiClient.get<User>(`/api/v1/users/${id}`),

  create: (data: CreateUserRequest) =>
    apiClient.post<User>('/api/v1/users', data),

  update: (id: number, data: Partial<CreateUserRequest>) =>
    apiClient.patch<User>(`/api/v1/users/${id}`, data),

  delete: (id: number) =>
    apiClient.delete(`/api/v1/users/${id}`),
};
```

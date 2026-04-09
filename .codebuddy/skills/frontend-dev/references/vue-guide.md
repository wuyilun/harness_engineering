# Vue 实现指南

## 项目结构

```
src/frontend/
├── public/
├── src/
│   ├── api/              # API Client
│   │   ├── client.ts     # axios/fetch 实例
│   │   ├── types.ts      # API 类型定义
│   │   └── {entity}.ts   # 实体 API 方法
│   ├── components/       # 可复用组件
│   │   ├── ui/           # 基础 UI 组件
│   │   └── {Feature}/    # 功能组件
│   ├── composables/      # 组合式函数
│   ├── views/            # 页面组件
│   ├── stores/           # Pinia 状态管理
│   ├── styles/           # 全局样式和 token
│   │   ├── tokens.css    # 设计 token
│   │   └── global.css    # 全局样式
│   ├── types/            # TypeScript 类型
│   ├── utils/            # 工具函数
│   ├── router/           # Vue Router
│   ├── App.vue
│   └── main.ts
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## 组件模板

```vue
<script setup lang="ts">
import styles from './ComponentName.module.css'

interface Props {
  prop1: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  action: [value: string]
}>()
</script>

<template>
  <article :class="styles.container">
    <!-- 内容 -->
  </article>
</template>
```

## Composable 模板

```ts
export function useEntity() {
  const data = ref<Entity | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchData(id: number) {
    loading.value = true
    error.value = null
    try {
      data.value = await entityApi.get(id)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, fetchData }
}
```

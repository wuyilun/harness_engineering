#!/usr/bin/env bash
# 前端项目初始化脚本 - 创建 React/Vue 项目骨架
# 用法: bash scripts/init_project.sh [react|vue] [target_dir]
# 默认: react src/frontend

set -e

FRAMEWORK="${1:-react}"
TARGET_DIR="${2:-src/frontend}"

echo "🚀 Initializing frontend project ($FRAMEWORK) at $TARGET_DIR..."

# 检查 node 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# 检查目标目录是否已有项目
if [ -f "$TARGET_DIR/package.json" ]; then
    echo "⚠️  Frontend project already exists at $TARGET_DIR, skipping init."
    exit 0
fi

# 创建目录
mkdir -p "$TARGET_DIR"

# 用 Vite 创建项目
if [ "$FRAMEWORK" = "vue" ]; then
    npx create-vite@latest "$TARGET_DIR" --template vue-ts 2>/dev/null
else
    npx create-vite@latest "$TARGET_DIR" --template react-ts 2>/dev/null
fi

cd "$TARGET_DIR"

# 安装基础依赖
npm install

# 安装项目常用依赖
if [ "$FRAMEWORK" = "vue" ]; then
    npm install pinia vue-router@4 axios
    npm install -D @vue/test-utils vitest @testing-library/vue
else
    npm install zustand react-router-dom axios
    npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
fi

# 创建标准目录结构
mkdir -p src/api
mkdir -p src/components
mkdir -p src/pages
mkdir -p src/hooks
mkdir -p src/styles
mkdir -p src/types
mkdir -p src/utils
mkdir -p tests

# 创建 API Client 模板
cat > src/api/client.ts << 'EOF'
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
EOF

# 创建设计 Token 基础
cat > src/styles/tokens.css << 'EOF'
/* Design Tokens - OKLCH Color Space */
:root {
  /* Colors - OKLCH */
  --color-primary: oklch(0.6 0.2 260);
  --color-primary-hover: oklch(0.55 0.22 260);
  --color-surface: oklch(0.98 0.005 260);
  --color-surface-raised: oklch(1.0 0.005 260);
  --color-text: oklch(0.25 0.02 260);
  --color-text-secondary: oklch(0.5 0.02 260);
  --color-border: oklch(0.88 0.01 260);
  --color-error: oklch(0.6 0.22 25);
  --color-success: oklch(0.6 0.2 145);

  /* Spacing - 4pt scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;
  --space-24: 96px;

  /* Typography - Modular Scale (1.25) */
  --font-size-xs: 0.64rem;
  --font-size-sm: 0.8rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.563rem;
  --font-size-2xl: 1.953rem;
  --font-size-3xl: 2.441rem;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
}
EOF

# 创建环境变量模板
cat > .env.example << 'EOF'
VITE_API_BASE_URL=http://localhost:8000/api/v1
EOF

cat > .env.local << 'EOF'
VITE_API_BASE_URL=http://localhost:8000/api/v1
EOF

# 创建 vitest 配置
cat > vitest.config.ts << 'EOF'
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test-setup.ts',
    css: true,
  },
});
EOF

cat > src/test-setup.ts << 'EOF'
import '@testing-library/jest-dom';
EOF

echo ""
echo "✅ Frontend project ($FRAMEWORK) initialized at $TARGET_DIR"
echo "   Run 'cd $TARGET_DIR && npm run dev' to start dev server"

# Frontend Rules Templates

> ⚠️ **注意**: 这些是前端开发规则模板，实际规则应根据具体项目技术栈创建。

## 技术栈检测

这些规则模板通过路径自动匹配项目类型：

| 技术栈 | 检测路径 |
|--------|---------|
| Vue | `**/*.vue` |
| React | `**/*.tsx`, `**/*.jsx` |
| Angular | `**/*.component.ts` |
| Svelte | `**/*.svelte` |

## 通用前端最佳实践

### 1. 组件拆分策略

按职责拆分组件，保持单一职责原则：

| 类型 | 目录 | 说明 |
|------|-------|------|
| 通用组件 | `components/common/` | 可复用的 UI 组件 |
| 业务组件 | `components/` | 特定业务逻辑组件 |
| 页面组件 | `pages/` 或 `views/` | 页面级别容器 |
| 布局组件 | `components/layout/` | 布局相关组件 |

### 2. 状态管理

使用适当的状态管理方案：

```typescript
// ✅ 正确：组件内部状态
const count = ref(0)
const doubleCount = computed(() => count.value * 2)

// ✅ 正确：跨组件状态（Pinia/Redux/Zustand）
const userStore = useUserStore()
```

### 3. TypeScript 类型安全

为所有 props、emits、函数添加类型定义：

```typescript
// ✅ 正确：完整的类型定义
interface Props {
  userId: number
  userName: string
  isActive?: boolean
}

const props = defineProps<Props>()
```

### 4. API 调用规范

统一 API 调用层，避免组件直接处理数据请求：

```typescript
// ✅ 正确：Service 层
export const userService = {
  getUser: (id: number) => api.get(`/users/${id}`),
  updateUser: (data: User) => api.put(`/users/${data.id}`, data),
}

// ❌ 错误：组件内直接请求
const response = await fetch(`/api/users/${id}`)
```

### 5. 响应式数据

使用框架的响应式系统：

```typescript
// ✅ 正确：Vue 响应式
const data = ref<T>(initialValue)
const computedData = computed(() => transform(data.value))

// ❌ 错误：直接操作 DOM
document.querySelector('.title').innerHTML = value
```

## 目录结构规范

推荐的前端目录结构：

```
src/
├── components/       # 组件（通用 + 业务）
├── pages/           # 页面（路由级别组件）
├── views/           # 视图（可替代 pages/）
├── stores/          # 状态管理
├── services/        # API 调用
├── utils/          # 通用函数
├── types/           # 类型定义
├── styles/          # 全局样式
└── router/          # 路由配置
```

## 代码风格

### 命名约定

| 类型 | 约定 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `UserCard.vue` |
| 工具函数 | camelCase | `formatDate.ts` |
| 常量 | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| CSS 类 | kebab-case | `user-card` |

### 组件规范

```vue
<!-- ✅ 正确：使用 script setup -->
<script setup lang="ts">
interface Props {
  title: string
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})

const emit = defineEmits<{
  update: [count: number]
}>()
</script>
```

## 安全最佳实践

### XSS防护

```typescript
// ✅ 正确：内容转义
<div v-html="sanitize(userContent)"></div>

// ❌ 错误：直接插入 HTML
<div innerHTML="<script>alert('xss')</script>"></div>
```

### 敏感数据

```typescript
// ✅ 正确：不在 localStorage 存储敏感信息
localStorage.setItem('theme', 'dark')  // 仅非敏感数据

// ❌ 错误：存储敏感信息
localStorage.setItem('token', userToken)
localStorage.setItem('password', password)
```

---

## 📈 合规统计

此文件为模板，合规统计应在实际项目中追踪。

_最后更新: 2026-04-30_

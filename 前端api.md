# AI 数字人视频定制平台 - 前端 API 设计文档

## 一、前端技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| 框架 | Vue 3.4+ | 组合式 API + TypeScript |
| 构建 | Vite 5.0+ | 快速构建工具 |
| UI 组件库 | Element Plus / Ant Design Vue | PC 端 UI |
| 状态管理 | Pinia | Vue 3 推荐状态管理 |
| 路由 | Vue Router 4.2+ | 官方路由 |
| HTTP 客户端 | Axios | 请求库 |
| 工具库 | Lodash / Day.js | 常用工具 |
| 富文本编辑器 | Quill / TinyMCE | 文案编辑器 |
| 视频播放 | Video.js / Plyr | 视频播放器 |
| WebSocket | Socket.io-client | 实时通信 |
| 文件上传 | Axios + OSS SDK | 文件上传 |
| 图表 | ECharts | 数据可视化 |

---

## 二、前端项目结构

```
src/
├── api/                    # API 接口层
│   ├── index.ts           # API 入口配置
│   ├── request.ts         # Axios 封装
│   ├── modules/           # 业务模块 API
│   │   ├── user.ts        # 用户相关
│   │   ├── auth.ts        # 认证相关
│   │   ├── digital-human.ts
│   │   ├── script.ts
│   │   ├── asset.ts
│   │   ├── video.ts
│   │   ├── wallet.ts
│   │   ├── notification.ts
│   │   └── admin.ts
│   └── types/             # TypeScript 类型定义
├── assets/                # 静态资源
│   ├── images/
│   ├── styles/
│   └── fonts/
├── components/            # 通用组件
│   ├── common/            # 通用组件
│   │   ├── Button.vue
│   │   ├── Input.vue
│   │   ├── Modal.vue
│   │   └── Upload.vue
│   ├── business/          # 业务组件
│   │   ├── DigitalHumanPreview.vue
│   │   ├── ScriptEditor.vue
│   │   ├── VideoPlayer.vue
│   │   ├── TimelineEditor.vue
│   │   └── AssetPicker.vue
│   └── layout/            # 布局组件
│       ├── Header.vue
│       ├── Sidebar.vue
│       └── Footer.vue
├── composables/           # 组合式函数
│   ├── useAuth.ts        # 认证相关
│   ├── useUser.ts        # 用户信息
│   ├── useDigitalHuman.ts
│   ├── useScript.ts
│   ├── useVideo.ts
│   ├── useWebSocket.ts   # WebSocket 连接
│   └── useUpload.ts      # 文件上传
├── layouts/              # 页面布局
│   ├── DefaultLayout.vue
│   ├── EmptyLayout.vue
│   └── AdminLayout.vue
├── pages/                # 页面
│   ├── auth/             # 认证页面
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   └── ForgotPassword.vue
│   ├── user/             # 个人中心
│   │   ├── Profile.vue
│   │   ├── Membership.vue
│   │   ├── Wallet.vue
│   │   ├── Devices.vue
│   │   └── Notifications.vue
│   ├── digital-human/    # 数字人管理
│   │   ├── List.vue
│   │   ├── Create.vue
│   │   └── Detail.vue
│   ├── script/           # 脚本管理
│   │   ├── List.vue
│   │   ├── Create.vue
│   │   ├── Edit.vue
│   │   └── Templates.vue
│   ├── asset/            # 素材库
│   │   ├── MyAssets.vue
│   │   ├── PlatformAssets.vue
│   │   └── Upload.vue
│   ├── video/            # 视频项目
│   │   ├── List.vue
│   │   ├── Create.vue
│   │   ├── Detail.vue
│   │   └── Output.vue
│   ├── admin/            # 管理后台
│   │   ├── Users.vue
│   │   ├── Reviews.vue
│   │   ├── Statistics.vue
│   │   └── Settings.vue
│   └── home/             # 首页
│       └── Index.vue
├── router/               # 路由配置
│   └── index.ts
├── stores/               # Pinia 状态管理
│   ├── user.ts
│   ├── digitalHuman.ts
│   ├── script.ts
│   ├── asset.ts
│   ├── video.ts
│   └── notification.ts
├── utils/                # 工具函数
│   ├── request.ts
│   ├── storage.ts
│   ├── validate.ts
│   └── format.ts
├── hooks/                # 自定义 Hooks
│   └── use.ts
├── App.vue
└── main.ts
```

---

## 三、核心模块前端实现

### 3.1 认证模块

#### 3.1.1 API 层 (api/auth.ts)

```typescript
import request from '@/api/request'
import type {
  LoginParams,
  SmsCodeParams,
  LoginResponse,
  RefreshTokenParams,
  RefreshTokenResponse
} from '@/api/types/auth'

/**
 * 发送短信验证码
 */
export function sendSmsCode(params: SmsCodeParams) {
  return request.post<{ expire_seconds: number; retry_after: number }>(
    '/auth/sms/send',
    params
  )
}

/**
 * 手机号验证码登录/注册
 */
export function loginBySms(params: LoginParams) {
  return request.post<LoginResponse>('/auth/login/sms', params)
}

/**
 * 密码登录
 */
export function loginByPassword(params: {
  account: string
  password: string
  device_id: string
  device_type: string
  user_agent: string
}) {
  return request.post<LoginResponse>('/auth/login/password', params)
}

/**
 * OAuth 登录
 */
export function loginByOAuth(params: {
  provider: 'wechat' | 'google' | 'apple'
  code: string
  state: string
  device_id: string
  device_type: string
}) {
  return request.post<LoginResponse>('/auth/login/oauth', params)
}

/**
 * 刷新 Token
 */
export function refreshToken(params: RefreshTokenParams) {
  return request.post<RefreshTokenResponse>('/auth/refresh', params)
}

/**
 * 登出
 */
export function logout() {
  return request.post('/auth/logout')
}
```

---

#### 3.1.2 Composable (composables/useAuth.ts)

```typescript
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  sendSmsCode,
  loginBySms,
  loginByPassword,
  loginByOAuth,
  refreshToken,
  logout
} from '@/api/auth'
import type { LoginParams, SmsCodeParams } from '@/api/types/auth'

export function useAuth() {
  const router = useRouter()
  const userStore = useUserStore()

  const loading = ref(false)
  const error = ref<string | null>(null)

  // 发送验证码
  const sendCode = async (params: SmsCodeParams) => {
    loading.value = true
    error.value = null

    try {
      const res = await sendSmsCode(params)
      loading.value = false
      return res.data
    } catch (err: any) {
      error.value = err.message
      loading.value = false
      throw err
    }
  }

  // 登录
  const doLogin = async (params: LoginParams) => {
    loading.value = true
    error.value = null

    try {
      const res = await loginBySms(params)

      // 保存 token
      userStore.setTokens({
        access_token: res.data.tokens.access_token,
        refresh_token: res.data.tokens.refresh_token,
        expires_in: res.data.tokens.expires_in
      })

      // 保存用户信息
      userStore.setUser(res.data.user)

      // 初始化 WebSocket
      userStore.initWebSocket()

      loading.value = false

      // 跳转到首页或重定向
      const redirect = router.currentRoute.value.query.redirect as string
      router.push(redirect || '/')

      return res.data
    } catch (err: any) {
      error.value = err.message
      loading.value = false
      throw err
    }
  }

  // 登出
  const doLogout = async () => {
    try {
      await logout()
    } catch (err) {
      console.error('登出失败:', err)
    } finally {
      userStore.clearAuth()
      router.push('/login')
    }
  }

  // 检查登录状态
  const isLoggedIn = computed(() => !!userStore.user?.id)

  return {
    loading,
    error,
    isLoggedIn,
    sendCode,
    doLogin,
    doLogout
  }
}
```

---

#### 3.1.3 Store (stores/user.ts)

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getUserProfile } from '@/api/user'
import type { User, Tokens } from '@/api/types/user'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const tokens = ref<Tokens | null>(null)
  const ws = ref<WebSocket | null>(null)

  // 设置 Token
  const setTokens = (newTokens: Tokens) => {
    tokens.value = newTokens
    localStorage.setItem('access_token', newTokens.access_token)
    localStorage.setItem('refresh_token', newTokens.refresh_token)
    localStorage.setItem('expires_at', String(Date.now() + newTokens.expires_in * 1000))
  }

  // 清除认证信息
  const clearAuth = () => {
    user.value = null
    tokens.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('expires_at')

    // 关闭 WebSocket
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
  }

  // 设置用户信息
  const setUser = (userData: User) => {
    user.value = userData
  }

  // 获取用户信息
  const fetchUserProfile = async () => {
    try {
      const res = await getUserProfile()
      user.value = res.data
      return res.data
    } catch (err) {
      clearAuth()
      throw err
    }
  }

  // 初始化 WebSocket
  const initWebSocket = () => {
    if (ws.value?.readyState === WebSocket.OPEN) {
      return
    }

    const token = localStorage.getItem('access_token')
    if (!token) {
      return
    }

    const wsUrl = `${import.meta.env.VITE_WS_BASE_URL}/ws/v1/stream?token=${token}`
    ws.value = new WebSocket(wsUrl)

    ws.value.onopen = () => {
      console.log('WebSocket 已连接')
      // 启动心跳
      startHeartbeat()
    }

    ws.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        handleWsMessage(data)
      } catch (err) {
        console.error('WebSocket 消息解析失败:', err)
      }
    }

    ws.value.onerror = (err) => {
      console.error('WebSocket 错误:', err)
    }

    ws.value.onclose = () => {
      console.log('WebSocket 已关闭')
      stopHeartbeat()
      // 5秒后重连
      setTimeout(() => {
        initWebSocket()
      }, 5000)
    }
  }

  // 心跳
  let heartbeatInterval: number | null = null
  const startHeartbeat = () => {
    heartbeatInterval = window.setInterval(() => {
      if (ws.value?.readyState === WebSocket.OPEN) {
        ws.value.send(JSON.stringify({ type: 'ping' }))
      }
    }, 30000)
  }

  const stopHeartbeat = () => {
    if (heartbeatInterval) {
      clearInterval(heartbeatInterval)
      heartbeatInterval = null
    }
  }

  // 处理 WebSocket 消息
  const handleWsMessage = (data: any) => {
    switch (data.type) {
      case 'task_progress':
        // 任务进度更新
        break
      case 'task_completed':
        // 任务完成
        break
      case 'task_failed':
        // 任务失败
        break
      case 'notification':
        // 消息通知
        break
      case 'pong':
        // 心跳响应
        break
    }
  }

  // Computed
  const isLoggedIn = computed(() => !!user.value?.id)
  const isVIP = computed(() => user.value?.membership_type !== 'free')
  const membershipType = computed(() => user.value?.membership_type || 'free')
  const quota = computed(() => user.value?.quota)

  return {
    user,
    tokens,
    ws,
    isLoggedIn,
    isVIP,
    membershipType,
    quota,
    setTokens,
    clearAuth,
    setUser,
    fetchUserProfile,
    initWebSocket
  }
})
```

---

### 3.2 数字人管理模块

#### 3.2.1 API 层 (api/digital-human.ts)

```typescript
import request from '@/api/request'
import type {
  DigitalHumanListParams,
  DigitalHumanListResponse,
  DigitalHumanCreateParams,
  DigitalHumanDetailResponse,
  TaskStatusResponse
} from '@/api/types/digital-human'

/**
 * 获取数字人列表
 */
export function getDigitalHumanList(params?: DigitalHumanListParams) {
  return request.get<DigitalHumanListResponse>('/digital-humans', { params })
}

/**
 * 获取数字人详情
 */
export function getDigitalHumanDetail(id: number) {
  return request.get<DigitalHumanDetailResponse>(`/digital-humans/${id}`)
}

/**
 * 获取上传凭证
 */
export function getUploadToken(params: { file_count: number; file_size_mb: number }) {
  return request.post<{
    upload_token: string
    upload_url: string
    expire_seconds: number
    file_prefix: string
  }>('/upload/digital-human-photos/token', params)
}

/**
 * 创建数字人
 */
export function createDigitalHuman(params: DigitalHumanCreateParams) {
  return request.post<{ id: number; task_id: number; estimated_seconds: number }>(
    '/digital-humans',
    params
  )
}

/**
 * 更新数字人
 */
export function updateDigitalHuman(id: number, params: Partial<DigitalHumanCreateParams>) {
  return request.patch(`/digital-humans/${id}`, params)
}

/**
 * 重新生成数字人
 */
export function regenerateDigitalHuman(id: number, params: { new_photos: any[] }) {
  return request.post(`/digital-humans/${id}/regenerate`, params)
}

/**
 * 设置默认数字人
 */
export function setDefaultDigitalHuman(id: number) {
  return request.post(`/digital-humans/${id}/set-default`)
}

/**
 * 删除数字人
 */
export function deleteDigitalHuman(id: number, params?: { delete_related_videos?: boolean }) {
  return request.delete(`/digital-humans/${id}`, { params })
}

/**
 * 获取任务状态
 */
export function getTaskStatus(taskId: number) {
  return request.get<TaskStatusResponse>(`/digital-humans/tasks/${taskId}`)
}
```

---

#### 3.2.2 Composable (composables/useDigitalHuman.ts)

```typescript
import { ref, computed } from 'vue'
import {
  getDigitalHumanList,
  getDigitalHumanDetail,
  createDigitalHuman,
  updateDigitalHuman,
  deleteDigitalHuman,
  setDefaultDigitalHuman,
  getTaskStatus
} from '@/api/digital-human'
import type { DigitalHuman, DigitalHumanListParams } from '@/api/types/digital-human'

export function useDigitalHuman() {
  const list = ref<DigitalHuman[]>([])
  const detail = ref<DigitalHuman | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({
    page: 1,
    page_size: 20,
    total: 0
  })

  // 获取列表
  const fetchList = async (params?: DigitalHumanListParams) => {
    loading.value = true
    error.value = null

    try {
      const res = await getDigitalHumanList({
        page: pagination.value.page,
        page_size: pagination.value.page_size,
        ...params
      })

      list.value = res.data.items
      pagination.value = {
        page: res.data.pagination.page,
        page_size: res.data.pagination.page_size,
        total: res.data.pagination.total
      }

      loading.value = false
      return res.data
    } catch (err: any) {
      error.value = err.message
      loading.value = false
      throw err
    }
  }

  // 获取详情
  const fetchDetail = async (id: number) => {
    loading.value = true
    error.value = null

    try {
      const res = await getDigitalHumanDetail(id)
      detail.value = res.data
      loading.value = false
      return res.data
    } catch (err: any) {
      error.value = err.message
      loading.value = false
      throw err
    }
  }

  // 创建
  const create = async (params: any) => {
    loading.value = true
    error.value = null

    try {
      const res = await createDigitalHuman(params)
      loading.value = false
      return res.data
    } catch (err: any) {
      error.value = err.message
      loading.value = false
      throw err
    }
  }

  // 更新
  const update = async (id: number, params: any) => {
    loading.value = true
    error.value = null

    try {
      const res = await updateDigitalHuman(id, params)
      loading.value = false
      return res.data
    } catch (err: any) {
      error.value = err.message
      loading.value = false
      throw err
    }
  }

  // 设置默认
  const setDefault = async (id: number) => {
    try {
      await setDefaultDigitalHuman(id)
      // 更新列表中的默认状态
      list.value.forEach((item) => {
        item.is_default = item.id === id
      })
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  // 删除
  const remove = async (id: number, params?: { delete_related_videos?: boolean }) => {
    loading.value = true
    error.value = null

    try {
      await deleteDigitalHuman(id, params)
      list.value = list.value.filter((item) => item.id !== id)
      loading.value = false
    } catch (err: any) {
      error.value = err.message
      loading.value = false
      throw err
    }
  }

  // Computed
  const readyDigitalHumans = computed(() =>
    list.value.filter((item) => item.status === 'ready')
  )
  const defaultDigitalHuman = computed(() =>
    list.value.find((item) => item.is_default) || readyDigitalHumans.value[0]
  )

  return {
    list,
    detail,
    readyDigitalHumans,
    defaultDigitalHuman,
    loading,
    error,
    pagination,
    fetchList,
    fetchDetail,
    create,
    update,
    setDefault,
    remove
  }
}
```

---

#### 3.2.3 组件示例 (components/business/DigitalHumanPreview.vue)

```vue
<template>
  <div class="digital-human-preview">
    <div class="preview-container">
      <video
        v-if="digitalHuman.preview_video_url"
        ref="videoRef"
        class="preview-video"
        :src="digitalHuman.preview_video_url"
        autoplay
        loop
        muted
        playsinline
      />
      <img
        v-else
        class="preview-image"
        :src="digitalHuman.preview_image_url"
        :alt="digitalHuman.name"
      />
    </div>

    <div class="preview-info">
      <h3 class="name">{{ digitalHuman.name }}</h3>
      <p v-if="digitalHuman.description" class="description">
        {{ digitalHuman.description }}
      </p>

      <div class="stats">
        <span class="stat">使用次数: {{ digitalHuman.usage_count }}</span>
        <el-tag v-if="digitalHuman.is_default" type="primary" size="small">
          默认
        </el-tag>
      </div>

      <div v-if="digitalHuman.status === 'processing'" class="progress">
        <el-progress
          :percentage="digitalHuman.progress || 0"
          :format="(p) => `生成中 ${p}%`"
        />
        <span class="time-remaining">
          预计剩余: {{ formatTime(digitalHuman.estimated_remaining_seconds) }}
        </span>
      </div>
    </div>

    <div class="preview-actions">
      <el-button v-if="!digitalHuman.is_default" @click="handleSetDefault">
        设为默认
      </el-button>
      <el-button @click="handleEdit">编辑</el-button>
      <el-button type="danger" @click="handleDelete">删除</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { DigitalHuman } from '@/api/types/digital-human'

interface Props {
  digitalHuman: DigitalHuman
}

const props = defineProps<Props>()
const emit = defineEmits<{
  setDefault: [id: number]
  edit: [id: number]
  delete: [id: number]
}>()

const videoRef = ref<HTMLVideoElement>()

// 格式化时间
const formatTime = (seconds?: number) => {
  if (!seconds) return '--'
  if (seconds < 60) return `${seconds}秒`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}分钟${seconds % 60}秒`
  return `${Math.floor(seconds / 3600)}小时${Math.floor((seconds % 3600) / 60)}分钟`
}

// 设为默认
const handleSetDefault = () => {
  emit('setDefault', props.digitalHuman.id)
  ElMessage.success('已设为默认数字人')
}

// 编辑
const handleEdit = () => {
  emit('edit', props.digitalHuman.id)
}

// 删除
const handleDelete = () => {
  ElMessageBox.confirm(
    '确定要删除这个数字人吗？删除后30天内可恢复。',
    '确认删除',
    {
      type: 'warning'
    }
  ).then(() => {
    emit('delete', props.digitalHuman.id)
    ElMessage.success('删除成功')
  })
}
</script>

<style scoped lang="scss">
.digital-human-preview {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}

.preview-container {
  width: 100%;
  aspect-ratio: 16/9;
  background: #f5f7fa;
  border-radius: 4px;
  overflow: hidden;

  .preview-video,
  .preview-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.preview-info {
  margin-top: 12px;

  .name {
    margin: 0 0 8px;
    font-size: 16px;
    font-weight: 500;
  }

  .description {
    margin: 0 0 12px;
    color: #606266;
    font-size: 14px;
  }

  .stats {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;

    .stat {
      font-size: 12px;
      color: #909399;
    }
  }

  .progress {
    margin-top: 8px;

    .time-remaining {
      display: block;
      margin-top: 4px;
      font-size: 12px;
      color: #909399;
    }
  }
}

.preview-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}
</style>
```

---

### 3.3 脚本管理模块

#### 3.3.1 API 层 (api/script.ts)

```typescript
import request from '@/api/request'
import type {
  ScriptListParams,
  ScriptListResponse,
  ScriptDetailResponse,
  ScriptCreateParams,
  AiWritingParams,
  AiWritingResponse
} from '@/api/types/script'

/**
 * 获取脚本列表
 */
export function getScriptList(params?: ScriptListParams) {
  return request.get<ScriptListResponse>('/scripts', { params })
}

/**
 * 获取脚本详情
 */
export function getScriptDetail(id: number) {
  return request.get<ScriptDetailResponse>(`/scripts/${id}`)
}

/**
 * 创建脚本
 */
export function createScript(params: ScriptCreateParams) {
  return request.post<{ id: number; word_count: number; estimated_duration: number }>(
    '/scripts',
    params
  )
}

/**
 * 更新脚本
 */
export function updateScript(id: number, params: Partial<ScriptCreateParams>) {
  return request.patch(`/scripts/${id}`, params)
}

/**
 * 删除脚本
 */
export function deleteScript(id: number) {
  return request.delete(`/scripts/${id}`)
}

/**
 * 保存为模板
 */
export function saveAsTemplate(id: number, params: { name: string; description?: string }) {
  return request.post(`/scripts/${id}/save-as-template`, params)
}

/**
 * AI 生成文案
 */
export function aiGenerateText(params: AiWritingParams) {
  return request.post<AiWritingResponse>('/ai-writing/generate', params)
}

/**
 * AI 改写/润色
 */
export function aiRewriteText(params: {
  text: string
  task_type: 'rewrite' | 'polish' | 'expand' | 'shrink' | 'translate'
  style?: string
  target_language?: string
}) {
  return request.post<AiWritingResponse>('/ai-writing/rewrite', params)
}

/**
 * 获取 AI 任务状态
 */
export function getAiWritingTaskStatus(taskId: number) {
  return request.get(`/ai-writing/tasks/${taskId}`)
}

/**
 * 获取模板列表
 */
export function getTemplateList(params?: {
  category?: string
  page?: number
  page_size?: number
}) {
  return request.get('/script-templates', { params })
}
```

---

#### 3.3.2 脚本编辑器组件 (components/business/ScriptEditor.vue)

```vue
<template>
  <div class="script-editor">
    <div class="editor-header">
      <el-input
        v-model="script.title"
        placeholder="请输入脚本标题"
        size="large"
        clearable
      />
      <el-select v-model="script.language" placeholder="语言">
        <el-option label="中文" value="zh" />
        <el-option label="英文" value="en" />
        <el-option label="日文" value="ja" />
      </el-select>
    </div>

    <div class="editor-content">
      <!-- 段落列表 -->
      <div class="segments-list">
        <div
          v-for="(segment, index) in script.content.segments"
          :key="index"
          class="segment-item"
          :class="{ 'is-active': activeSegmentIndex === index }"
          @click="activeSegmentIndex = index"
        >
          <div class="segment-header">
            <span class="segment-index">段落 {{ index + 1 }}</span>
            <el-button
              type="text"
              :icon="Delete"
              @click.stop="removeSegment(index)"
            />
          </div>
          <el-input
            v-model="segment.text"
            type="textarea"
            :rows="3"
            placeholder="请输入段落内容"
          />

          <!-- 段落配置 -->
          <div class="segment-config">
            <div class="config-item">
              <label>语速</label>
              <el-slider
                v-model="segment.speed"
                :min="0.5"
                :max="2.0"
                :step="0.1"
                :format-tooltip="formatSpeed"
              />
            </div>
            <div class="config-item">
              <label>停顿</label>
              <el-select
                v-model="segment.pause_after"
                placeholder="停顿时间"
              >
                <el-option label="无" :value="0" />
                <el-option label="0.5秒" :value="0.5" />
                <el-option label="1秒" :value="1" />
                <el-option label="2秒" :value="2" />
                <el-option label="自定义" :value="null" />
              </el-select>
            </div>
            <div class="config-item">
              <label>情感</label>
              <el-select v-model="segment.emotion" placeholder="情感">
                <el-option label="平静" value="neutral" />
                <el-option label="开心" value="happy" />
                <el-option label="严肃" value="serious" />
                <el-option label="幽默" value="humorous" />
              </el-select>
            </div>
          </div>

          <div class="segment-info">
            <span>时长: {{ formatDuration(segment.duration) }}</span>
          </div>
        </div>

        <el-button
          type="primary"
          :icon="Plus"
          @click="addSegment"
          style="width: 100%"
        >
          添加段落
        </el-button>
      </div>

      <!-- 预览区 -->
      <div class="preview-panel">
        <div class="preview-header">
          <h4>预览</h4>
          <el-button type="text" @click="handlePreview">播放预览</el-button>
        </div>
        <div class="preview-content">
          <div
            v-for="(segment, index) in script.content.segments"
            :key="index"
            class="preview-segment"
          >
            {{ segment.text }}
          </div>
        </div>
        <div class="preview-stats">
          <div>字数: {{ totalWords }}</div>
          <div>预估时长: {{ formatDuration(totalDuration) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Delete, Plus } from '@element-plus/icons-vue'
import type { Script } from '@/api/types/script'

interface Props {
  modelValue: Script
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: Script]
}>()

const script = ref<Script>({ ...props.modelValue })
const activeSegmentIndex = ref(0)
const audioRef = ref<HTMLAudioElement>()

// 监听变化
watch(
  script,
  () => {
    emit('update:modelValue', script.value)
    calculateDurations()
  },
  { deep: true }
)

// 计算时长
const calculateDurations = () => {
  script.value.content.segments.forEach((segment) => {
    const wordCount = segment.text.length
    const wordsPerSecond = 3 * segment.speed
    segment.duration = Math.ceil(wordCount / wordsPerSecond)
  })
}

// 添加段落
const addSegment = () => {
  script.value.content.segments.push({
    id: Date.now(),
    text: '',
    speed: 1.0,
    pause_after: 0.5,
    emotion: 'neutral',
    duration: 0
  })
}

// 删除段落
const removeSegment = (index: number) => {
  script.value.content.segments.splice(index, 1)
  if (activeSegmentIndex.value >= script.value.content.segments.length) {
    activeSegmentIndex.value = script.value.content.segments.length - 1
  }
}

// 格式化时长
const formatDuration = (seconds: number) => {
  if (seconds < 60) return `${seconds}秒`
  return `${Math.floor(seconds / 60)}分${seconds % 60}秒`
}

// 格式化语速
const formatSpeed = (value: number) => `${value}x`

// 总字数
const totalWords = computed(() => {
  return script.value.content.segments.reduce((sum, seg) => sum + seg.text.length, 0)
})

// 总时长
const totalDuration = computed(() => {
  return script.value.content.segments.reduce((sum, seg) => sum + (seg.duration || 0), 0)
})

// 播放预览
const handlePreview = () => {
  // 实现 TTS 预览
}
</script>

<style scoped lang="scss">
.script-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.editor-header {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.editor-content {
  display: flex;
  gap: 24px;
  flex: 1;
  min-height: 0;
}

.segments-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
}

.segment-item {
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    border-color: #409eff;
  }

  &.is-active {
    border-color: #409eff;
    background: #ecf5ff;
  }
}

.segment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  .segment-index {
    font-weight: 500;
    color: #409eff;
  }
}

.segment-config {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin: 12px 0;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;

  .config-item {
    display: flex;
    flex-direction: column;
    gap: 4px;

    label {
      font-size: 12px;
      color: #606266;
    }
  }
}

.segment-info {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.preview-panel {
  width: 320px;
  display: flex;
  flex-direction: column;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e4e7ed;

  h4 {
    margin: 0;
  }
}

.preview-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;

  .preview-segment {
    padding: 8px 0;
    border-bottom: 1px dashed #e4e7ed;
    line-height: 1.6;
  }
}

.preview-stats {
  padding: 12px 16px;
  border-top: 1px solid #e4e7ed;
  background: #f5f7fa;
  border-radius: 0 0 8px 8px;

  div {
    font-size: 12px;
    color: #606266;
    margin-bottom: 4px;

    &:last-child {
      margin-bottom: 0;
    }
  }
}
</style>
```

---

### 3.4 视频生成模块

#### 3.4.1 API 层 (api/video.ts)

```typescript
import request from '@/api/request'
import type {
  VideoProjectListParams,
  VideoProjectListResponse,
  VideoProjectDetailResponse,
  VideoProjectCreateParams,
  GenerationTaskResponse
} from '@/api/types/video'

/**
 * 获取视频项目列表
 */
export function getVideoProjectList(params?: VideoProjectListParams) {
  return request.get<VideoProjectListResponse>('/video-projects', { params })
}

/**
 * 获取项目详情
 */
export function getVideoProjectDetail(id: number) {
  return request.get<VideoProjectDetailResponse>(`/video-projects/${id}`)
}

/**
 * 创建项目
 */
export function createVideoProject(params: VideoProjectCreateParams) {
  return request.post<{ id: number; status: string; estimated_cost_cents: number }>(
    '/video-projects',
    params
  )
}

/**
 * 更新项目
 */
export function updateVideoProject(id: number, params: Partial<VideoProjectCreateParams>) {
  return request.patch(`/video-projects/${id}`, params)
}

/**
 * 提交生成
 */
export function submitVideoGeneration(id: number, params?: {
  priority?: number
  skip_queue?: boolean
}) {
  return request.post<{
    project_id: number
    task_id: number
    status: string
    queue_position?: number
    estimated_seconds: number
  }>(`/video-projects/${id}/generate`, params)
}

/**
 * 取消生成
 */
export function cancelVideoGeneration(id: number) {
  return request.post(`/video-projects/${id}/cancel`)
}

/**
 * 获取任务状态
 */
export function getGenerationTaskStatus(taskId: number) {
  return request.get<GenerationTaskResponse>(`/generation-tasks/${taskId}`)
}

/**
 * 获取视频输出
 */
export function getVideoOutput(projectId: number) {
  return request.get(`/video-projects/${projectId}/output`)
}

/**
 * 下载视频
 */
export function downloadVideo(outputId: number) {
  return request.get(`/video-outputs/${outputId}/download`, {
    responseType: 'blob'
  })
}

/**
 * 创建分享链接
 */
export function createVideoShare(outputId: number, params: {
  expire_hours: number
  enable_password?: boolean
  password?: string
}) {
  return request.post<{ share_url: string; share_token: string; expire_at: string }>(
    `/video-outputs/${outputId}/share`,
    params
  )
}

/**
 * 删除项目
 */
export function deleteVideoProject(id: number) {
  return request.delete(`/video-projects/${id}`)
}
```

---

#### 3.4.2 视频项目创建页面 (pages/video/Create.vue)

```vue
<template>
  <div class="create-video-project">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <h2 class="page-title">新建视频项目</h2>
      </template>
    </el-page-header>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="project-form"
    >
      <!-- 基本信息配置 -->
      <el-card class="form-section" header="基本配置">
        <el-form-item label="项目名称" prop="project_name">
          <el-input
            v-model="form.project_name"
            placeholder="请输入项目名称"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="视频模式" prop="mode">
          <el-radio-group v-model="form.mode">
            <el-radio-button label="simple">简易模式</el-radio-button>
            <el-radio-button label="professional">专业模式</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="分辨率" prop="resolution">
          <el-select v-model="form.resolution" placeholder="请选择分辨率">
            <el-option label="720p" value="720p" />
            <el-option label="1080p" value="1080p" />
            <el-option label="2K" value="2k" :disabled="!isVIP" />
            <el-option label="4K" value="4k" :disabled="!isPro" />
          </el-select>
        </el-form-item>

        <el-form-item label="宽高比" prop="aspect_ratio">
          <el-select v-model="form.aspect_ratio" placeholder="请选择宽高比">
            <el-option label="16:9 (横屏)" value="16:9" />
            <el-option label="9:16 (竖屏)" value="9:16" />
            <el-option label="1:1 (方形)" value="1:1" />
          </el-select>
        </el-form-item>
      </el-card>

      <!-- 简易模式配置 -->
      <template v-if="form.mode === 'simple'">
        <el-card class="form-section" header="选择数字人">
          <el-form-item label="数字人" prop="digital_human_id" required>
            <el-select
              v-model="form.digital_human_id"
              placeholder="请选择数字人"
              filterable
            >
              <el-option
                v-for="dh in readyDigitalHumans"
                :key="dh.id"
                :label="dh.name"
                :value="dh.id"
              >
                <div class="digital-human-option">
                  <img
                    :src="dh.preview_image_url"
                    class="option-avatar"
                    alt=""
                  />
                  <span class="option-name">{{ dh.name }}</span>
                  <el-tag v-if="dh.is_default" size="small">默认</el-tag>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
        </el-card>

        <el-card class="form-section" header="选择脚本">
          <el-form-item label="脚本" prop="script_id" required>
            <el-select
              v-model="form.script_id"
              placeholder="请选择脚本"
              filterable
            >
              <el-option
                v-for="script in scripts"
                :key="script.id"
                :label="script.title"
                :value="script.id"
              />
            </el-select>
          </el-form-item>

          <el-button
            type="primary"
            link
            @click="showCreateScript = true"
          >
            新建脚本
          </el-button>
        </el-card>

        <el-card class="form-section" header="选择素材">
          <el-form-item label="背景" prop="background_asset_id">
            <el-select
              v-model="form.background_type"
              placeholder="背景类型"
              style="width: 120px; margin-right: 8px"
            >
              <el-option label="图片" value="image" />
              <el-option label="视频" value="video" />
              <el-option label="纯色" value="color" />
            </el-select>

            <el-select
              v-if="form.background_type !== 'color'"
              v-model="form.background_asset_id"
              placeholder="选择背景"
              filterable
              style="width: calc(100% - 128px)"
            >
              <el-option
                v-for="asset in backgrounds"
                :key="asset.id"
                :label="asset.name"
                :value="asset.id"
              >
                <div class="asset-option">
                  <img
                    :src="asset.thumbnail_url || asset.file_url"
                    class="option-thumb"
                    alt=""
                  />
                  <span>{{ asset.name }}</span>
                </div>
              </el-option>
            </el-select>

            <el-color-picker
              v-else
              v-model="form.background_value"
              :predefine="predefineColors"
            />
          </el-form-item>

          <el-form-item label="背景音乐" prop="bgm_asset_id">
            <el-select
              v-model="form.bgm_asset_id"
              placeholder="选择背景音乐（可选）"
              clearable
              filterable
            >
              <el-option
                v-for="bgm in bgms"
                :key="bgm.id"
                :label="bgm.name"
                :value="bgm.id"
              />
            </el-select>

            <el-slider
              v-if="form.bgm_asset_id"
              v-model="form.bgm_volume"
              :min="0"
              :max="1"
              :step="0.1"
              :format-tooltip="(v) => `${v * 100}%`"
              style="width: 200px; margin-left: 16px"
            />
          </el-form-item>

          <el-button
            type="primary"
            link
            @click="showAssetPicker = 'background'"
          >
            上传背景素材
          </el-button>
        </el-card>
      </template>

      <!-- 专业模式配置 -->
      <template v-else>
        <el-card class="form-section" header="时间线配置">
          <timeline-editor
            v-model="form.timeline_config"
            :digital-humans="readyDigitalHumans"
            :assets="allAssets"
          />
        </el-card>

        <el-card class="form-section" header="字幕配置">
          <subtitle-config
            v-model="form.subtitle_config"
          />
        </el-card>
      </template>

      <!-- 预估信息 -->
      <el-card class="form-section" header="预估信息">
        <div class="estimate-info">
          <div class="info-item">
            <span class="label">预估时长：</span>
            <span class="value">{{ estimatedDuration }}</span>
          </div>
          <div class="info-item">
            <span class="label">预估成本：</span>
            <span class="value">{{ estimatedCost }}</span>
          </div>
          <div class="info-item">
            <span class="label">预估时间：</span>
            <span class="value">{{ estimatedTime }}</span>
          </div>
        </div>
      </el-card>

      <!-- 操作按钮 -->
      <div class="form-actions">
        <el-button @click="goBack">取消</el-button>
        <el-button
          type="primary"
          :loading="creating"
          @click="handleCreateProject"
        >
          保存为草稿
        </el-button>
        <el-button
          type="success"
          :loading="submitting"
          @click="handleSubmitProject"
        >
          提交生成
        </el-button>
      </div>
    </el-form>

    <!-- 新建脚本对话框 -->
    <create-script-dialog
      v-model="showCreateScript"
      @created="handleScriptCreated"
    />

    <!-- 素材选择器 -->
    <asset-picker
      v-model:visible="showAssetPickerDialog"
      :type="showAssetPicker"
      @select="handleAssetSelect"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { useDigitalHuman } from '@/composables/useDigitalHuman'
import { useScript } from '@/composables/useScript'
import { useAsset } from '@/composables/useAsset'
import { createVideoProject, submitVideoGeneration } from '@/api/video'
import TimelineEditor from '@/components/business/TimelineEditor.vue'
import SubtitleConfig from '@/components/business/SubtitleConfig.vue'
import CreateScriptDialog from '@/components/business/CreateScriptDialog.vue'
import AssetPicker from '@/components/business/AssetPicker.vue'

const router = useRouter()
const userStore = useUserStore()
const { readyDigitalHumans } = useDigitalHuman()
const { scripts, fetchScriptList } = useScript()
const { backgrounds, bgms, allAssets, fetchAssetList } = useAsset()

const formRef = ref()
const form = ref({
  project_name: '',
  mode: 'simple',
  resolution: '1080p',
  aspect_ratio: '16:9',
  digital_human_id: null as number | null,
  script_id: null as number | null,
  background_type: 'image',
  background_asset_id: null as number | null,
  background_value: '#ffffff',
  bgm_asset_id: null as number | null,
  bgm_volume: 0.3,
  timeline_config: null,
  subtitle_config: null
})

const rules = {
  project_name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' }
  ],
  digital_human_id: [
    { required: true, message: '请选择数字人', trigger: 'change' }
  ],
  script_id: [
    { required: true, message: '请选择脚本', trigger: 'change' }
  ]
}

const creating = ref(false)
const submitting = ref(false)
const showCreateScript = ref(false)
const showAssetPicker = ref('')
const showAssetPickerDialog = ref(false)

// 预定义颜色
const predefineColors = [
  '#ffffff', '#000000', '#409eff', '#67c23a',
  '#e6a23c', '#f56c6c', '#909399', '#c71585'
]

// 会员级别
const isVIP = computed(() => userStore.isVIP)
const isPro = computed(() => userStore.membershipType === 'pro')

// 预估时长
const estimatedDuration = computed(() => {
  const script = scripts.value.find(s => s.id === form.value.script_id)
  return script?.estimated_duration
    ? formatDuration(script.estimated_duration)
    : '--'
})

// 预估成本
const estimatedCost = computed(() => {
  const basePrice = 30
  const resolutionMultiplier = {
    '720p': 1,
    '1080p': 1.5,
    '2k': 2.5,
    '4k': 4
  }
  return `${(basePrice * (resolutionMultiplier[form.value.resolution as keyof typeof resolutionMultiplier] || 1)).toFixed(2)}元`
})

// 预估时间
const estimatedTime = computed(() => {
  const script = scripts.value.find(s => s.id === form.value.script_id)
  const duration = script?.estimated_duration || 0
  const minutes = Math.ceil(duration / 60)
  return `约 ${minutes * 2}-${minutes * 5} 分钟`
})

// 格式化时长
const formatDuration = (seconds: number) => {
  if (seconds < 60) return `${seconds}秒`
  return `${Math.floor(seconds / 60)}分${seconds % 60}秒`
}

// 返回
const goBack = () => {
  router.back()
}

// 创建项目
const handleCreateProject = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  creating.value = true
  try {
    await createVideoProject(form.value)
    ElMessage.success('草稿已保存')
    router.push('/video')
  } catch (err: any) {
    ElMessage.error(err.message || '创建失败')
  } finally {
    creating.value = false
  }
}

// 提交项目
const handleSubmitProject = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const projectRes = await createVideoProject(form.value)
    const taskRes = await submitVideoGeneration(projectRes.data.id)

    ElMessage.success('任务已提交，正在生成中')
    router.push(`/video/${projectRes.data.id}`)
  } catch (err: any) {
    if (err.response?.data?.code === 30001) {
      ElMessage.error('配额不足，请升级会员或充值')
    } else {
      ElMessage.error(err.message || '提交失败')
    }
  } finally {
    submitting.value = false
  }
}

// 脚本创建完成
const handleScriptCreated = (scriptId: number) => {
  form.value.script_id = scriptId
  fetchScriptList()
}

// 素材选择
const handleAssetSelect = (asset: any) => {
  if (showAssetPicker.value === 'background') {
    form.value.background_asset_id = asset.id
  }
  showAssetPickerDialog.value = false
}

// 初始化
onMounted(() => {
  fetchScriptList()
  fetchAssetList()
})
</script>

<style scoped lang="scss">
.create-video-project {
  padding: 24px;
}

.page-title {
  margin: 0;
  font-size: 20px;
}

.form-section {
  margin-bottom: 24px;
}

.digital-human-option {
  display: flex;
  align-items: center;
  gap: 8px;

  .option-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
  }
}

.asset-option {
  display: flex;
  align-items: center;
  gap: 8px;

  .option-thumb {
    width: 40px;
    height: 40px;
    border-radius: 4px;
    object-fit: cover;
  }
}

.estimate-info {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;

  .info-item {
    display: flex;
    justify-content: space-between;
    padding: 12px;
    background: #f5f7fa;
    border-radius: 4px;

    .label {
      color: #606266;
    }

    .value {
      font-weight: 500;
      color: #409eff;
    }
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}
</style>
```

---

### 3.5 实时进度监控组件

```vue
<template>
  <div class="generation-progress">
    <div class="progress-header">
      <div class="task-info">
        <h3>视频生成中</h3>
        <span class="task-id">任务 #{{ taskId }}</span>
      </div>
      <el-tag :type="taskTagType">{{ taskStatusText }}</el-tag>
    </div>

    <div class="progress-content">
      <div class="progress-main">
        <el-progress
          :percentage="progress"
          :status="progressStatus"
          :stroke-width="8"
        />
        <div class="progress-text">
          <span>{{ progress }}%</span>
          <span v-if="queuePosition > 0">
            排队位置: {{ queuePosition }}
          </span>
        </div>
      </div>

      <div v-if="taskStatus === 'processing'" class="progress-step">
        <div class="step-label">当前步骤:</div>
        <div class="step-value">{{ currentStep }}</div>
      </div>

      <div class="progress-estimate">
        <div>预计剩余: {{ formatTime(estimatedSeconds) }}</div>
        <div>已耗时: {{ formatTime(elapsedSeconds) }}</div>
      </div>
    </div>

    <div class="progress-actions">
      <el-button
        v-if="canCancel"
        type="danger"
        @click="handleCancel"
      >
        取消任务
      </el-button>
      <el-button
        v-else
        @click="handleViewOutput"
      >
        查看视频
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getGenerationTaskStatus } from '@/api/video'
import { useUserStore } from '@/stores/user'

interface Props {
  taskId: number
  projectId: number
}

const props = defineProps<Props>()

const userStore = useUserStore()

const progress = ref(0)
const taskStatus = ref<'queued' | 'processing' | 'completed' | 'failed'>('queued')
const currentStep = ref('')
const queuePosition = ref(0)
const estimatedSeconds = ref(0)
const elapsedSeconds = ref(0)

const startTime = ref(Date.now())
let timer: number | null = null
let wsSubscription: (() => void) | null = null

// 任务状态文本
const taskStatusText = computed(() => {
  const statusMap = {
    queued: '排队中',
    processing: '生成中',
    completed: '已完成',
    failed: '失败'
  }
  return statusMap[taskStatus.value]
})

// 任务标签类型
const taskTagType = computed(() => {
  const typeMap = {
    queued: 'info',
    processing: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return typeMap[taskStatus.value]
})

// 进度状态
const progressStatus = computed(() => {
  if (taskStatus.value === 'completed') return 'success'
  if (taskStatus.value === 'failed') return 'exception'
  return undefined
})

// 是否可以取消
const canCancel = computed(() => {
  return ['queued', 'processing'].includes(taskStatus.value)
})

// 格式化时间
const formatTime = (seconds: number) => {
  if (seconds < 60) return `${seconds}秒`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}分${seconds % 60}秒`
  return `${Math.floor(seconds / 3600)}小时${Math.floor((seconds % 3600) / 60)}分钟`
}

// 获取任务状态
const fetchTaskStatus = async () => {
  try {
    const res = await getGenerationTaskStatus(props.taskId)
    const data = res.data

    progress.value = data.progress || 0
    taskStatus.value = data.status
    currentStep.value = data.current_step || ''
    queuePosition.value = data.queue_position || 0
    estimatedSeconds.value = data.estimated_seconds || 0

    if (data.started_at) {
      elapsedSeconds.value = Math.floor((Date.now() - new Date(data.started_at).getTime()) / 1000)
    }

    if (taskStatus.value === 'completed' || taskStatus.value === 'failed') {
      stopTimer()
      if (taskStatus.value === 'completed') {
        ElMessage.success('视频生成完成!')
      }
    }
  } catch (err) {
    console.error('获取任务状态失败:', err)
  }
}

// WebSocket 订阅
const subscribeWebSocket = () => {
  const handleMessage = (data: any) => {
    if (data.data.task_id === props.taskId) {
      switch (data.type) {
        case 'task_progress':
          progress.value = data.data.progress
          currentStep.value = data.data.current_step
          estimatedSeconds.value = data.data.estimated_seconds
          break
        case 'task_completed':
          progress.value = 100
          taskStatus.value = 'completed'
          ElMessage.success('视频生成完成!')
          stopTimer()
          break
        case 'task_failed':
          taskStatus.value = 'failed'
          ElMessage.error(data.data.error_message || '视频生成失败')
          stopTimer()
          break
      }
    }
  }

  userStore.$onAction(({ name, args, after }) => {
    if (name === 'handleWsMessage') {
      after(() => {
        handleMessage(args[0])
      })
    }
  })

  wsSubscription = () => {
    userStore.$offAction('handleWsMessage')
  }
}

// 取消任务
const handleCancel = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要取消这个任务吗？已使用的时间将不退还。',
      '确认取消',
      { type: 'warning' }
    )

    await cancelVideoGeneration(props.projectId)
    ElMessage.success('任务已取消')
  } catch (err) {
    // 用户取消
  }
}

// 查看视频
const handleViewOutput = () => {
  router.push(`/video/${props.projectId}/output`)
}

// 启动定时器
const startTimer = () => {
  timer = window.setInterval(async () => {
    await fetchTaskStatus()
    elapsedSeconds.value = Math.floor((Date.now() - startTime.value) / 1000)
  }, 3000)
}

// 停止定时器
const stopTimer = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

onMounted(() => {
  fetchTaskStatus()
  startTimer()
  subscribeWebSocket()
})

onUnmounted(() => {
  stopTimer()
  wsSubscription?.()
})
</script>
```

---

## 四、状态管理

### 4.1 数字人 Store (stores/digitalHuman.ts)

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getDigitalHumanList, getDigitalHumanDetail } from '@/api/digital-human'
import type { DigitalHuman } from '@/api/types/digital-human'

export const useDigitalHumanStore = defineStore('digitalHuman', () => {
  const list = ref<DigitalHuman[]>([])
  const loading = ref(false)

  // 获取列表
  const fetchList = async (params?: { status?: string }) => {
    loading.value = true
    try {
      const res = await getDigitalHumanList(params)
      list.value = res.data.items
      loading.value = false
    } catch (err) {
      loading.value = false
      throw err
    }
  }

  // 添加到列表
  const addToList = (digitalHuman: DigitalHuman) => {
    list.value.unshift(digitalHuman)
  }

  // 从列表中移除
  const removeFromList = (id: number) => {
    const index = list.value.findIndex((item) => item.id === id)
    if (index > -1) {
      list.value.splice(index, 1)
    }
  }

  // 更新列表项
  const updateListItem = (id: number, updates: Partial<DigitalHuman>) => {
    const index = list.value.findIndex((item) => item.id === id)
    if (index > -1) {
      list.value[index] = { ...list.value[index], ...updates }
    }
  }

  // Computed
  const readyDigitalHumans = computed(() =>
    list.value.filter((item) => item.status === 'ready')
  )
  const defaultDigitalHuman = computed(() =>
    list.value.find((item) => item.is_default) || readyDigitalHumans.value[0]
  )
  const processingCount = computed(() =>
    list.value.filter((item) => item.status === 'processing').length
  )

  return {
    list,
    loading,
    readyDigitalHumans,
    defaultDigitalHuman,
    processingCount,
    fetchList,
    addToList,
    removeFromList,
    updateListItem
  }
})
```

---

## 五、路由配置

### 5.1 路由文件 (router/index.ts)

```typescript
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/auth/Login.vue'),
    meta: { guest: true, layout: 'empty' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/pages/auth/Register.vue'),
    meta: { guest: true, layout: 'empty' }
  },
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    meta: { auth: true },
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/pages/home/Index.vue')
      },
      {
        path: '/user',
        name: 'User',
        redirect: '/user/profile'
      },
      {
        path: '/user/profile',
        name: 'UserProfile',
        component: () => import('@/pages/user/Profile.vue')
      },
      {
        path: '/user/membership',
        name: 'UserMembership',
        component: () => import('@/pages/user/Membership.vue')
      },
      {
        path: '/user/wallet',
        name: 'UserWallet',
        component: () => import('@/pages/user/Wallet.vue')
      },
      {
        path: '/digital-human',
        name: 'DigitalHuman',
        redirect: '/digital-human/list'
      },
      {
        path: '/digital-human/list',
        name: 'DigitalHumanList',
        component: () => import('@/pages/digital-human/List.vue')
      },
      {
        path: '/digital-human/create',
        name: 'DigitalHumanCreate',
        component: () => import('@/pages/digital-human/Create.vue')
      },
      {
        path: '/digital-human/:id',
        name: 'DigitalHumanDetail',
        component: () => import('@/pages/digital-human/Detail.vue')
      },
      {
        path: '/script',
        name: 'Script',
        redirect: '/script/list'
      },
      {
        path: '/script/list',
        name: 'ScriptList',
        component: () => import('@/pages/script/List.vue')
      },
      {
        path: '/script/create',
        name: 'ScriptCreate',
        component: () => import('@/pages/script/Create.vue')
      },
      {
        path: '/script/edit/:id',
        name: 'ScriptEdit',
        component: () => import('@/pages/script/Edit.vue')
      },
      {
        path: '/video',
        name: 'Video',
        redirect: '/video/list'
      },
      {
        path: '/video/list',
        name: 'VideoList',
        component: () => import('@/pages/video/List.vue')
      },
      {
        path: '/video/create',
        name: 'VideoCreate',
        component: () => import('@/pages/video/Create.vue')
      },
      {
        path: '/video/:id',
        name: 'VideoDetail',
        component: () => import('@/pages/video/Detail.vue')
      },
      {
        path: '/video/:id/output',
        name: 'VideoOutput',
        component: () => import('@/pages/video/Output.vue')
      }
    ]
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { auth: true, admin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/pages/admin/Dashboard.vue')
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/pages/admin/Users.vue')
      },
      {
        path: 'reviews',
        name: 'AdminReviews',
        component: () => import('@/pages/admin/Reviews.vue')
      },
      {
        path: 'statistics',
        name: 'AdminStatistics',
        component: () => import('@/pages/admin/Statistics.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 需要登录
  if (to.meta.auth && !userStore.isLoggedIn) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // 游客页面
  if (to.meta.guest && userStore.isLoggedIn) {
    next({ path: '/' })
    return
  }

  // 需要管理员权限
  if (to.meta.admin && !userStore.user?.is_admin) {
    next({ path: '/' })
    return
  }

  next()
})

export default router
```

---

## 六、API 请求封装

### 6.1 Axios 配置 (api/request.ts)

```typescript
import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

// 创建 axios 实例
const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 添加 token
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 添加请求 ID
    config.headers['X-Request-ID'] = generateRequestId()

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const res = response.data

    // 业务成功
    if (res.code === 0) {
      return response
    }

    // 业务错误
    ElMessage.error(res.message || '请求失败')
    return Promise.reject(new Error(res.message || '请求失败'))
  },
  (error: AxiosError) => {
    const userStore = useUserStore()

    // 401 未授权
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        userStore.refreshToken(refreshToken)
      } else {
        userStore.clearAuth()
        window.location.href = '/login'
      }
      return Promise.reject(error)
    }

    // 403 无权限
    if (error.response?.status === 403) {
      ElMessage.error('无权限访问')
      return Promise.reject(error)
    }

    // 404 不存在
    if (error.response?.status === 404) {
      ElMessage.error('请求的资源不存在')
      return Promise.reject(error)
    }

    // 429 请求过多
    if (error.response?.status === 429) {
      ElMessage.error('请求频率过高，请稍后再试')
      return Promise.reject(error)
    }

    // 500 服务器错误
    if (error.response?.status >= 500) {
      ElMessage.error('服务器错误，请稍后再试')
      return Promise.reject(error)
    }

    // 网络错误
    if (!error.response) {
      ElMessage.error('网络连接失败，请检查网络')
      return Promise.reject(error)
    }

    // 其他错误
    const message = error.response?.data?.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(new Error(message))
  }
)

// 生成请求 ID
function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

export default request
```

---

## 七、环境变量配置

### 7.1 环境变量 (.env.development)

```bash
# API 地址
VITE_API_BASE_URL=http://localhost:8080/api/v1
VITE_WS_BASE_URL=ws://localhost:8080

# OSS 配置
VITE_OSS_REGION=oss-cn-hangzhou
VITE_OSS_BUCKET=your-bucket
VITE_OSS_ACCESS_KEY_ID=your-access-key-id
VITE_OSS_ACCESS_KEY_SECRET=your-access-key-secret
VITE_OSS_CDN_DOMAIN=https://cdn.example.com

# 应用配置
VITE_APP_TITLE=AI数字人视频平台
VITE_APP_VERSION=1.0.0
```

---

### 7.2 环境变量 (.env.production)

```bash
# API 地址
VITE_API_BASE_URL=https://api.example.com/api/v1
VITE_WS_BASE_URL=wss://api.example.com

# OSS 配置
VITE_OSS_REGION=oss-cn-hangzhou
VITE_OSS_BUCKET=your-bucket
VITE_OSS_ACCESS_KEY_ID=your-access-key-id
VITE_OSS_ACCESS_KEY_SECRET=your-access-key-secret
VITE_OSS_CDN_DOMAIN=https://cdn.example.com

# 应用配置
VITE_APP_TITLE=AI数字人视频平台
VITE_APP_VERSION=1.0.0
```

---

## 八、Vue 组件规范

### 8.1 组件命名

- 单文件组件使用 PascalCase
- 组件文件名与组件名一致
- 业务组件放在 `components/business/`
- 通用组件放在 `components/common/`

### 8.2 Props 定义

```typescript
interface Props {
  digitalHuman: DigitalHuman
  editable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  editable: false
})
```

### 8.3 Emits 定义

```typescript
const emit = defineEmits<{
  update: [value: any]
  delete: [id: number]
}>()
```

### 8.4 组合式函数

使用 `use` 前缀命名，如 `useAuth`, `useDigitalHuman`, `useVideo`

---

## 九、前端构建优化

### 9.1 Vite 配置优化

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  build: {
    target: 'es2015',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    },
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'element-plus': ['element-plus'],
          'editor': ['@vueup/vue-quill']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
})
```

### 9.2 性能优化建议

1. 路由懒加载
2. 图片懒加载
3. 长列表虚拟滚动
4. 防抖节流
5. 缓存策略
6. CDN 加速

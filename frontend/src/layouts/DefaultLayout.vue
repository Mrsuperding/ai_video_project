<template>
  <div class="default-layout">
    <header class="header">
      <div class="header-left">
        <h1 class="logo">AI 数字人视频平台</h1>
        <nav class="nav">
          <router-link to="/">首页</router-link>
          <router-link to="/digital-human">数字人</router-link>
          <router-link to="/script">脚本</router-link>
          <router-link to="/asset">素材</router-link>
          <router-link to="/video">视频</router-link>
        </nav>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-avatar :src="userStore.avatar" />
            <span>{{ userStore.nickname || '用户' }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="membership">会员中心</el-dropdown-item>
              <el-dropdown-item command="wallet">我的钱包</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { logout } from '@/api/modules/auth'

const router = useRouter()
const userStore = useUserStore()

const handleCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/user/profile')
      break
    case 'membership':
      router.push('/user/membership')
      break
    case 'wallet':
      router.push('/user/wallet')
      break
    case 'logout':
      await logout()
      localStorage.removeItem('token')
      router.push('/auth/login')
      break
  }
}
</script>

<style scoped lang="scss">
.default-layout {
  min-height: 100vh;
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 24px;
    height: 60px;
    background: #fff;
    border-bottom: 1px solid #e4e7ed;
    .header-left {
      display: flex;
      align-items: center;
      gap: 40px;
      .logo {
        font-size: 18px;
        font-weight: 600;
        color: #409EFF;
      }
      .nav {
        display: flex;
        gap: 24px;
        a {
          color: #606266;
          text-decoration: none;
          &.router-link-active {
            color: #409EFF;
          }
        }
      }
    }
    .header-right {
      .user-info {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
      }
    }
  }
  .main {
    padding: 24px;
  }
}
</style>
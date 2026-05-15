<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="logo">管理后台</div>
      <nav class="nav">
        <router-link to="/admin">数据概览</router-link>
        <router-link to="/admin/users">用户管理</router-link>
        <router-link to="/admin/reviews">内容审核</router-link>
        <router-link to="/admin/statistics">数据统计</router-link>
        <router-link to="/admin/settings">系统设置</router-link>
      </nav>
    </aside>
    <div class="content">
      <header class="header">
        <span class="admin-name">管理员</span>
        <el-button size="small" @click="handleLogout">退出</el-button>
      </header>
      <main class="main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const handleLogout = () => {
  localStorage.removeItem('admin_token')
  router.push('/auth/login')
}
</script>

<style scoped lang="scss">
.admin-layout {
  display: flex;
  min-height: 100vh;
  .sidebar {
    width: 220px;
    background: #304156;
    .logo {
      padding: 20px;
      color: #fff;
      font-size: 16px;
      font-weight: 600;
      text-align: center;
    }
    .nav {
      display: flex;
      flex-direction: column;
      padding: 8px 0;
      a {
        padding: 14px 24px;
        color: #bfcbd9;
        text-decoration: none;
        &:hover, &.router-link-active {
          background: #263445;
          color: #409EFF;
        }
      }
    }
  }
  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
    .header {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      padding: 0 24px;
      height: 60px;
      background: #fff;
      border-bottom: 1px solid #e4e7ed;
    }
    .main {
      padding: 24px;
      background: #f0f2f5;
    }
  }
}
</style>
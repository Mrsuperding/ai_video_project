<template>
  <div class="admin-dashboard">
    <el-row :gutter="16" class="stats">
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <span class="label">用户总数</span>
            <span class="value">12,580</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <span class="label">今日新增</span>
            <span class="value">156</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <span class="label">视频项目</span>
            <span class="value">8,420</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <span class="label">收入(元)</span>
            <span class="value">125,680</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 24px;">
      <el-col :span="12">
        <el-card>
          <template #header>最近活跃用户</template>
          <el-table :data="recentUsers">
            <el-table-column prop="phone" label="手机号" />
            <el-table-column prop="nickname" label="昵称" />
            <el-table-column prop="last_login_at" label="最后登录" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>待审核内容</template>
          <el-table :data="pendingReviews">
            <el-table-column prop="user_id" label="用户ID" />
            <el-table-column prop="target_type" label="类型" />
            <el-table-column prop="created_at" label="提交时间" />
            <el-table-column label="操作">
              <template #default>
                <el-button size="small">审核</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const recentUsers = ref([
  { phone: '138****8001', nickname: '用户A', last_login_at: '2024-01-14 10:30' },
  { phone: '139****8002', nickname: '用户B', last_login_at: '2024-01-14 09:15' }
])

const pendingReviews = ref([
  { user_id: 1001, target_type: 'digital_human', created_at: '2024-01-14 08:00' },
  { user_id: 1002, target_type: 'video', created_at: '2024-01-13 22:30' }
])
</script>

<style scoped lang="scss">
.admin-dashboard {
  .stats {
    .stat-item {
      display: flex;
      flex-direction: column;
      .label { color: #909399; font-size: 14px; margin-bottom: 8px; }
      .value { font-size: 28px; font-weight: 600; color: #303133; }
    }
  }
}
</style>
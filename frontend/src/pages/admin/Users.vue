<template>
  <div class="admin-users">
    <div class="header">
      <h3>用户管理</h3>
      <el-input v-model="keyword" placeholder="搜索用户" style="width: 200px;" />
    </div>
    <el-table :data="users" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column prop="membership_type" label="会员类型" width="100">
        <template #default="{ row }">
          <el-tag :type="row.membership_type === 'vip' ? 'success' : 'info'" size="small">
            {{ row.membership_type }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="balance" label="余额" width="100" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="注册时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="handleView(row)">详情</el-button>
          <el-button
            v-if="row.status === 'active'"
            size="small"
            type="danger"
            @click="handleBan(row.id)"
          >
            封禁
          </el-button>
          <el-button
            v-else
            size="small"
            type="success"
            @click="handleUnban(row.id)"
          >
            解封
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="page"
      :page-size="20"
      :total="total"
      layout="total, prev, pager, next"
      style="margin-top: 24px;"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const keyword = ref('')
const page = ref(1)
const total = ref(0)
const loading = ref(false)
const users = ref<any[]>([])

const handleView = (user: any) => {}
const handleBan = async (id: number) => {
  await request.post(`/admin/users/${id}/ban`, { action: 'ban' })
  ElMessage.success('已封禁')
  fetchUsers()
}
const handleUnban = async (id: number) => {
  await request.post(`/admin/users/${id}/ban`, { action: 'unban' })
  ElMessage.success('已解封')
  fetchUsers()
}

const fetchUsers = async () => {
  loading.value = true
  const res = await request.get('/admin/users', { params: { page: page.value, keyword: keyword.value } })
  users.value = res.items || []
  total.value = res.pagination?.total || 0
  loading.value = false
}

onMounted(fetchUsers)
</script>

<style scoped lang="scss">
.admin-users {
  .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; h3 { margin: 0; } }
}
</style>
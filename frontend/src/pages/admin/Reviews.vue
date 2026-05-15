<template>
  <div class="admin-reviews">
    <h3>内容审核</h3>
    <el-table :data="items" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="user_id" label="用户ID" width="100" />
      <el-table-column prop="target_type" label="类型" width="120" />
      <el-table-column prop="review_type" label="审核类型" width="120" />
      <el-table-column prop="risk_score" label="风险分数" width="100">
        <template #default="{ row }">
          <span :class="{ 'high-risk': row.risk_score > 0.7 }">{{ row.risk_score }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="提交时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" type="success" @click="handleApprove(row.id)">通过</el-button>
          <el-button size="small" type="danger" @click="handleReject(row.id)">驳回</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const items = ref<any[]>([])

const handleApprove = async (id: number) => {
  await request.post(`/admin/reviews/${id}/approve`, { reason: '' })
  ElMessage.success('已通过')
  items.value = items.value.filter(item => item.id !== id)
}

const handleReject = async (id: number) => {
  await request.post(`/admin/reviews/${id}/reject`, { reason: '' })
  ElMessage.success('已驳回')
  items.value = items.value.filter(item => item.id !== id)
}

onMounted(async () => {
  loading.value = true
  const res = await request.get('/admin/reviews/pending')
  items.value = res.items || []
  loading.value = false
})
</script>

<style scoped lang="scss">
.admin-reviews {
  h3 { margin: 0 0 24px; }
  .high-risk { color: #f56c6c; font-weight: 600; }
}
</style>
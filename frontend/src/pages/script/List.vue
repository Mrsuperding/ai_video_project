<template>
  <div class="script-list">
    <div class="header">
      <h2>脚本管理</h2>
      <el-button type="primary" @click="$router.push('/script/create')">新建脚本</el-button>
    </div>
    <el-table :data="items" @row-click="handleRowClick">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="duration" label="时长(秒)" width="100" />
      <el-table-column prop="word_count" label="字数" width="80" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'completed' ? 'success' : 'info'" size="small">
            {{ row.status === 'completed' ? '已完成' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/api/request'

const router = useRouter()
const items = ref<any[]>([])

const handleRowClick = (row: any) => {
  router.push(`/script/${row.id}/edit`)
}

onMounted(async () => {
  const res = await request.get('/script')
  items.value = res.items || []
})
</script>

<style scoped lang="scss">
.script-list {
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    h2 { margin: 0; }
  }
}
</style>
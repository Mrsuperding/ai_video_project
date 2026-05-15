<template>
  <div class="video-list">
    <div class="header">
      <h2>视频项目</h2>
      <el-button type="primary" @click="$router.push('/video/create')">创建项目</el-button>
    </div>
    <el-table :data="items" @row-click="handleRowClick">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="project_name" label="项目名称" />
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column prop="duration" label="时长(秒)" width="100" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)" size="small">{{ getStatusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click.stop="$router.push(`/video/${row.id}`)">查看</el-button>
          <el-button size="small" type="danger" @click.stop="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getVideoProjects } from '@/api/modules/video'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/request'

const router = useRouter()
const items = ref<any[]>([])

const getStatusType = (status: string) => {
  const map: Record<string, any> = { completed: 'success', processing: 'warning', failed: 'danger', pending: 'info' }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = { completed: '已完成', processing: '生成中', failed: '失败', pending: '等待' }
  return map[status] || status
}

const handleRowClick = (row: any) => router.push(`/video/${row.id}`)

const handleDelete = async (id: number) => {
  await ElMessageBox.confirm('确定要删除该项目吗？')
  await request.delete(`/video/${id}`)
  ElMessage.success('删除成功')
  items.value = items.value.filter(item => item.id !== id)
}

onMounted(async () => {
  const res = await getVideoProjects()
  items.value = res.items || []
})
</script>

<style scoped lang="scss">
.video-list {
  .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; h2 { margin: 0; } }
}
</style>
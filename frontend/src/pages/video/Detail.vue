<template>
  <div class="video-detail">
    <el-page-header @back="$router.back()" content="项目详情" />

    <el-row :gutter="24" style="margin-top: 24px;">
      <el-col :span="16">
        <el-card>
          <div class="video-preview">
            <video v-if="item.output_url" :src="item.output_url" controls />
            <div v-else class="placeholder">
              <el-icon :size="48"><VideoPlay /></el-icon>
              <span>暂无视频</span>
            </div>
          </div>
          <div class="info">
            <h3>{{ item.project_name }}</h3>
            <div class="meta">
              <el-tag :type="getStatusType(item.status)">{{ getStatusText(item.status) }}</el-tag>
              <span>时长: {{ item.duration || '-' }}秒</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>操作</template>
          <el-button
            v-if="item.status === 'draft' || item.status === 'failed'"
            type="primary"
            style="width: 100%"
            @click="handleGenerate"
          >
            提交生成
          </el-button>
          <el-button
            v-if="item.status === 'processing' || item.status === 'pending'"
            type="warning"
            style="width: 100%"
            @click="handleCancel"
          >
            取消生成
          </el-button>
          <el-button style="width: 100%; margin-top: 12px;" @click="$router.push(`/video/${item.id}/output`)">
            视频输出
          </el-button>
          <el-button type="danger" style="width: 100%; margin-top: 12px;" @click="handleDelete">
            删除项目
          </el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { VideoPlay } from '@element-plus/icons-vue'
import { getVideoProjectDetail, submitVideoGenerate, cancelVideoGenerate } from '@/api/modules/video'
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const route = useRoute()
const router = useRouter()
const item = ref<any>({ project_name: '', status: 'draft', duration: 0 })

const getStatusType = (status: string) => {
  const map: Record<string, any> = { completed: 'success', processing: 'warning', failed: 'danger', draft: 'info' }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = { completed: '已完成', processing: '生成中', failed: '失败', draft: '草稿', pending: '等待' }
  return map[status] || status
}

const handleGenerate = async () => {
  await submitVideoGenerate(Number(route.params.id))
  ElMessage.success('生成任务已提交')
  item.value.status = 'pending'
}

const handleCancel = async () => {
  await cancelVideoGenerate(Number(route.params.id))
  ElMessage.success('已取消生成')
  item.value.status = 'draft'
}

const handleDelete = async () => {
  await request.delete(`/video/${route.params.id}`)
  router.push('/video')
}

onMounted(async () => {
  item.value = await getVideoProjectDetail(Number(route.params.id))
})
</script>

<style scoped lang="scss">
.video-detail {
  .video-preview {
    background: #000;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 16px;
    video { width: 100%; display: block; }
    .placeholder {
      height: 300px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #fff;
      gap: 16px;
      background: #1a1a1a;
    }
  }
  .info {
    h3 { margin: 0 0 12px; }
    .meta { display: flex; gap: 16px; align-items: center; span { color: #909399; } }
  }
}
</style>
<template>
  <div class="digital-human-detail">
    <el-page-header @back="$router.back()" content="数字人详情" />

    <el-row :gutter="24" style="margin-top: 24px;">
      <el-col :span="16">
        <el-card>
          <div class="preview">
            <img v-if="item.thumbnail_url" :src="item.thumbnail_url" :alt="item.name" />
            <div v-else class="placeholder">暂无预览</div>
          </div>
          <div class="info">
            <h3>{{ item.name }}</h3>
            <p>{{ item.description }}</p>
            <div class="meta">
              <el-tag :type="getStatusType(item.status)">{{ getStatusText(item.status) }}</el-tag>
              <span>使用 {{ item.use_count }} 次</span>
              <span>观看 {{ item.watch_count }} 次</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>操作</template>
          <el-button type="primary" style="width: 100%" @click="handleGenerate">
            生成数字人
          </el-button>
          <el-button style="width: 100%; margin-top: 12px;" @click="handleEdit">
            编辑信息
          </el-button>
          <el-button type="danger" style="width: 100%; margin-top: 12px;" @click="handleDelete">
            删除
          </el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getDigitalHumanDetail, generateDigitalHuman, deleteDigitalHuman } from '@/api/modules/digital-human'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const item = ref<any>({
  name: '',
  status: 'pending',
  use_count: 0,
  watch_count: 0,
  thumbnail_url: ''
})

const getStatusType = (status: string) => {
  const map: Record<string, any> = { ready: 'success', processing: 'warning', pending: 'info', failed: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = { ready: '就绪', processing: '生成中', pending: '等待中', failed: '失败' }
  return map[status] || status
}

const handleGenerate = async () => {
  await generateDigitalHuman(Number(route.params.id))
  ElMessage.success('生成任务已提交')
}

const handleEdit = () => {}
const handleDelete = async () => {
  await deleteDigitalHuman(Number(route.params.id))
  router.push('/digital-human')
}

onMounted(async () => {
  item.value = await getDigitalHumanDetail(Number(route.params.id))
})
</script>

<style scoped lang="scss">
.digital-human-detail {
  .preview {
    height: 300px;
    background: #f5f7fa;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 16px;
    img { width: 100%; height: 100%; object-fit: contain; }
    .placeholder { display: flex; align-items: center; justify-content: center; height: 100%; color: #909399; }
  }
  .info {
    h3 { margin: 0 0 8px; }
    p { color: #606266; margin-bottom: 16px; }
    .meta { display: flex; gap: 16px; align-items: center; span { color: #909399; font-size: 14px; } }
  }
}
</style>
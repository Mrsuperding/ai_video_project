<template>
  <div class="asset-page">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="我的素材" name="mine">
        <div class="header">
          <el-button type="primary" @click="showUploadDialog = true">上传素材</el-button>
        </div>
        <el-row :gutter="16">
          <el-col v-for="item in mineItems" :key="item.id" :span="6">
            <el-card class="asset-card">
              <div class="thumbnail">
                <img v-if="item.url" :src="item.url" :alt="item.name" />
                <div v-else class="placeholder">暂无封面</div>
              </div>
              <div class="info">
                <span>{{ item.name }}</span>
                <span class="size">{{ formatSize(item.size) }}</span>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="平台素材" name="platform">
        <el-empty description="平台素材" />
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="showUploadDialog" title="上传素材" width="400px">
      <el-upload
        drag
        action="/api/v1/asset/upload"
        headers="{ Authorization: `Bearer ${token}` }"
        multiple
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      </el-upload>
      <template #footer>
        <el-button @click="showUploadDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import request from '@/api/request'

const activeTab = ref('mine')
const showUploadDialog = ref(false)
const mineItems = ref<any[]>([])
const token = localStorage.getItem('token') || ''

const formatSize = (bytes: number) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

onMounted(async () => {
  const res = await request.get('/asset')
  mineItems.value = res.items || []
})
</script>

<style scoped lang="scss">
.asset-page {
  .header { margin-bottom: 16px; }
  .asset-card {
    .thumbnail {
      height: 120px;
      background: #f5f7fa;
      border-radius: 4px;
      overflow: hidden;
      margin-bottom: 8px;
      img { width: 100%; height: 100%; object-fit: cover; }
      .placeholder { display: flex; align-items: center; justify-content: center; height: 100%; color: #909399; }
    }
    .info { display: flex; justify-content: space-between; font-size: 14px; .size { color: #909399; } }
  }
}
</style>
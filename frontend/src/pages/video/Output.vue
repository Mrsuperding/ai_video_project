<template>
  <div class="video-output">
    <el-page-header @back="$router.back()" content="视频输出" />
    <el-card style="margin-top: 24px;">
      <div v-if="output" class="output-info">
        <video :src="output.video_url" controls style="width: 100%; max-height: 500px;" />
        <div class="actions">
          <el-button type="primary" @click="handleDownload">下载视频</el-button>
          <el-button @click="handleShare">分享</el-button>
        </div>
      </div>
      <el-empty v-else description="暂无输出视频" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getVideoOutput } from '@/api/modules/video'

const route = useRoute()
const output = ref<any>(null)

onMounted(async () => {
  output.value = await getVideoOutput(Number(route.params.id))
})

const handleDownload = () => {
  if (output.value?.video_url) {
    window.open(output.value.video_url, '_blank')
  }
}

const handleShare = () => {
  // TODO: share dialog
}
</script>

<style scoped lang="scss">
.video-output {
  .output-info { }
  .actions { margin-top: 24px; display: flex; gap: 12px; }
}
</style>
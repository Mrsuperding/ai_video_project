<template>
  <div class="digital-human-list">
    <div class="header">
      <h2>我的数字人</h2>
      <el-button type="primary" @click="$router.push('/digital-human/create')">
        创建数字人
      </el-button>
    </div>

    <el-row :gutter="16" class="list">
      <el-col v-for="item in items" :key="item.id" :span="6">
        <el-card class="dh-card" @click="$router.push(`/digital-human/${item.id}`)">
          <div class="thumbnail">
            <img v-if="item.thumbnail_url" :src="item.thumbnail_url" :alt="item.name" />
            <div v-else class="placeholder">暂无封面</div>
          </div>
          <div class="info">
            <h4>{{ item.name }}</h4>
            <div class="meta">
              <el-tag :type="getStatusType(item.status)" size="small">
                {{ getStatusText(item.status) }}
              </el-tag>
              <span class="use-count">使用 {{ item.use_count }} 次</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="items.length === 0" description="暂无数字人" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDigitalHumans } from '@/api/modules/digital-human'

const items = ref<any[]>([])

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    ready: 'success',
    processing: 'warning',
    pending: 'info',
    failed: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    ready: '就绪',
    processing: '生成中',
    pending: '等待中',
    failed: '失败'
  }
  return map[status] || status
}

onMounted(async () => {
  const res = await getDigitalHumans()
  items.value = res.items || []
})
</script>

<style scoped lang="scss">
.digital-human-list {
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    h2 { margin: 0; }
  }
  .list {
    .dh-card {
      cursor: pointer;
      transition: all 0.3s;
      &:hover { transform: translateY(-4px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
      .thumbnail {
        height: 160px;
        background: #f5f7fa;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 12px;
        img { width: 100%; height: 100%; object-fit: cover; }
        .placeholder { display: flex; align-items: center; justify-content: center; height: 100%; color: #909399; }
      }
      .info {
        h4 { margin: 0 0 8px; }
        .meta {
          display: flex;
          justify-content: space-between;
          align-items: center;
          .use-count { font-size: 12px; color: #909399; }
        }
      }
    }
  }
}
</style>
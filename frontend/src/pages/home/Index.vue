<template>
  <div class="home-page">
    <el-row :gutter="24">
      <el-col :span="16">
        <div class="main-content">
          <div class="welcome-banner">
            <h2>欢迎使用 AI 数字人视频平台</h2>
            <p>轻松创建专业的数字人视频内容</p>
            <el-button type="primary" size="large" @click="$router.push('/video/create')">
              创建视频项目
            </el-button>
          </div>

          <div class="quick-actions">
            <h3>快捷操作</h3>
            <el-row :gutter="16">
              <el-col :span="6">
                <div class="action-card" @click="$router.push('/digital-human/create')">
                  <el-icon :size="32"><Plus /></el-icon>
                  <span>创建数字人</span>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="action-card" @click="$router.push('/script/create')">
                  <el-icon :size="32"><Document /></el-icon>
                  <span>新建脚本</span>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="action-card" @click="$router.push('/asset')">
                  <el-icon :size="32"><Upload /></el-icon>
                  <span>上传素材</span>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="action-card" @click="$router.push('/video')">
                  <el-icon :size="32"><VideoPlay /></el-icon>
                  <span>视频列表</span>
                </div>
              </el-col>
            </el-row>
          </div>

          <div class="recent-projects">
            <h3>最近项目</h3>
            <el-empty v-if="projects.length === 0" description="暂无项目" />
            <div v-else class="project-list">
              <div v-for="project in projects" :key="project.id" class="project-item">
                <div class="project-info">
                  <h4>{{ project.project_name }}</h4>
                  <span class="status" :class="project.status">{{ project.status }}</span>
                </div>
                <span class="date">{{ formatDate(project.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-col>

      <el-col :span="8">
        <div class="side-content">
          <el-card class="quota-card">
            <template #header>
              <span>我的配额</span>
            </template>
            <div class="quota-item">
              <span>数字人</span>
              <el-progress :percentage="20" />
              <span class="quota-text">2/10</span>
            </div>
            <div class="quota-item">
              <span>本月视频</span>
              <el-progress :percentage="15" />
              <span class="quota-text">15/100</span>
            </div>
            <el-button type="primary" link @click="$router.push('/user/membership')">
              升级会员
            </el-button>
          </el-card>

          <el-card class="membership-card">
            <template #header>
              <span>会员信息</span>
            </template>
            <div class="membership-info">
              <el-tag type="success">VIP会员</el-tag>
              <span class="expire">到期时间: 2025-12-31</span>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Document, Upload, VideoPlay } from '@element-plus/icons-vue'
import { getVideoProjects } from '@/api/modules/video'

const projects = ref<any[]>([])

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

onMounted(async () => {
  try {
    const res = await getVideoProjects({ page_size: 5 })
    projects.value = res.items || []
  } catch (e) {
    // ignore
  }
})
</script>

<style scoped lang="scss">
.home-page {
  .welcome-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    padding: 32px;
    border-radius: 8px;
    margin-bottom: 24px;
    h2 { margin-bottom: 8px; }
    p { margin-bottom: 24px; opacity: 0.9; }
  }

  .quick-actions {
    margin-bottom: 24px;
    h3 { margin-bottom: 16px; }
    .action-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      padding: 24px;
      background: #fff;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s;
      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      }
    }
  }

  .recent-projects {
    background: #fff;
    padding: 24px;
    border-radius: 8px;
    h3 { margin-bottom: 16px; }
    .project-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid #f0f0f0;
      &:last-child { border-bottom: none; }
      .project-info {
        display: flex;
        align-items: center;
        gap: 12px;
        h4 { margin: 0; }
        .status {
          font-size: 12px;
          padding: 2px 8px;
          border-radius: 4px;
          &.completed { background: #e1f3d8; color: #67c23a; }
          &.processing { background: #ecf5ff; color: #409eff; }
          &.failed { background: #fef0f0; color: #f56c6c; }
        }
      }
      .date { color: #909399; font-size: 14px; }
    }
  }

  .side-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
    .quota-card, .membership-card {
      .quota-item {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
        span:first-child { width: 80px; }
        .quota-text { font-size: 14px; color: #909399; }
      }
      .membership-info {
        display: flex;
        flex-direction: column;
        gap: 8px;
        .expire { color: #909399; font-size: 14px; }
      }
    }
  }
}
</style>
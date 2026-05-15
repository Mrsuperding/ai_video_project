<template>
  <div class="video-create">
    <el-card>
      <template #header>
        <span>创建视频项目</span>
      </template>
      <el-form :model="form" label-width="120px">
        <el-form-item label="项目名称">
          <el-input v-model="form.project_name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="选择脚本">
          <el-select v-model="form.script_id" placeholder="请选择脚本">
            <el-option v-for="s in scripts" :key="s.id" :label="s.title" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="选择数字人">
          <el-select v-model="form.digital_human_id" placeholder="请选择数字人">
            <el-option v-for="dh in digitalHumans" :key="dh.id" :label="dh.name" :value="dh.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="请选择分类">
            <el-option label="宣传" value="promotion" />
            <el-option label="介绍" value="intro" />
            <el-option label="广告" value="ad" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleCreate">创建</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createVideoProject } from '@/api/modules/video'
import request from '@/api/request'

const router = useRouter()
const scripts = ref<any[]>([])
const digitalHumans = ref<any[]>([])
const form = reactive({
  project_name: '',
  script_id: undefined as number | undefined,
  digital_human_id: undefined as number | undefined,
  category: ''
})

const handleCreate = async () => {
  if (!form.project_name || !form.script_id || !form.digital_human_id) return
  await createVideoProject(form)
  router.push('/video')
}

onMounted(async () => {
  const [scriptsRes, dhRes] = await Promise.all([
    request.get('/script', { params: { page_size: 100 } }),
    request.get('/digital-human', { params: { page_size: 100 } })
  ])
  scripts.value = scriptsRes.items || []
  digitalHumans.value = dhRes.items || []
})
</script>

<style scoped lang="scss">
.video-create { max-width: 600px; }
</style>
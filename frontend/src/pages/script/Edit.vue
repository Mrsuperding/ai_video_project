<template>
  <div class="script-edit">
    <el-card>
      <template #header>
        <span>编辑脚本</span>
      </template>
      <el-form :model="form" label-width="100px">
        <el-form-item label="标题">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="文案内容">
          <el-input v-model="form.content" type="textarea" :rows="10" />
        </el-form-item>
        <el-form-item label="配音演员">
          <el-select v-model="form.voice_id">
            <el-option label="男声-标准" :value="1" />
            <el-option label="女声-温柔" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave">保存</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '@/api/request'

const route = useRoute()
const router = useRouter()
const form = reactive({ title: '', content: '', voice_id: undefined as number | undefined })
const script = ref<any>(null)

onMounted(async () => {
  script.value = await request.get(`/script/${route.params.id}`)
  Object.assign(form, script.value)
})

const handleSave = async () => {
  await request.patch(`/script/${route.params.id}`, form)
  router.push('/script')
}
</script>

<style scoped lang="scss">
.script-edit { max-width: 800px; }
</style>
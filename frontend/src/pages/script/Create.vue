<template>
  <div class="script-create">
    <el-card>
      <template #header>
        <span>新建脚本</span>
      </template>
      <el-form :model="form" label-width="100px">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入脚本标题" />
        </el-form-item>
        <el-form-item label="文案内容">
          <el-input v-model="form.content" type="textarea" :rows="10" placeholder="请输入文案内容" />
        </el-form-item>
        <el-form-item label="配音演员">
          <el-select v-model="form.voice_id" placeholder="请选择配音演员">
            <el-option label="男声-标准" :value="1" />
            <el-option label="女声-温柔" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="背景音乐">
          <el-select v-model="form.bgm_id" placeholder="请选择背景音乐">
            <el-option label="无" :value="0" />
            <el-option label="轻音乐" :value="1" />
            <el-option label="企业风" :value="2" />
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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/api/request'

const router = useRouter()
const form = reactive({
  title: '',
  content: '',
  voice_id: undefined as number | undefined,
  bgm_id: 0
})

const handleSave = async () => {
  if (!form.title || !form.content) return
  await request.post('/script', form)
  router.push('/script')
}
</script>

<style scoped lang="scss">
.script-create {
  max-width: 800px;
}
</style>
<template>
  <div class="digital-human-create">
    <el-card>
      <template #header>
        <span>创建数字人</span>
      </template>
      <el-form :model="form" label-width="120px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="请输入数字人名称" />
        </el-form-item>
        <el-form-item label="来源">
          <el-radio-group v-model="form.source">
            <el-radio label="photo">照片生成</el-radio>
            <el-radio label="template">模板选择</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="form.source === 'photo'" label="照片">
          <el-input v-model="form.photo_url" placeholder="请输入照片URL" />
        </el-form-item>
        <el-form-item v-if="form.source === 'template'" label="模板">
          <el-select v-model="form.template_id" placeholder="请选择模板">
            <el-option label="模板1" :value="1" />
            <el-option label="模板2" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="form.gender" placeholder="请选择">
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
          </el-select>
        </el-form-item>
        <el-form-item label="风格">
          <el-checkbox-group v-model="form.style">
            <el-checkbox label="professional">专业</el-checkbox>
            <el-checkbox label="casual">休闲</el-checkbox>
            <el-checkbox label="formal">正式</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleCreate">创建</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { createDigitalHuman } from '@/api/modules/digital-human'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  name: '',
  source: 'photo',
  photo_url: '',
  template_id: undefined as number | undefined,
  gender: '',
  style: [] as string[],
  description: ''
})

const handleCreate = async () => {
  if (!form.name) return
  loading.value = true
  try {
    await createDigitalHuman(form)
    router.push('/digital-human')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.digital-human-create {
  max-width: 600px;
}
</style>
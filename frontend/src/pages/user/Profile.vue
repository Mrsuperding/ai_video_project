<template>
  <div class="profile-page">
    <el-card>
      <template #header>
        <span>个人资料</span>
      </template>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="头像">
          <el-avatar :src="form.avatar_url" :size="80" />
          <el-button size="small" style="margin-left: 16px" @click="showAvatarDialog = true">
            更换头像
          </el-button>
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" disabled />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input v-model="form.real_name" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog v-model="showAvatarDialog" title="更换头像" width="400px">
      <el-input v-model="avatarUrl" placeholder="请输入头像 URL" />
      <template #footer>
        <el-button @click="showAvatarDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUpdateAvatar">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { FormInstance } from 'element-plus'
import { getProfile, updateProfile, updateAvatar } from '@/api/modules/user'

const formRef = ref<FormInstance>()
const showAvatarDialog = ref(false)
const avatarUrl = ref('')

const form = reactive({
  phone: '',
  email: '',
  nickname: '',
  real_name: '',
  avatar_url: ''
})

const rules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  email: [{ type: 'email', message: '邮箱格式错误', trigger: 'blur' }]
}

const handleSave = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async () => {
    await updateProfile({
      nickname: form.nickname,
      email: form.email,
      real_name: form.real_name
    })
  })
}

const handleUpdateAvatar = async () => {
  await updateAvatar(avatarUrl.value)
  form.avatar_url = avatarUrl.value
  showAvatarDialog.value = false
}

onMounted(async () => {
  const profile = await getProfile()
  Object.assign(form, profile)
})
</script>

<style scoped lang="scss">
.profile-page {
  max-width: 600px;
}
</style>
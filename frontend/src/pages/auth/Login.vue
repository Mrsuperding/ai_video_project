<template>
  <div class="login-page">
    <div class="login-card">
      <h2 class="title">登录</h2>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="0"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="loginKey">
          <el-input
            v-model="form.loginKey"
            placeholder="手机号/邮箱"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            size="large"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            native-type="submit"
            style="width: 100%"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <div class="links">
        <router-link to="/auth/register">注册账号</router-link>
        <router-link to="/auth/forgot-password">忘记密码</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { loginByPassword } from '@/api/modules/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const form = reactive({
  loginKey: '',
  password: ''
})

const rules = {
  loginKey: [{ required: true, message: '请输入手机号或邮箱', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      const res = await loginByPassword({
        account: form.loginKey,
        password: form.password
      })
      if (res && res.tokens) {
        userStore.setToken(res.tokens.access_token)
        router.push('/')
      } else {
        ElMessage.error('登录失败，请稍后重试')
      }
    } catch (error: any) {
      ElMessage.error('登录出错: ' + (error?.message || '未知错误'))
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped lang="scss">
.login-page {
  width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  .title {
    text-align: center;
    margin-bottom: 32px;
    color: #303133;
  }
  .links {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    a {
      color: #409EFF;
    }
  }
}
</style>
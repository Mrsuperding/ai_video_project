<template>
  <div class="register-page">
    <div class="register-card">
      <h2 class="title">注册</h2>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="0"
        @submit.prevent="handleRegister"
      >
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="手机号" size="large" />
        </el-form-item>
        <el-form-item prop="smsCode">
          <div class="sms-code-row">
            <el-input v-model="form.smsCode" placeholder="验证码" size="large" />
            <el-button :disabled="countdown > 0" @click="sendCode">
              {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码 (8位以上)"
            size="large"
            show-password
          />
        </el-form-item>
        <el-form-item prop="inviteCode">
          <el-input v-model="form.inviteCode" placeholder="邀请码 (可选)" size="large" />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            native-type="submit"
            style="width: 100%"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      <div class="links">
        <router-link to="/auth/login">已有账号？去登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance } from 'element-plus'
import { sendSmsCode, register } from '@/api/modules/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const countdown = ref(0)

const form = reactive({
  phone: '',
  smsCode: '',
  password: '',
  inviteCode: ''
})

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式错误', trigger: 'blur' }
  ],
  smsCode: [{ required: true, message: '请输入验证码', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码至少8位', trigger: 'blur' }
  ]
}

let timer: number | null = null

const sendCode = async () => {
  if (!/^1[3-9]\d{9}$/.test(form.phone)) {
    return
  }
  await sendSmsCode({ phone: form.phone, type: 'register' })
  countdown.value = 60
  timer = window.setInterval(() => {
    countdown.value--
    if (countdown.value <= 0 && timer) {
      clearInterval(timer)
    }
  }, 1000)
}

const handleRegister = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      const res = await register({
        phone: form.phone,
        password: form.password,
        sms_code: form.smsCode,
        invite_code: form.inviteCode || undefined
      })
      userStore.setToken(res.tokens.access_token)
      router.push('/')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped lang="scss">
.register-page {
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
  .sms-code-row {
    display: flex;
    gap: 8px;
    .el-input {
      flex: 1;
    }
  }
  .links {
    text-align: center;
    font-size: 14px;
    a {
      color: #409EFF;
    }
  }
}
</style>
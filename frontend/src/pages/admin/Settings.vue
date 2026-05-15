<template>
  <div class="admin-settings">
    <h3>系统设置</h3>
    <el-card>
      <template #header>基本配置</template>
      <el-form label-width="150px">
        <el-form-item label="网站名称">
          <el-input v-model="config.site_name" style="width: 300px;" />
        </el-form-item>
        <el-form-item label="Logo URL">
          <el-input v-model="config.logo_url" style="width: 400px;" />
        </el-form-item>
        <el-form-item label="客服电话">
          <el-input v-model="config.service_phone" style="width: 200px;" />
        </el-form-item>
        <el-form-item label="会员价格">
          <el-input-number v-model="config.vip_price" :min="0" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const config = reactive({
  site_name: 'AI 数字人视频平台',
  logo_url: '',
  service_phone: '400-xxx-xxxx',
  vip_price: 299
})

const handleSave = async () => {
  await request.patch('/admin/configs', { configs: Object.entries(config).map(([key, value]) => ({ key, value })) })
  ElMessage.success('保存成功')
}
</script>

<style scoped lang="scss">
.admin-settings { h3 { margin: 0 0 24px; } }
</style>
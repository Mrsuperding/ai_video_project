<template>
  <div class="membership-page">
    <el-card>
      <template #header>
        <span>会员中心</span>
      </template>
      <div class="current-plan">
        <el-tag type="success" size="large">VIP会员</el-tag>
        <p>到期时间: 2025-12-31</p>
      </div>
    </el-card>

    <h3>会员套餐</h3>
    <el-row :gutter="16">
      <el-col v-for="plan in plans" :key="plan.id" :span="8">
        <el-card class="plan-card" :class="{ active: plan.popular }">
          <div v-if="plan.popular" class="popular-tag">热门</div>
          <h4>{{ plan.name }}</h4>
          <div class="price">
            <span class="currency">¥</span>
            <span class="amount">{{ plan.price }}</span>
            <span class="period">/{{ plan.period }}</span>
          </div>
          <ul class="features">
            <li v-for="feature in plan.features" :key="feature">
              <el-icon><Check /></el-icon>
              {{ feature }}
            </li>
          </ul>
          <el-button :type="plan.popular ? 'primary' : 'default'" style="width: 100%">
            立即购买
          </el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Check } from '@element-plus/icons-vue'

const plans = ref([
  {
    id: 1,
    name: '基础版',
    price: 99,
    period: '月',
    popular: false,
    features: ['3个数字人', '50个视频/月', '1TB存储空间', '邮件支持']
  },
  {
    id: 2,
    name: 'VIP',
    price: 299,
    period: '月',
    popular: true,
    features: ['10个数字人', '200个视频/月', '5TB存储空间', '优先客服', 'API访问']
  },
  {
    id: 3,
    name: '企业版',
    price: 999,
    period: '月',
    popular: false,
    features: ['无限数字人', '无限视频', '无限存储', '专属客服', 'API访问', '定制服务']
  }
])
</script>

<style scoped lang="scss">
.membership-page {
  h3 { margin: 24px 0 16px; }
  .current-plan {
    display: flex;
    align-items: center;
    gap: 16px;
    p { color: #909399; margin: 0; }
  }
  .plan-card {
    position: relative;
    text-align: center;
    &.active {
      border-color: #409EFF;
    }
    .popular-tag {
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      background: #409EFF;
      color: #fff;
      padding: 4px 16px;
      border-radius: 12px;
      font-size: 12px;
    }
    h4 { margin: 0 0 16px; }
    .price {
      margin-bottom: 24px;
      .currency { font-size: 16px; vertical-align: top; }
      .amount { font-size: 36px; font-weight: 600; }
      .period { color: #909399; }
    }
    .features {
      list-style: none;
      padding: 0;
      margin: 0 0 24px;
      li {
        padding: 8px 0;
        color: #606266;
        .el-icon { color: #67c23a; margin-right: 8px; }
      }
    }
  }
}
</style>
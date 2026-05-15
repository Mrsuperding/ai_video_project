<template>
  <div class="wallet-page">
    <el-card>
      <template #header>
        <span>我的钱包</span>
      </template>
      <div class="balance-info">
        <div class="balance">
          <span class="label">账户余额</span>
          <span class="amount">¥ {{ balance }}</span>
        </div>
        <div class="frozen">
          <span class="label">冻结金额</span>
          <span class="amount">¥ {{ frozen }}</span>
        </div>
        <el-button type="primary" @click="showRechargeDialog = true">充值</el-button>
      </div>
    </el-card>

    <el-card style="margin-top: 24px;">
      <template #header>
        <span>交易记录</span>
      </template>
      <el-table :data="transactions">
        <el-table-column prop="created_at" label="时间" width="180" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="row.type === 'recharge' ? 'success' : 'warning'">
              {{ row.type === 'recharge' ? '充值' : '消费' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额" />
        <el-table-column prop="description" label="说明" />
      </el-table>
    </el-card>

    <el-dialog v-model="showRechargeDialog" title="充值" width="400px">
      <div class="recharge-amounts">
        <el-radio-group v-model="selectedAmount">
          <el-radio-button :label="10">10元</el-radio-button>
          <el-radio-button :label="50">50元</el-radio-button>
          <el-radio-button :label="100">100元</el-radio-button>
          <el-radio-button :label="200">200元</el-radio-button>
          <el-radio-button :label="500">500元</el-radio-button>
        </el-radio-group>
      </div>
      <template #footer>
        <el-button @click="showRechargeDialog = false">取消</el-button>
        <el-button type="primary" @click="handleRecharge">确认充值</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getProfile } from '@/api/modules/user'

const balance = ref('0.00')
const frozen = ref('0.00')
const showRechargeDialog = ref(false)
const selectedAmount = ref(100)
const transactions = ref<any[]>([])

const handleRecharge = () => {
  // TODO: call recharge API
  showRechargeDialog.value = false
}

onMounted(async () => {
  const profile = await getProfile()
  balance.value = profile.balance
  frozen.value = profile.frozen_balance
  // TODO: fetch transactions
})
</script>

<style scoped lang="scss">
.wallet-page {
  max-width: 800px;
  .balance-info {
    display: flex;
    align-items: center;
    gap: 48px;
    .balance, .frozen {
      .label { display: block; color: #909399; font-size: 14px; margin-bottom: 8px; }
      .amount { font-size: 24px; font-weight: 600; }
    }
  }
  .recharge-amounts {
    .el-radio-group {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
  }
}
</style>
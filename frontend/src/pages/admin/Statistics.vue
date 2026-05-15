<template>
  <div class="admin-statistics">
    <h3>数据统计</h3>
    <el-card>
      <template #header>平台概览</template>
      <el-row :gutter="24">
        <el-col :span="8">
          <div class="stat-item">
            <span class="label">总用户数</span>
            <span class="value">12,580</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <span class="label">总视频数</span>
            <span class="value">8,420</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <span class="label">总收入(元)</span>
            <span class="value">125,680</span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card style="margin-top: 24px;">
      <template #header>数据趋势</template>
      <div ref="chartRef" style="height: 300px;"></div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref<HTMLElement>()

onMounted(() => {
  if (chartRef.value) {
    const chart = echarts.init(chartRef.value)
    chart.setOption({
      title: { text: '用户增长趋势' },
      tooltip: {},
      xAxis: { type: 'category', data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'] },
      yAxis: { type: 'value' },
      series: [{ data: [120, 200, 150, 80, 70, 110, 130], type: 'line' }]
    })
  }
})
</script>

<style scoped lang="scss">
.admin-statistics {
  h3 { margin: 0 0 24px; }
  .stat-item {
    text-align: center;
    .label { display: block; color: #909399; font-size: 14px; margin-bottom: 8px; }
    .value { font-size: 28px; font-weight: 600; color: #303133; }
  }
}
</style>
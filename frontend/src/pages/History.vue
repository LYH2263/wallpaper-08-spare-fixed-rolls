<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const lookupId = ref('')
const picked = ref(null)
const lookupErr = ref('')
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
async function openById() {
  lookupErr.value = ''; picked.value = null
  if (lookupId.value === '' || lookupId.value == null) return
  try {
    // 按编号回看：返回的是写入时钉住的订货卷数与 N，不随默认 N 改变
    picked.value = await getJSON(`/api/runs/${Number(lookupId.value)}`)
  } catch (e) { lookupErr.value = e.message }
}
</script>
<template>
  <div class="page"><h1>记录</h1>
  <div class="lookup-row">
    <label>按编号回看 <input type="number" min="1" v-model.number="lookupId" @keyup.enter="openById" /></label>
    <button @click="openById">回看</button>
    <span v-if="lookupErr" class="warn">{{ lookupErr }}</span>
  </div>
  <div v-if="picked" class="run-card">
    <strong>#{{ picked.id }} {{ picked.wall_name }} → {{ picked.roll_name }}</strong>
    <table class="roll-cols"><tbody>
      <tr><td>基础卷数</td><td>{{ picked.result?.rolls }} 卷</td></tr>
      <tr v-if="picked.result?.spare_enabled"><td>固定备用 N</td><td>{{ picked.result?.spare_n }} 枚</td></tr>
      <tr class="order-row"><td>订货卷数</td><td><strong>{{ picked.result?.order_rolls ?? picked.result?.rolls }} 卷</strong></td></tr>
    </tbody></table>
    <p v-if="picked.note" class="hint">备注：{{ picked.note }}</p>
  </div>
  <ul><li v-for="r in items" :key="r.id">
    #{{ r.id }} {{ r.wall_name }} → 基础 {{ r.result?.rolls }} 卷<template v-if="r.result?.spare_enabled"> · 备用 {{ r.result?.spare_n }}</template> ·
    <strong>订货 {{ r.result?.order_rolls ?? r.result?.rolls }} 卷</strong>
  </li></ul></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
const walls = ref([]); const rolls = ref([]); const wallId = ref(1); const rollId = ref(1); const out = ref(null)
const spareEnabled = ref(false); const spareDefaultN = ref(0)
onMounted(async () => {
  walls.value = (await getJSON('/api/walls')).items.filter(w => w.data_quality==='clean')
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  if (walls.value.length) wallId.value = walls.value[0].id
  if (rolls.value.length) rollId.value = rolls.value[0].id
  const s = await getJSON('/api/settings')
  spareDefaultN.value = Number(s.spare_default_n || 0)
})
async function run(save) {
  out.value = save
    ? await postJSON('/api/estimate', { wall_id: wallId.value, roll_id: rollId.value, save: true, spare_enabled: spareEnabled.value })
    : await getJSON(`/api/estimate?wall_id=${wallId.value}&roll_id=${rollId.value}&spare_enabled=${spareEnabled.value}`)
}
</script>
<template>
  <div class="page"><h1>算卷工作台</h1>
  <select v-model.number="wallId"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}</option></select>
  <select v-model.number="rollId"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option></select>
  <label><input type="checkbox" v-model="spareEnabled" /> 固定备用 +{{ spareDefaultN }} 卷</label>
  <button @click="run(false)">试算</button><button @click="run(true)">保存</button>
  <div v-if="out"><strong>{{ out.rolls }} 卷</strong> · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m
  <p v-if="out.spare_enabled">订货 <strong>{{ out.order_rolls }} 卷</strong>（基础 {{ out.rolls }} + 备用 {{ out.spare_n }}）</p>
  <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" /></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
import SpareRollsField from '../components/SpareRollsField.vue'
const walls = ref([]); const rolls = ref([]); const wallId = ref(1); const rollId = ref(1); const out = ref(null)
const spare = ref({ enabled: false, n: 0 })
const err = ref('')
onMounted(async () => {
  walls.value = (await getJSON('/api/walls')).items.filter(w => w.data_quality==='clean')
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  if (walls.value.length) wallId.value = walls.value[0].id
  if (rolls.value.length) rollId.value = rolls.value[0].id
  const s = await getJSON('/api/settings')
  spare.value.n = Number(s.spare_default_n ?? 0)
})
function spareQuery() {
  return spare.value.enabled ? `&spare_enabled=true&spare_n=${spare.value.n ?? 0}` : ''
}
async function run(save) {
  err.value = ''
  try {
    out.value = save
      ? await postJSON('/api/estimate', {
          wall_id: wallId.value, roll_id: rollId.value, save: true,
          spare_enabled: spare.value.enabled, spare_n: spare.value.n,
        })
      : await getJSON(`/api/estimate?wall_id=${wallId.value}&roll_id=${rollId.value}${spareQuery()}`)
  } catch (e) { err.value = e.message }
}
</script>
<template>
  <div class="page"><h1>算卷工作台</h1>
  <select v-model.number="wallId"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}</option></select>
  <select v-model.number="rollId"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option></select>
  <SpareRollsField v-model="spare" />
  <button @click="run(false)">试算</button><button @click="run(true)">保存</button>
  <p v-if="err" class="warn">{{ err }}</p>
  <div v-if="out">
    <table class="roll-cols"><tbody>
      <tr><td>基础卷数</td><td>{{ out.rolls }} 卷</td></tr>
      <tr v-if="out.spare_enabled"><td>固定备用 N</td><td>{{ out.spare_n }} 枚</td></tr>
      <tr class="order-row"><td>订货卷数</td><td><strong>{{ out.order_rolls }} 卷</strong></td></tr>
    </tbody></table>
    · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m
    <!-- 展开示意始终按基础幅数画，不随备用卷增加 -->
    <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" />
  </div>
  </div>
</template>

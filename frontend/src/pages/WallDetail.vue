<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
import SpareRollsField from '../components/SpareRollsField.vue'
const props = defineProps({ id: String })
const wall = ref(null)
const rolls = ref([])
const rollId = ref(null)
const spare = ref({ enabled: false, n: 0 })
const out = ref(null)
const err = ref('')
async function recalc() {
  if (!rollId.value) return
  err.value = ''
  const q = spare.value.enabled ? `&spare_enabled=true&spare_n=${spare.value.n ?? 0}` : ''
  try {
    out.value = await getJSON(`/api/estimate?wall_id=${props.id}&roll_id=${rollId.value}${q}`)
  } catch (e) { err.value = e.message }
}
onMounted(async () => {
  wall.value = await getJSON(`/api/walls/${props.id}`)
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  if (rolls.value.length) rollId.value = rolls.value[0].id
  const s = await getJSON('/api/settings')
  spare.value.n = Number(s.spare_default_n ?? 0)
  recalc()
})
</script>
<template>
  <div class="page" v-if="wall"><h1>{{ wall.name }}</h1>
  <p v-if="wall.data_quality==='dirty'" class="warn">{{ wall.note }}</p>
  <p>周长 {{ wall.perimeter }} m，墙高 {{ wall.height }} m</p>
  <select v-if="wall.data_quality!=='dirty'" v-model.number="rollId" @change="recalc">
    <option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option>
  </select>
  <SpareRollsField v-if="wall.data_quality!=='dirty'" v-model="spare" @update:model-value="recalc" />
  <p v-if="err" class="warn">{{ err }}</p>
  <div v-if="out">
    <!-- 订货列单独显示；展开示意只用基础幅数/基础卷数 -->
    <table class="roll-cols"><tbody>
      <tr><td>基础卷数</td><td>{{ out.rolls }} 卷</td></tr>
      <tr v-if="out.spare_enabled"><td>固定备用 N</td><td>{{ out.spare_n }} 枚</td></tr>
      <tr class="order-row"><td>订货卷数</td><td><strong>{{ out.order_rolls }} 卷</strong></td></tr>
    </tbody></table>
    <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" />
  </div>
  </div>
</template>

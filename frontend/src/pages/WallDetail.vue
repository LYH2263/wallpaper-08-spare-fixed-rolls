<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
const props = defineProps({ id: String })
const wall = ref(null)
const rolls = ref([]); const rollId = ref(null); const est = ref(null)
onMounted(async () => {
  wall.value = await getJSON(`/api/walls/${props.id}`)
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  if (rolls.value.length) rollId.value = rolls.value[0].id
})
async function expand() {
  est.value = await getJSON(`/api/estimate?wall_id=${props.id}&roll_id=${rollId.value}&spare_enabled=true`)
}
</script>
<template>
  <div class="page" v-if="wall"><h1>{{ wall.name }}</h1>
  <p v-if="wall.data_quality==='dirty'" class="warn">{{ wall.note }}</p>
  <p>周长 {{ wall.perimeter }} m，墙高 {{ wall.height }} m</p>
  <div v-if="wall.data_quality==='clean' && rolls.length">
    <select v-model.number="rollId"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option></select>
    <button @click="expand">展开示意</button>
  </div>
  <div v-if="est">
    <DropStripBar :drops="est.drops" :drop-len="est.drop_len_m" :rolls="est.rolls" />
    <table><tr><th>基础卷数</th><th>备用</th><th>订货卷数</th></tr>
    <tr><td>{{ est.rolls }}</td><td>+{{ est.spare_n }}</td><td>{{ est.order_rolls }}</td></tr></table>
  </div></div>
</template>

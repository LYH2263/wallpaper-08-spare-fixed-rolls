<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template>
  <div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id">
    #{{ r.id }} {{ r.wall_name }} → {{ r.result?.rolls }} 卷<template v-if="r.result?.spare_enabled"> · 订货 {{ r.result.order_rolls }} 卷（备用 +{{ r.result.spare_n }}）</template>
  </li></ul></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({})
const defaultN = ref(0)
const msg = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  defaultN.value = Number(s.value.spare_default_n ?? 0)
})
async function save() {
  msg.value = ''
  if (defaultN.value < 0) { msg.value = '默认 N 不能为负'; return }
  const r = await putJSON('/api/settings/spare-default', { spare_n: Math.trunc(defaultN.value) })
  defaultN.value = r.spare_default_n
  s.value = await getJSON('/api/settings')
  msg.value = '已保存（仅影响之后的测算，旧 run 不变）'
}
</script>
<template><div class="page"><h1>设置</h1>
  <div class="settings-row">
    <label>固定备用默认 N
      <input type="number" min="0" step="1" v-model.number="defaultN" /> 枚
    </label>
    <button @click="save">保存默认 N</button>
    <span v-if="msg" class="hint">{{ msg }}</span>
  </div>
  <pre>{{ s }}</pre>
</div></template>

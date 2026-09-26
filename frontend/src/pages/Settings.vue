<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({})
const spareDefaultN = ref(0); const saved = ref(false); const err = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  spareDefaultN.value = Number(s.value.spare_default_n || 0)
})
async function save() {
  err.value = ''; saved.value = false
  try {
    await putJSON('/api/settings/spare_default_n', { spare_default_n: Number(spareDefaultN.value) })
    s.value = await getJSON('/api/settings')
    saved.value = true
  } catch (e) { err.value = String(e.message || e) }
}
</script>
<template>
  <div class="page"><h1>设置</h1>
  <p><label>默认备用卷数 N
    <input type="number" min="0" step="1" v-model.number="spareDefaultN" /></label>
  <button @click="save">保存</button>
  <span v-if="saved">已保存</span><span v-if="err" class="warn">{{ err }}</span></p>
  <pre>{{ s }}</pre></div>
</template>

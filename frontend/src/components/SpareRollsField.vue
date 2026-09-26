<script setup>
// Fixed spare rolls toggle + N input, kept in its own file so the benchmark,
// settings and any future caller share one switch field.
const props = defineProps({
  modelValue: { type: Object, required: true }, // { enabled: Boolean, n: Number }
})
const emit = defineEmits(['update:modelValue'])
function patch(p) { emit('update:modelValue', { ...props.modelValue, ...p }) }
</script>
<template>
  <label class="spare-field">
    <input type="checkbox" :checked="modelValue.enabled" @change="patch({ enabled: $event.target.checked })" />
    固定备用卷
    <input
      type="number" min="0" step="1" :value="modelValue.n ?? ''"
      :disabled="!modelValue.enabled"
      @input="patch({ n: $event.target.value === '' ? null : Number($event.target.value) })"
    /> 枚
  </label>
</template>

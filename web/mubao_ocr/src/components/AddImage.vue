<script setup lang="ts">
import { ref, toRef } from 'vue'

const props = defineProps<{
  text: string
  url?: string
}>()

const emits = defineEmits<{
  (event: 'addImage', data: string): void
}>()

const text = toRef(props, 'text')
const addButton = ref<HTMLInputElement>()

function addImage() {
  addButton.value?.click()
}

function imageOnChanged() {
  const imageFile = addButton.value!.files![0]
  const reader = new FileReader()
  reader.onload = () => {
    emits('addImage', reader.result as string)
  }
  reader.readAsDataURL(imageFile)
  addButton.value!.value = ''
}
</script>

<template>
  <div
    mxauto
    w80vw
    h20vw
    b="w8 dashed"
    rounded-xl
    flex
    justify-center
    items-center
    cursor-pointer
    @click="addImage"
  >
    {{ text }}
  </div>
  <input
    type="file"
    hidden
    ref="addButton"
    accept="image/gif,image/jpeg,image/jpg,image/png,image/svg"
    @change="imageOnChanged"
  />
</template>

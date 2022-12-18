<script setup lang="ts">
import { ref, toRef } from 'vue'
import axios from 'axios'

const props = defineProps<{
  text: string
  type: 'reg' | 'sim'
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
  const data = new FormData()
  data.set('image', imageFile)

  axios({
    url: `/image/${props.type}`,
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then((res) => {
    console.log(res)
  })

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
    accept="image/png,image/gif,image/jpeg"
    @change="imageOnChanged"
  />
</template>

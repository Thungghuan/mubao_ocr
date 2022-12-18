<script setup lang="ts">
const props = defineProps<{
  data?: string
}>()

const emits = defineEmits<{
  (event: 'delImage'): void
  (event: 'copyImage', data: string): void
}>()
</script>

<template>
  <div mx4 hfull b="4 dashed! gray300" box-border relative>
    <img
      wauto
      hfull
      block
      :src="data"
      alt=""
      @click="$emit('copyImage', data)"
    />
    <div absolute right-0 top-0 cursor-pointer @click="$emit('delImage')">
      <div
        w20px
        h20px
        rounded-15px
        bg-red
        flex
        justify-center
        items-center
        text-white
      >
        X
      </div>
    </div>
  </div>
</template>

<style scoped></style>

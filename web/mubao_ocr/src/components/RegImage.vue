<script setup lang="ts">
defineProps<{
  data: string
  result: string
}>()

defineEmits<{
  (event: 'delImage'): void
  (event: 'copyResult', result: string): void
}>()
</script>

<template>
  <div
    mx2
    p2
    flex
    gap-x2
    b="4 dashed! gray300"
    rounded
    relative
    hover="b-solid!"
  >
    <div hfull rounded hover="shadow-md" of-hidden>
      <img wauto hfull :src="data" alt="" />
    </div>
    <div w80 of-hidden flex="~ col 1" justify-evenly>
      <div h="6/7">
        <div
          hfull
          b
          rounded-xl
          bg-white
          opacity-30
          flex
          justify-center
          items-center
          v-if="result === ''"
        >
          <img src="../assets/loading.svg" alt="" />
        </div>
        <div
          px3
          hfull
          b
          rounded-xl
          select-text
          text-justify
          break-all
          of-auto
          v-else
        >
          {{ result }}
        </div>
      </div>
      <div h="1/7">
        <div wfull hfull flex justify-center items-center>
          <div
            w="3/5"
            h="2/3"
            bg-emerald400
            rounded-xl
            flex
            justify-center
            items-center
            font-bold
            text-white
            cursor-pointer
            select-none
            hover="bg-emerald600"
            @click="$emit('copyResult', result)"
          >
            Copy to clipboard!
          </div>
        </div>
      </div>
    </div>
    <div
      absolute
      top--10px
      right--10px
      cursor-pointer
      @click="$emit('delImage')"
    >
      <div
        w30px
        h30px
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

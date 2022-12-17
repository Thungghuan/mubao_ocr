<script setup lang="ts">
import RegImage from './components/RegImage.vue'
import SimpleImage from './components/SimpleImage.vue'
</script>

<template>
  <div
    class="lg:flex flex-col"
    mxauto
    w96vw
    h100vh
    max-h-100vh
    of-hidden
    hidden
  >
    <div my2 p2 h65vh flex of-auto b="4 gray dashed" rounded>
      <RegImage v-for="i in 3" />
    </div>
    <div mxauto my2 w90vw h2 bg-gray300 rounded></div>
    <div my2 h25vh flex of-auto>
      <SimpleImage v-for="i in 20" />
    </div>
  </div>
  <div></div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
}
#main {
  display: flex;
}
</style>

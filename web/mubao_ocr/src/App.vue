<script setup lang="ts">
import { ref } from 'vue'
import RegImage from './components/RegImage.vue'
import SimpleImage from './components/SimpleImage.vue'
import AddImage from './components/AddImage.vue'
import { io } from 'socket.io-client'

// PC端
const regImagesPC = ref<string[]>([])
const regResult = ref<string[]>([])
const simImagesPC = ref<string[]>([])

const socket = io(`ws://${location.host}`)
// client-side
socket.on('connect', () => {
  console.log(socket.id) // x8WIv7-mJelg7on_ALbx

  socket.on('disconnect', () => {
    console.log(socket.id) // undefined
  })

  socket.on('pong', () => {
    console.log('connected')
  })

  socket.on('regImage', (image) => {
    console.log('receive regImage')
    regImagesPC.value.push('data:image/jpg;base64,' + image)
  })

  socket.on('simImage', (image) => {
    console.log('receive simImage')
    simImagesPC.value.push('data:image/jpg;base64,' + image)
  })

  socket.on('regResult', ({ content }) => {
    console.log('receive result')
    console.log(content)
    regResult.value.push(content)
  })

  socket.emit('ping')
})

// 移动端
const regImagesM = ref<string[]>([])
const simImagesM = ref<string[]>([])

function addImageM(type: 'regM' | 'simM', data: string) {
  if (type === 'regM') {
    regImagesM.value.unshift(data)
  } else {
    simImagesM.value.unshift(data)
  }
}

function delImage(type: 'regPC' | 'regM' | 'simM' | 'simPC', i: number) {
  if (type === 'regM') {
    regImagesM.value.splice(i, 1)
  } else if (type === 'regPC') {
    regImagesPC.value.splice(i, 1)
  } else if (type === 'simPC') {
    simImagesPC.value.splice(i, 1)
  } else {
    simImagesM.value.splice(i, 1)
  }
}

function copyImage(data: string) {
  console.log(data)
}

function copyResult(result: string) {
  console.log(result)
}
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
      <RegImage
        v-for="(img, i) in regImagesPC"
        :key="i"
        :data="img"
        :result="regResult[i] || ''"
        @del-image="delImage('regPC', i)"
        @copy-result="(result) => copyResult(result)"
      />
    </div>
    <div mxauto my2 w90vw h2 bg-gray300 rounded></div>
    <div my2 h25vh flex of-auto>
      <SimpleImage
        v-for="(img, i) in simImagesPC"
        :key="i"
        :data="img"
        @del-image="delImage('simPC', i)"
      />
    </div>
  </div>
  <div class="lg:hidden" h100vh flex="~ col" justify-evenly>
    <div h45vh flex="~ col" justify-evenly items-center>
      <AddImage
        :text="'需识别的图片'"
        :type="'reg'"
        @add-image="(e) => addImageM('regM', e)"
      />
      <div my2 p3 w90vw h25vh b flex of-auto>
        <SimpleImage
          v-for="(img, i) in regImagesM"
          :key="i"
          :data="img"
          @del-image="delImage('regM', i)"
        />
      </div>
    </div>
    <div mxauto my2 w90vw h2 bg-gray300 rounded />
    <div h45vh flex="~ col" justify-evenly items-center of-hidden>
      <AddImage
        :text="'不需识别的图片'"
        :type="'sim'"
        @add-image="(e) => addImageM('simM', e)"
      />
      <div my2 p3 w90vw h25vh b flex of-auto>
        <SimpleImage
          v-for="(img, i) in simImagesM"
          :key="i"
          :data="img"
          @del-image="delImage('simM', i)"
          @copy-image="(data) => copyImage(data)"
        />
      </div>
    </div>
  </div>
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

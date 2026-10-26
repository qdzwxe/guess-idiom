<script setup>
import HelloWorld from './components/HelloWorld.vue'
import Block from './components/Block.vue'
import find from './components/find.js'

const type = ['字', '声', '韵', '调'];
const check = [
  ['', '', '', ''],
  ['', '', '', ''],
  ['', '', '', ''],
  ['', '', '', '']
];

const ban = [];

</script>

<template>
  <div v-for="(c, i) in type">
    <span>{{ c }}:</span>
    <Block v-for="j in 4" v-model="check[i][j - 1]"></Block>
    <input v-model="ban[i]">
    <!-- <button @click="check[i] = ['', '', '', '']">Clear</button> -->
  </div>
  <button @click="console.log(check, ban, find(check, ban))">Find</button>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

button {
  border-color: black;
}
</style>

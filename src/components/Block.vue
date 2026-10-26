<script setup>
import { ref } from 'vue'

let value = ref('');
//  maxlength="1"
</script>

<template>
    <input v-model="value" placeholder="*">
</template>

<style scoped>
* {
    width: 50px;
    height: 50px;
    font-size: 1.6rem;
    color: #fff;
    border-radius: 5px;
    background-color: #3A5E37;
    margin: 10px;
}
</style>

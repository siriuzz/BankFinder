<template>
  <v-app>
    <!-- <v-container fluid> -->
    <default-bar />
    <View />

    <!-- </v-container> -->
    <default-footer class="d-block" />
  </v-app>
</template>

<script setup>
import DefaultBar from './AppBar.vue'
import View from './View.vue'
import DefaultFooter from './Footer.vue'
</script>

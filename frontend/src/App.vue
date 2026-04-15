<template>
  <div id="app-container">
    <!-- Flowing Cloud Background (Upper Part) -->
    <FlowingCloudBg />

    <!-- Router View with Transition -->
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import FlowingCloudBg from './components/FlowingCloudBg.vue'
</script>

<style>
#app-container {
  min-height: 100vh;
  background: var(--bg-base);
  position: relative;
}

/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.4s var(--ease-in-out);
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>

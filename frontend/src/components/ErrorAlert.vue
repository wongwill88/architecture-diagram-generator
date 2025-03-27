<template>
  <div v-if="error" class="glass-effect p-4 mb-6 rounded-xl relative overflow-hidden">
    <div class="neon-border absolute inset-0 opacity-30" style="border-color: #ef4444;"></div>
    <div class="flex z-10 relative">
      <div class="flex-shrink-0">
        <div class="w-4 h-4 rounded-full bg-red-500 animate-pulse"></div>
      </div>
      <div class="ml-3">
        <p class="text-base text-red-400 sci-fi-font">{{ error }}</p>
      </div>
    </div>
    <div class="absolute right-0 top-0 h-full w-16" style="background: linear-gradient(90deg, transparent, rgba(239, 68, 68, 0.2));"></div>
  </div>
</template>

<script setup>
defineProps({
  error: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.animate-pulse {
  animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style> 
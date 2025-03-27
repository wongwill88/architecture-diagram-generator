<template>
  <div v-if="isLoading" class="glass-effect p-6 rounded-lg">
    <div class="relative">
      <!-- 科技感加载动画 -->
      <div class="flex flex-col items-center">
        <div class="sci-fi-font text-blue-400 mb-4 text-center">生成中...</div>
        
        <!-- 动态加载动画 -->
        <div class="relative w-24 h-24 mb-6">
          <div class="absolute inset-0 border-2 border-blue-500 rounded-full animate-spin" style="border-top-color: transparent; animation-duration: 1.5s;"></div>
          <div class="absolute inset-2 border-2 border-purple-500 rounded-full animate-spin" style="border-bottom-color: transparent; animation-duration: 2s;"></div>
          <div class="absolute inset-4 border-2 border-cyan-500 rounded-full animate-spin" style="border-left-color: transparent; animation-duration: 2.5s;"></div>
          <div class="absolute inset-6 border-2 border-blue-400 rounded-full animate-spin" style="border-right-color: transparent; animation-duration: 3s;"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
          </div>
        </div>
        
        <!-- 加载进度条 -->
        <div class="w-full h-1 bg-slate-800 rounded-full overflow-hidden mb-6">
          <div class="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full loading-bar"></div>
        </div>
        
        <!-- 加载文本 -->
        <div class="grid grid-cols-3 gap-4 w-full max-w-md">
          <div v-for="i in 6" :key="i" class="h-4 bg-slate-800 rounded loading-block" :style="{ animationDelay: `${i * 0.1}s` }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isLoading: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

@keyframes loading {
  0% {
    width: 0%;
  }
  50% {
    width: 70%;
  }
  100% {
    width: 100%;
  }
}

@keyframes block-loading {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-spin {
  animation: spin 2s linear infinite;
}

.animate-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.loading-bar {
  animation: loading 2s ease-in-out infinite;
}

.loading-block {
  animation: block-loading 1.5s ease-in-out infinite;
}
</style> 
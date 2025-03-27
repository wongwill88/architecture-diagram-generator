<template>
  <header class="glass-effect py-3 px-6">
    <div class="relative w-full">
      <!-- 居中标题容器 -->
      <div class="flex justify-center items-center w-full">
        <div class="flex items-center space-x-3">
          <!-- 标志图标 -->
          <div class="w-8 h-8 rounded-full neon-border flex items-center justify-center">
            <span class="text-sm font-bold text-gradient">AI</span>
          </div>
          <!-- 标题 -->
          <h1 class="text-2xl sci-fi-font neon-text text-center">架构图生成器</h1>
        </div>
      </div>
      
      <!-- 装饰元素（两侧对称） -->
      <div class="absolute left-0 top-1/2 transform -translate-y-1/2 hidden md:flex items-center space-x-4">
        <div class="h-2 w-2 rounded-full bg-blue-400 animate-pulse"></div>
        <div class="h-2 w-16 neon-border"></div>
      </div>
      <div class="absolute right-0 top-1/2 transform -translate-y-1/2 hidden md:flex items-center space-x-4">
        <div class="h-2 w-16 neon-border"></div>
        <div class="h-2 w-2 rounded-full bg-purple-400 animate-pulse"></div>
      </div>
    </div>
  </header>
</template>

<style scoped>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>

<script setup>
// 头部组件逻辑
</script> 
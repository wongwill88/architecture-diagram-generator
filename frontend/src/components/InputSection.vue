<template>
  <div class="glass-effect rounded-2xl shadow-2xl p-8 mb-8 transform hover:scale-[1.01] transition-all duration-300">
    <div class="mb-6">
      <label class="block text-gray-700 text-lg font-medium mb-3 flex items-center">
        <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
        </svg>
        系统架构描述
      </label>
      
      <textarea
        v-model="description"
        class="w-full p-4 bg-white/80 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 text-gray-700 placeholder-gray-500 text-lg"
        rows="4"
        placeholder="请描述您的系统架构，例如：&#10;系统包含一个前端应用，使用Vue.js开发，通过REST API与后端服务通信。&#10;后端服务使用Python FastAPI框架，连接PostgreSQL数据库。&#10;系统使用Redis作为缓存层，使用Nginx作为反向代理。"
      ></textarea>
      <div class="mt-2 text-sm text-gray-500 flex justify-between">
        <span>支持中文和英文描述</span>
        <span>{{ description.length }}/500</span>
      </div>
    </div>

    <!-- 示例按钮 -->
    <div class="flex space-x-4 mb-4">
      <button 
        @click="loadExample('simple')"
        class="px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200 transition-colors"
      >
        简单示例
      </button>
      <button 
        @click="loadExample('complex')"
        class="px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200 transition-colors"
      >
        复杂示例
      </button>
    </div>

    <button
      @click="generateDiagram"
      class="w-full py-4 px-6 bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 text-white rounded-xl hover:from-indigo-700 hover:via-purple-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-white transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg transform hover:scale-[1.02]"
      :disabled="isLoading"
    >
      <span v-if="!isLoading" class="flex items-center justify-center text-lg">
        <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
        生成架构图
      </span>
      <span v-else class="flex items-center justify-center text-lg">
        <svg class="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        生成中...
      </span>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['generate', 'loadExample'])

const description = ref('')

const generateDiagram = () => {
  emit('generate', description.value)
}

const loadExample = (type) => {
  emit('loadExample', type)
}
</script> 
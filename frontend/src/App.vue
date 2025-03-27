<template>
  <!-- 修改最外层容器 -->
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 relative">
    <!-- 动态背景 - 调整z-index -->
    <div class="tech-grid absolute inset-0 z-0"></div>
    
    <!-- 主要内容 - 确保在背景之上 -->
    <main class="relative z-10 min-h-[calc(100vh-4rem)] py-8">
      <div class="container mx-auto px-4 max-w-4xl">
        <!-- 标题区域 -->
        <div class="text-center mb-12">
          <h1 class="text-5xl font-bold mb-6">
            <span class="text-gradient">架构图</span> 生成器
          </h1>
          <p class="text-gray-600 text-xl">
            通过简单描述，快速生成专业的系统架构图
          </p>
        </div>
        
        <!-- 输入区域 -->
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

        <!-- 错误提示 -->
        <div v-if="error" class="glass-effect border-l-4 border-red-500 p-4 mb-8 rounded-xl">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-base text-red-600">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="isLoading" class="glass-effect rounded-2xl shadow-2xl p-8 mb-8">
          <div class="flex flex-col items-center justify-center py-12">
            <svg class="animate-spin h-12 w-12 text-indigo-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="text-lg text-gray-600">正在生成架构图，请稍候...</p>
          </div>
        </div>

        <!-- 结果区域 -->
        <div v-if="diagramHtml" class="glass-effect rounded-2xl shadow-2xl p-8 transform hover:scale-[1.01] transition-all duration-300">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-3xl font-semibold text-gray-800 flex items-center">
              <svg class="w-8 h-8 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              生成的架构图
            </h2>
            <button
              @click="exportAsImage"
              class="inline-flex items-center px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-xl hover:from-green-600 hover:to-emerald-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-white transition-all duration-200 shadow-lg"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
              </svg>
              导出为图片
            </button>
          </div>
          <div class="border border-gray-200 rounded-xl p-6 bg-white/80" ref="diagramContainer">
            <div v-html="diagramHtml" class="diagram-content"></div>
          </div>
        </div>
      </div>
    </main>
    
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import html2canvas from 'html2canvas'

const description = ref('')
const diagramHtml = ref('')
const isLoading = ref(false)
const error = ref('')
const diagramContainer = ref(null)

const generateDiagram = async () => {
  if (!description.value.trim()) {
    error.value = '请输入系统架构描述'
    return
  }

  isLoading.value = true
  error.value = ''
  diagramHtml.value = ''

  try {
    const response = await axios.post('/api/generate', {
      description: description.value
    })
    diagramHtml.value = response.data.html
  } catch (err) {
    error.value = '生成架构图时出错：' + (err.response?.data?.detail || err.message)
  } finally {
    isLoading.value = false
  }
}

const exportAsImage = async () => {
  if (!diagramContainer.value) return

  try {
    const canvas = await html2canvas(diagramContainer.value, {
      backgroundColor: '#ffffff',
      scale: 2
    })
    const link = document.createElement('a')
    link.download = 'architecture-diagram.png'
    link.href = canvas.toDataURL('image/png')
    link.click()
  } catch (err) {
    error.value = '导出图片时出错：' + err.message
  }
}

const loadExample = (type) => {
  const examples = {
    simple: `系统包含一个前端应用，使用Vue.js开发，通过REST API与后端服务通信。
后端服务使用Python FastAPI框架，连接PostgreSQL数据库。`,
    complex: `系统采用微服务架构，包含以下组件:
- 前端: Vue.js应用，通过API Gateway访问后端服务
- API Gateway: 使用Kong实现请求路由和认证
- 用户服务: 处理用户认证和权限管理
- 订单服务: 处理订单业务逻辑
- 支付服务: 集成第三方支付接口
- 数据库: 使用PostgreSQL存储业务数据
- 缓存: 使用Redis缓存热点数据
- 消息队列: 使用RabbitMQ处理异步任务`
  }
  description.value = examples[type]
}
</script>
<style>
.diagram-content {
  max-width: 100%;
  overflow-x: auto;
}

/* 自定义滚动条样式 */
.diagram-content::-webkit-scrollbar {
  height: 8px;
}

.diagram-content::-webkit-scrollbar-track {
  background: rgba(17, 24, 39, 0.1);
  border-radius: 4px;
}

.diagram-content::-webkit-scrollbar-thumb {
  background: rgba(99, 102, 241, 0.5);
  border-radius: 4px;
}

.diagram-content::-webkit-scrollbar-thumb:hover {
  background: rgba(99, 102, 241, 0.7);
}
</style>

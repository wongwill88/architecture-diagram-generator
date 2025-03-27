<template>
  <!-- 修改最外层容器 -->
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 relative">
    <!-- 动态背景 - 调整z-index -->
    <div class="tech-grid absolute inset-0 z-0"></div>
    
    <!-- 主要内容 - 确保在背景之上 -->
    <main class="relative z-10 min-h-[calc(100vh-4rem)] py-8">
      <div class="container mx-auto px-4 max-w-4xl">
        <Header />
        
        <InputSection 
          :is-loading="isLoading"
          @generate="handleGenerate"
          @load-example="handleLoadExample"
        />

        <ErrorAlert :error="error" />
        
        <LoadingSpinner :is-loading="isLoading" />
        
        <DiagramResult 
          :diagram-html="diagramHtml"
          @error="handleError"
        />
      </div>
    </main>
    
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Header from './components/Header.vue'
import InputSection from './components/InputSection.vue'
import ErrorAlert from './components/ErrorAlert.vue'
import LoadingSpinner from './components/LoadingSpinner.vue'
import DiagramResult from './components/DiagramResult.vue'

const diagramHtml = ref('')
const isLoading = ref(false)
const error = ref('')

const handleGenerate = async (description) => {
  if (!description.trim()) {
    error.value = '请输入系统架构描述'
    return
  }

  isLoading.value = true
  error.value = ''
  diagramHtml.value = ''

  try {
    const response = await axios.post('/api/generate', {
      description: description
    })
    diagramHtml.value = response.data.html
  } catch (err) {
    error.value = '生成架构图时出错：' + (err.response?.data?.detail || err.message)
  } finally {
    isLoading.value = false
  }
}

const handleLoadExample = (type) => {
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
  emit('update:description', examples[type])
}

const handleError = (message) => {
  error.value = message
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

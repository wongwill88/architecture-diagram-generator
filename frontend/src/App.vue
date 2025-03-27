<template>
  <!-- 修改最外层容器 -->
  <div class="min-h-screen">
    <!-- 背景层 -->
    <div class="stars-background"></div>
    <div class="earth-background"></div>
    <div class="earth-atmosphere"></div>
    <div class="earth-grid"></div>
    <div class="tech-grid"></div>
    <div class="cyber-particles"></div>
    
    <!-- 科技线条装饰 -->
    <div class="tech-line" style="top: 80px;"></div>
    <div class="tech-line" style="bottom: 40px;"></div>
    
    <!-- 主要内容 -->
    <main class="min-h-screen flex flex-col">
      <!-- 顶部导航 -->
      <Header class="z-20" />
      
      <!-- 主要内容区域 -->
      <div class="flex-1 container mx-auto px-6 py-8 z-10">
        <el-card class="box-card glass-effect">
          <template #header>
            <div class="flex items-center">
              <span class="text-lg neon-text sci-fi-font">系统架构描述</span>
            </div>
          </template>

          <!-- 输入和结果区域 -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- 左侧输入区域 -->
            <div>
              <InputSection 
                :is-loading="isLoading"
                v-model="description"
                @generate="handleGenerate"
                @load-example="handleLoadExample"
              />
            </div>
            
            <!-- 右侧结果区域 -->
            <div class="space-y-6">
              <ErrorAlert :error="error" />
              <LoadingSpinner :is-loading="isLoading" />
              <DiagramResult 
                :diagram-html="diagramHtml"
                @error="handleError"
              />
            </div>
          </div>
        </el-card>
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
const description = ref('')

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
  description.value = examples[type]
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
  background: rgba(15, 23, 42, 0.7);
  border-radius: 4px;
}

.diagram-content::-webkit-scrollbar-thumb {
  background: rgba(56, 189, 248, 0.7);
  border-radius: 4px;
}

.diagram-content::-webkit-scrollbar-thumb:hover {
  background: rgba(56, 189, 248, 1);
}
</style>

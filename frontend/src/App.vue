<template>
  <div class="app-container">
    <el-container>
      <el-header height="80px">
        <div class="header-content">
          <h1 class="app-title">架构图生成器</h1>
          <p class="app-subtitle">基于AI的系统架构图可视化工具</p>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <el-col :span="12">
            <InputSection 
              :is-loading="isLoading"
              :example-text="exampleText"
              @generate="handleGenerate"
              @load-example="handleLoadExample"
            />
          </el-col>
          <el-col :span="12">
            <OutputSection 
              :diagram-html="diagramHtml" 
              :is-loading="isLoading"
            />
          </el-col>
        </el-row>
      </el-main>
      
      <el-footer height="60px">
        <p>© 2023 架构图生成器 | 使用 Vue.js + Element Plus + DeepSeek API 构建</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import InputSection from './components/InputSection.vue'
import OutputSection from './components/OutputSection.vue'

const diagramHtml = ref('')
const isLoading = ref(false)
const exampleText = ref('')

const handleGenerate = async (description) => {
  if (!description.trim()) {
    ElMessage.warning('请输入系统架构描述')
    return
  }
  
  isLoading.value = true
  const loadingInstance = ElLoading.service({
    lock: true,
    text: '正在生成架构图...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  
  try {
    const response = await fetch('http://localhost:8001/generate-diagram', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ description })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    diagramHtml.value = data.html
    ElMessage.success('架构图生成成功')
  } catch (error) {
    console.error('Error generating diagram:', error)
    ElMessage.error('生成架构图失败，请重试')
  } finally {
    isLoading.value = false
    loadingInstance.close()
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
  exampleText.value = examples[type]
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.el-header {
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header-content {
  text-align: center;
}

.app-title {
  margin: 0;
  font-size: 28px;
}

.app-subtitle {
  margin: 5px 0 0;
  font-size: 16px;
  opacity: 0.9;
}

.el-main {
  padding: 20px;
}

.el-footer {
  text-align: center;
  color: #909399;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1px solid #e4e7ed;
  background-color: white;
}
</style>

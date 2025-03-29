<template>
  <div class="app-container">
    <el-container>
      <el-header height="80px">
        <div class="header-content">
          <h1 class="app-title">智能图表生成器</h1>
          <p class="app-subtitle">基于AI的系统图表可视化工具</p>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <el-col :span="12">
            <InputSection 
              ref="inputSection"
              @generate="handleGenerate" 
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
        <p>Powered by Vue.js, Element Plus & Mermaid.js</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import InputSection from './components/InputSection.vue'
import OutputSection from './components/OutputSection.vue'

const inputSection = ref(null)
const diagramHtml = ref('')
const isLoading = ref(false)

const handleGenerate = async (data) => {
  const { type, description } = data
  
  isLoading.value = true
  if (inputSection.value) {
    inputSection.value.isLoading = true
  }
  
  const loadingInstance = ElLoading.service({
    lock: true,
    text: '正在生成图表...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  
  try {
    const response = await fetch('/api/generate-diagram', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ type, description })
    })
    
    console.log('Response status:', response.status)
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('Error response:', errorText)
      throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`)
    }
    
    const data = await response.json()
    diagramHtml.value = data.html
    ElMessage.success('图表生成成功')
  } catch (error) {
    console.error('Error generating diagram:', error)
    ElMessage.error(`生成图表失败: ${error.message}`)
  } finally {
    isLoading.value = false
    if (inputSection.value) {
      inputSection.value.isLoading = false
    }
    loadingInstance.close()
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.el-header {
  background-color: white;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
}

.header-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.app-title {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.app-subtitle {
  margin: 5px 0 0;
  font-size: 14px;
  color: #909399;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
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

<template>
  <div class="app-container">
    <el-container>
      <el-header height="80px">
        <div class="header-content">
          <h1 class="app-title">智能架构图生成器</h1>
          <p class="app-subtitle">基于AI的系统架构图可视化工具</p>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card class="input-section" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>系统描述</span>
                </div>
              </template>
              
              <el-form>
                <el-form-item label="描述内容">
                  <el-input
                    v-model="description"
                    type="textarea"
                    :rows="8"
                    placeholder="请输入系统描述..."
                    resize="vertical"
                  />
                </el-form-item>
                
                <el-form-item>
                  <el-button 
                    type="primary" 
                    @click="handleGenerate" 
                    :loading="isLoading"
                    style="width: 100%"
                  >
                    生成架构图
                  </el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </el-col>
          
          <el-col :span="12">
            <el-card class="output-section" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>架构图预览</span>
                </div>
              </template>
              
              <div class="diagram-container">
                <div v-if="isLoading" class="loading-container">
                  <el-icon class="loading-icon"><Loading /></el-icon>
                  <p>正在生成架构图，请稍候...</p>
                </div>
                
                <div v-else-if="!diagramHtml" class="empty-state">
                  <el-empty description="输入系统架构描述并点击生成按钮" />
                </div>
                
                <div v-else class="diagram-content" v-html="diagramHtml"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

const description = ref('')
const diagramHtml = ref('')
const isLoading = ref(false)

const handleGenerate = async () => {
  if (!description.value.trim()) {
    ElMessage.warning('请输入系统描述')
    return
  }
  
  isLoading.value = true
  const loadingInstance = ElLoading.service({
    lock: true,
    text: '正在生成架构图...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  
  try {
    const response = await fetch('/api/generate-diagram', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ description: description.value })
    })
    
    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`)
    }
    
    const result = await response.json()
    
    if (result.html) {
      diagramHtml.value = result.html
      ElMessage.success('架构图生成成功')
    } else {
      throw new Error('API返回的数据格式不正确')
    }
  } catch (error) {
    console.error('Error generating diagram:', error)
    ElMessage.error(`生成架构图失败: ${error.message}`)
  } finally {
    isLoading.value = false
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

.input-section, .output-section {
  height: 100%;
}

.card-header {
  font-weight: bold;
}

.diagram-container {
  min-height: 400px;
  background-color: #f9f9f9;
  border-radius: 4px;
  overflow: auto;
  padding: 20px;
}

.diagram-content {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  overflow: hidden;
  padding: 20px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.loading-icon {
  font-size: 40px;
  margin-bottom: 10px;
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

:deep(.architecture-diagram) {
  width: 100%;
  min-height: 300px;
}
</style>

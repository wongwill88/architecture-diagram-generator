<template>
  <el-card class="output-section" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>架构图预览</span>
        <el-button 
          type="success" 
          plain 
          size="small" 
          @click="exportImage" 
          :disabled="!diagramHtml || isLoading"
        >
          导出为图片
        </el-button>
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
      
      <div v-else ref="diagramRef" class="diagram-content" v-html="sanitizedHtml"></div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import html2canvas from 'html2canvas'

const props = defineProps({
  diagramHtml: {
    type: String,
    default: ''
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const diagramRef = ref(null)

// 计算属性，处理HTML内容
const sanitizedHtml = computed(() => {
  if (!props.diagramHtml) return ''
  return props.diagramHtml
})

// 监听HTML变化，初始化mermaid
watch(() => props.diagramHtml, (newVal) => {
  if (newVal) {
    // 使用setTimeout确保DOM已更新
    setTimeout(() => {
      if (window.mermaid) {
        try {
          window.mermaid.init(undefined, document.querySelectorAll('.mermaid'))
        } catch (error) {
          console.error('Mermaid initialization error:', error)
        }
      }
    }, 100)
  }
})

// 组件挂载时加载mermaid.js
onMounted(() => {
  if (!window.mermaid) {
    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js'
    script.onload = () => {
      window.mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        flowchart: {
          useMaxWidth: false,
          htmlLabels: true,
          curve: 'basis'
        }
      })
      
      if (props.diagramHtml) {
        setTimeout(() => {
          try {
            window.mermaid.init(undefined, document.querySelectorAll('.mermaid'))
          } catch (error) {
            console.error('Mermaid initialization error:', error)
          }
        }, 100)
      }
    }
    document.head.appendChild(script)
  }
})

const exportImage = async () => {
  if (!diagramRef.value) return
  
  try {
    // 确保mermaid图表已完全渲染
    if (window.mermaid) {
      try {
        await window.mermaid.init(undefined, document.querySelectorAll('.mermaid'))
      } catch (error) {
        console.error('Mermaid initialization error during export:', error)
      }
    }
    
    // 等待一小段时间确保渲染完成
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const canvas = await html2canvas(diagramRef.value, {
      backgroundColor: '#ffffff',
      scale: 2,
      logging: false,
      useCORS: true
    })
    
    const link = document.createElement('a')
    link.download = `架构图_${new Date().toISOString().slice(0, 10)}.png`
    link.href = canvas.toDataURL('image/png')
    link.click()
    
    ElMessage.success('图片导出成功')
  } catch (error) {
    console.error('Error exporting image:', error)
    ElMessage.error('图片导出失败，请重试')
  }
}
</script>

<style scoped>
.output-section {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.diagram-container {
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9f9f9;
  border-radius: 4px;
  overflow: auto;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.loading-icon {
  font-size: 40px;
  margin-bottom: 10px;
  animation: rotate 2s linear infinite;
}

.empty-state {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
}

.diagram-content {
  width: 100%;
  padding: 20px;
  background-color: white;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style> 
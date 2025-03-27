<template>
  <div v-if="diagramHtml">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg sci-fi-font neon-text">生成的架构图</h3>
      <el-button
        @click="exportAsImage"
        type="primary"
        :icon="Download"
        class="neon-border"
        plain
      >
        导出为图片
      </el-button>
    </div>
    <div class="glass-effect p-1 rounded-lg">
      <div class="neon-border rounded-lg" style="padding: 1px;">
        <div ref="diagramContainer" class="relative rounded-lg bg-slate-900">
          <div v-html="diagramHtml" class="diagram-content"></div>
          <div class="absolute top-2 left-2 w-2 h-2 rounded-full bg-blue-400 animate-pulse"></div>
          <div class="absolute top-2 right-2 w-2 h-2 rounded-full bg-purple-400 animate-pulse"></div>
          <div class="absolute bottom-2 left-2 w-2 h-2 rounded-full bg-blue-400 animate-pulse"></div>
          <div class="absolute bottom-2 right-2 w-2 h-2 rounded-full bg-purple-400 animate-pulse"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import html2canvas from 'html2canvas'
import { Download } from '@element-plus/icons-vue'

const props = defineProps({
  diagramHtml: {
    type: String,
    default: ''
  }
})

const diagramContainer = ref(null)

const exportAsImage = async () => {
  if (!diagramContainer.value) return

  try {
    const canvas = await html2canvas(diagramContainer.value, {
      backgroundColor: '#0f172a',
      scale: 2
    })
    const link = document.createElement('a')
    link.download = 'architecture-diagram.png'
    link.href = canvas.toDataURL('image/png')
    link.click()
  } catch (err) {
    emit('error', '导出图片时出错：' + err.message)
  }
}

defineEmits(['error'])
</script>

<style scoped>
.diagram-content {
  max-width: 100%;
  overflow-x: auto;
  padding: 2rem;
  border-radius: 0.5rem;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style> 
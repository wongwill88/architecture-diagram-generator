<template>
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
</template>

<script setup>
import { ref } from 'vue'
import html2canvas from 'html2canvas'

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
      backgroundColor: '#ffffff',
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
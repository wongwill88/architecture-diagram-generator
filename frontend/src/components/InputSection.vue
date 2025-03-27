<template>
  <div class="h-full flex flex-col glass-effect rounded-lg">
    <!-- 主要内容区域 -->
    <div class="flex-1 p-6">
      <div class="flex flex-col h-full">
        <div class="flex justify-between mb-2">
          <div class="text-sm text-blue-300 flex items-center">
            <div class="h-1.5 w-1.5 rounded-full bg-blue-400 mr-2"></div>
            <span>{{ description.length }} 字符</span>
            <span class="mx-2">|</span>
            <span>中/英文</span>
          </div>
          <div class="flex items-center">
            <div class="h-1 w-8 neon-border mr-2"></div>
            <div class="h-1.5 w-1.5 rounded-full bg-purple-400"></div>
          </div>
        </div>
        
        <el-input
          v-model="description"
          type="textarea"
          :rows="12"
          placeholder="请描述您的系统架构，例如：
系统包含一个前端应用，使用Vue.js开发，通过REST API与后端服务通信。
后端服务使用Python FastAPI框架，连接PostgreSQL数据库。
系统使用Redis作为缓存层，使用Nginx作为反向代理。"
          resize="none"
          class="mb-4 flex-1 neon-border"
          :disabled="isLoading"
        />
        
        <div class="flex justify-between items-center mb-4">
          <div class="space-x-2">
            <el-button type="text" @click="loadExample('simple')" class="neon-text text-xs">简单实例</el-button>
            <el-button type="text" @click="loadExample('complex')" class="neon-text text-xs">复杂实例</el-button>
          </div>
        </div>

        <div class="flex justify-end">
          <el-button
            @click="generateDiagram"
            type="primary"
            :loading="isLoading"
            :disabled="!description.trim()"
            class="w-32 neon-border sci-fi-font"
          >
            <span v-if="isLoading">
              <span class="inline-block w-1 h-1 bg-blue-300 rounded-full animate-pulse mr-0.5"></span>
              <span class="inline-block w-1 h-1 bg-blue-300 rounded-full animate-pulse mr-0.5" style="animation-delay: 0.2s"></span>
              <span class="inline-block w-1 h-1 bg-blue-300 rounded-full animate-pulse" style="animation-delay: 0.4s"></span>
            </span>
            <span v-else>生成架构图</span>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  },
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['generate', 'loadExample', 'update:modelValue'])

const description = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const generateDiagram = () => {
  emit('generate', description.value)
}

const loadExample = (type) => {
  emit('loadExample', type)
}
</script>

<style scoped>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.animate-pulse {
  animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style> 
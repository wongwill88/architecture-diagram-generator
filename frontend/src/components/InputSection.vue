<template>
  <el-card class="input-section" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>系统架构描述</span>
        <div class="example-buttons">
          <el-button type="primary" plain size="small" @click="loadExample('simple')">
            简单示例
          </el-button>
          <el-button type="primary" plain size="small" @click="loadExample('complex')">
            复杂示例
          </el-button>
        </div>
      </div>
    </template>
    
    <el-form>
      <el-form-item>
        <el-input
          v-model="description"
          type="textarea"
          :rows="10"
          placeholder="请输入系统架构描述，例如：系统包含一个前端应用，使用Vue.js开发，通过REST API与后端服务通信..."
          resize="none"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button 
          type="primary" 
          :loading="isLoading" 
          @click="generateDiagram"
          :disabled="!description.trim()"
          size="large"
          style="width: 100%"
        >
          {{ isLoading ? '生成中...' : '生成架构图' }}
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  },
  exampleText: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['generate', 'load-example'])
const description = ref('')

watch(() => props.exampleText, (newValue) => {
  if (newValue) {
    description.value = newValue
  }
})

const generateDiagram = () => {
  if (description.value.trim()) {
    emit('generate', description.value)
  }
}

const loadExample = (type) => {
  emit('load-example', type)
}
</script>

<style scoped>
.input-section {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.example-buttons {
  display: flex;
  gap: 10px;
}
</style> 
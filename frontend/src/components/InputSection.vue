<template>
  <el-card class="input-section" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>系统描述</span>
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
      <el-form-item label="图表类型">
        <el-select v-model="diagramType" placeholder="请选择图表类型" style="width: 100%">
          <el-option label="架构图" value="architecture" />
          <el-option label="时序图" value="sequence" />
          <el-option label="流程图" value="flowchart" />
          <el-option label="用例图" value="usecase" />
          <el-option label="ER图" value="er" />
          <el-option label="类图" value="class" />
        </el-select>
      </el-form-item>

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
          生成图表
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const description = ref('')
const diagramType = ref('architecture')
const isLoading = ref(false)

const emit = defineEmits(['generate'])

const examples = {
  simple: {
    type: 'architecture',
    description: '一个简单的网站系统，包含前端、后端API和数据库三个主要组件。'
  },
  complex: {
    type: 'architecture',
    description: '一个电商系统，包含用户服务、订单服务、支付服务、商品服务、库存服务，以及对应的数据库。服务之间通过消息队列通信。'
  }
}

const loadExample = (type) => {
  const example = examples[type]
  description.value = example.description
  diagramType.value = example.type
}

const handleGenerate = () => {
  if (!description.value.trim()) {
    ElMessage.warning('请输入系统描述')
    return
  }
  
  emit('generate', {
    type: diagramType.value,
    description: description.value
  })
}

defineExpose({
  isLoading
})
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
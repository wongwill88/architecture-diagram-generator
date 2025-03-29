<template>
  <el-container>
    <el-aside width="300px">
      <design-templates />
      <design-history />
    </el-aside>
    
    <el-main>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="图表设计" name="diagram">
          <diagram-editor 
            v-model="currentDesign"
            :context="designContext"
            @analyze="handleAnalyze"
          />
        </el-tab-pane>
        
        <el-tab-pane label="代码预览" name="code">
          <code-preview 
            :design="currentDesign"
            :language="selectedLanguage"
          />
        </el-tab-pane>
        
        <el-tab-pane label="设计分析" name="analysis">
          <design-analysis 
            :design="currentDesign"
            :analysis="analysisResult"
          />
        </el-tab-pane>
      </el-tabs>
    </el-main>
    
    <el-aside width="300px">
      <design-inspector 
        v-model="currentDesign"
        @update:style="updateStyle"
      />
      <design-suggestions 
        :suggestions="suggestions"
        @apply="applySuggestion"
      />
    </el-aside>
  </el-container>
</template> 
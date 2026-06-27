<template>
  <el-avatar :size="size">
    <el-icon><UserFilled /></el-icon>
  </el-avatar>
</template>

<script setup lang="ts">
import { UserFilled } from '@element-plus/icons-vue'

defineProps<{ size?: number }>()
</script>
<template>
  <div class="filter-tags">
    <div class="tags-wrapper">
      <button
        v-for="tag in visibleTags"
        :key="tag.value"
        :class="['filter-chip', { active: isSelected(tag.value) }]"
        @click="toggle(tag.value)"
      >
        <span>{{ tag.label }}</span>
        <el-icon v-if="isSelected(tag.value)" :size="14" class="check-icon"><Check /></el-icon>
      </button>

      <el-dropdown v-if="collapsedTags.length > 0" trigger="click">
        <button class="filter-chip more-chip">
          更多
          <el-icon :size="14"><ArrowDown /></el-icon>
        </button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item
              v-for="tag in collapsedTags"
              :key="tag.value"
              :class="{ 'is-active': isSelected(tag.value) }"
              @click="toggle(tag.value)"
            >
              {{ tag.label }}
              <el-icon v-if="isSelected(tag.value)" :size="14"><Check /></el-icon>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Check, ArrowDown } from '@element-plus/icons-vue'

interface TagOption {
  label: string
  value: string
}

const props = withDefaults(defineProps<{
  options: TagOption[]
  modelValue: string[]
  maxVisible?: number
}>(), {
  maxVisible: 5,
})

const emit = defineEmits<{
  'update:modelValue': [value: string[]]
}>()

const visibleTags = computed(() => props.options.slice(0, props.maxVisible))
const collapsedTags = computed(() => props.options.slice(props.maxVisible))

function isSelected(value: string) {
  return props.modelValue.includes(value)
}

function toggle(value: string) {
  const current = [...props.modelValue]
  const idx = current.indexOf(value)
  if (idx >= 0) {
    current.splice(idx, 1)
  } else {
    current.push(value)
  }
  emit('update:modelValue', current)
}
</script>

<style scoped lang="scss">
.filter-tags {
  overflow: hidden;
}

.tags-wrapper {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 16px;
  background: var(--color-bg-alt);
  border: 1px solid var(--color-border-light);
  border-radius: 20px;
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-family: var(--font-family);
  transition: all var(--transition-base);
  white-space: nowrap;

  &:hover {
    border-color: var(--color-primary);
    color: var(--color-primary);
  }

  &:active {
    transform: scale(0.96);
  }

  &.active {
    background: var(--color-primary);
    border-color: var(--color-primary);
    color: #fff;

    &:hover {
      background: var(--color-primary-dark);
    }
  }

  .check-icon {
    margin-left: 2px;
  }
}

.more-chip {
  color: var(--color-text-muted);
}
</style>

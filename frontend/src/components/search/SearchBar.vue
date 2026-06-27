<template>
  <div class="search-bar" ref="searchBarRef">
    <div class="search-wrapper">
      <span class="search-icon">
        <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
      </span>
      <input v-model="keyword" class="search-input" placeholder="搜索景点、酒店、餐厅..." @keyup.enter="handleSearch" @input="handleSuggest" />
      <button class="search-btn" @click="handleSearch">
        <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
        搜索
      </button>
    </div>
    <Teleport to="body">
      <transition name="scale-fade">
        <div v-if="suggestions.length > 0" class="suggestions" :style="dropdownStyle">
          <div v-for="s in suggestions" :key="s" class="suggest-item" @click="selectSuggestion(s)">
            <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
            <span>{{ s }}</span>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useSearch } from '@/composables/useSearch'
const emit = defineEmits<{ search: [keyword: string] }>()
const { suggest } = useSearch()
const keyword = ref('')
const suggestions = ref<string[]>([])
const searchBarRef = ref<HTMLElement | null>(null)

const dropdownStyle = computed(() => {
  if (!searchBarRef.value) return {}
  const rect = searchBarRef.value.getBoundingClientRect()
  return {
    position: 'fixed' as const,
    top: rect.bottom + 8 + 'px',
    left: rect.left + 'px',
    width: rect.width + 'px',
  }
})

async function handleSuggest() {
  if (keyword.value.length < 2) { suggestions.value = []; return }
  suggestions.value = await suggest(keyword.value)
}
function selectSuggestion(text: string) { keyword.value = text; suggestions.value = []; handleSearch() }
function handleSearch() { if (keyword.value.trim()) { suggestions.value = []; emit('search', keyword.value.trim()) } }
</script>

<style scoped lang="scss">
$bg-deep: #0a0e1a;
$bg-elevated: #1a2235;
$brand-amber: #f59e0b;
$text-primary: #f1f5f9;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border: #1e293b;

.search-bar { position: relative; max-width: 640px; margin: 0 auto; }

.search-wrapper {
  display: flex; align-items: center;
  background: $bg-elevated; border: 1.5px solid $border;
  border-radius: 16px; padding: 5px 5px 5px 18px;
  transition: all 0.3s ease;
  &:focus-within { border-color: $brand-amber; box-shadow: 0 0 0 4px rgba(245,158,11,0.08); }
}

.search-icon { color: $text-muted; flex-shrink: 0; display: flex; }

.search-input {
  flex: 1; border: none; outline: none;
  font-size: 15px; font-family: inherit; color: $text-primary;
  padding: 14px 16px; background: transparent;
  &::placeholder { color: $text-muted; }
}

.search-btn {
  flex-shrink: 0; padding: 12px 28px;
  border: none; border-radius: 12px;
  font-size: 15px; font-weight: 600; font-family: inherit;
  cursor: pointer; color: #0f172a;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  box-shadow: 0 4px 16px rgba(245,158,11,0.25);
  display: flex; align-items: center; gap: 6px;
  transition: all 0.3s ease;
  &:hover { box-shadow: 0 6px 24px rgba(245,158,11,0.35); transform: translateY(-1px); }
}

.suggestions {
  background: $bg-elevated; border: 1px solid $border;
  border-radius: 14px; z-index: 1000;
  box-shadow: 0 12px 32px rgba(0,0,0,0.4);
  max-height: 360px;
  overflow-x: hidden;
  overflow-y: auto;

  // 自定义滚动条
  &::-webkit-scrollbar { width: 6px; }
  &::-webkit-scrollbar-track { background: transparent; }
  &::-webkit-scrollbar-thumb {
    background: $border; border-radius: 3px;
    &:hover { background: #334155; }
  }
}

.suggest-item {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 20px; cursor: pointer;
  font-size: 14px; color: $text-secondary;
  transition: all 0.15s;
  &:hover { background: rgba(245,158,11,0.06); color: $brand-amber; }
  &:not(:last-child) { border-bottom: 1px solid $border; }
}
</style>

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
    <transition name="suggest-draw">
      <div v-if="suggestions.length > 0" class="suggestions">
        <div v-for="(s, i) in suggestions" :key="s"
             class="suggest-item" @click="selectSuggestion(s)">
          <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
          <span>{{ s }}</span>
        </div>
        <div class="suggest-footer">共 {{ suggestions.length }} 个相关结果</div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useSearch } from '@/composables/useSearch'
import { searchAPI } from '@/api/search'
const emit = defineEmits<{ search: [keyword: string] }>()
const { suggest } = useSearch()
const keyword = ref('')
const suggestions = ref<string[]>([])
const searchBarRef = ref<HTMLElement | null>(null)

function closeSuggestions() { suggestions.value = [] }

let timer: ReturnType<typeof setTimeout> | null = null

async function handleSuggest() {
  const kw = keyword.value.trim()
  if (kw.length < 2) { suggestions.value = []; return }
  if (timer) clearTimeout(timer)
  timer = setTimeout(async () => {
    try {
      // ① 先调 suggest（快速补全）
      const list: string[] = await suggest(kw, 10)

      // ② 结果足够直接显示
      if (list.length >= 6) {
        suggestions.value = list
        return
      }

      // ③ 太少则直接调 API 补充 POI 名称（不经过 store，无副作用）
      const { data } = await searchAPI.searchPOI({ keyword: kw, page: 1, page_size: 12 })
      const items = data?.data?.items ?? []
      const extraNames = items
        .map((r: any) => r.name)
        .filter((n: string) => n && !list.includes(n))

      suggestions.value = [...list, ...extraNames].slice(0, 12)
    } catch (err) {
      // suggest 本身出错才清空；如果只是补充失败，上面已赋值了 list
      if (!suggestions.value.length) suggestions.value = []
    }
  }, 200)
}
function selectSuggestion(text: string) { keyword.value = text; suggestions.value = []; handleSearch() }
function handleSearch() { if (keyword.value.trim()) { suggestions.value = []; emit('search', keyword.value.trim()) } }

// 点击外部 / ESC 关闭下拉框
// 滚动时：仅当输入框为空时才关闭（有输入则保留建议供 ES 搜索）
let attached = false
function handleClickOutside(e: Event) {
  if (searchBarRef.value && !searchBarRef.value.contains(e.target as Node)) {
    closeSuggestions()
  }
}
function handleScroll() {
  if (!keyword.value.trim()) closeSuggestions()
}

onMounted(() => {
  if (!attached) {
    document.addEventListener('click', handleClickOutside)
    window.addEventListener('scroll', handleScroll, { passive: true })
    window.addEventListener('keydown', (e: KeyboardEvent) => {
      if (e.key === 'Escape') closeSuggestions()
    })
    attached = true
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped lang="scss">
$bg-warm: #FAF8F3;
$bg-oat: #F5F0E8;
$brand-brown: #A68B7A;
$brand-sage: #B8C4B8;
$text-primary: #3D3D3D;
$text-secondary: #6B6B6B;
$text-muted: #B8B0A8;
$border: #E8D5D0;

.search-bar { position: relative; max-width: 640px; margin: 0 auto; }

.search-wrapper {
  display: flex; align-items: center;
  background: $bg-oat; border: 1.5px solid $border;
  border-radius: 16px; padding: 5px 5px 5px 18px;
  transition: all 0.3s ease;
  &:focus-within { border-color: $brand-brown; box-shadow: 0 0 0 4px rgba(245,158,11,0.08); }
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
  position: absolute; top: calc(100% + 8px); left: 0;
  width: 100%; background: #fff; border: 1px solid $border;
  border-radius: 12px; z-index: 3000;
  box-shadow:
    0 8px 28px rgba(0,0,0,0.1),
    0 2px 6px rgba(0,0,0,0.04);
  max-height: 420px;
  overflow-y: auto;

  // 自定义滚动条
  &::-webkit-scrollbar { width: 5px; }
  &::-webkit-scrollbar-track { background: transparent; }
  &::-webkit-scrollbar-thumb {
    background: rgba($brand-brown, 0.22); border-radius: 3px;
    &:hover { background: rgba($brand-brown, 0.38); }
  }

  // 底部计数栏（粘在列表底部）
  .suggest-footer {
    position: sticky; bottom: 0;
    padding: 7px 14px; font-size: 11px;
    color: $text-muted; text-align: center;
    border-top: 1px solid rgba($border, 0.55);
    background: rgba($bg-warm, 0.85);
    backdrop-filter: blur(4px);
    margin-top: 2px;
  }
}

.suggest-item {
  display: flex; align-items: center; gap: 9px;
  padding: 10px 16px; cursor: pointer;
  font-size: 13.5px; color: $text-secondary;
  line-height: 1.35; transition: background-color 0.12s, color 0.12s;
  svg { flex-shrink: 0; color: $brand-brown; opacity: 0.4; transition: opacity 0.12s; }

  &:first-child { border-radius: 11px 11px 0 0; }
  &:last-child { border-radius: 0 0 11px 11px; }
  &:hover {
    background: rgba($bg-oat, 0.7); color: $text-primary;
    svg { opacity: 1; }
  }
}

// 下拉框过渡动画
.suggest-draw-enter-active { transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1); }
.suggest-draw-leave-active { transition: all 0.15s cubic-bezier(0.4, 0, 1, 1); }
.suggest-draw-enter-from {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}
.suggest-draw-leave-to {
  opacity: 0;
  transform: translateY(-4px) scale(0.98);
}
</style>

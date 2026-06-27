<template>
  <div class="chat-panel">
    <div class="chat-header">
      <div class="chat-header-left">
        <div class="ai-icon">
          <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/></svg>
        </div>
        <div>
          <div class="ai-name">AI 旅行助手</div>
          <div class="ai-status" :class="{ busy: generating }">
            {{ generating ? '正在规划...' : (difyOnline ? '在线 · Dify' : '在线 · 本地') }}
          </div>
        </div>
      </div>
      <button v-if="messages.length > 0" class="clear-btn" @click="clearChat">清空对话</button>
    </div>

    <div class="chat-messages" ref="messagesRef">
      <div v-if="messages.length === 0 && !generating" class="chat-welcome">
        <div class="welcome-icon">
          <svg viewBox="0 0 24 24" fill="currentColor" width="40" height="40"><path d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
        </div>
        <h3>你好！我是你的 AI 旅行助手</h3>
        <p>告诉我你的旅行需求，我将为你生成完美的行程方案</p>
      </div>

      <ChatMessage v-for="(msg, i) in messages" :key="i" :role="msg.role as 'user' | 'assistant'">
        {{ msg.content }}
        <!-- 动态重排备选方案卡片 -->
        <div v-if="msg.alternatives && msg.alternatives.length" class="replan-cards">
          <div
            v-for="(alt, ai) in msg.alternatives"
            :key="ai"
            class="plan-card"
            :class="{ 'plan-selected': msg.selectedPlan === ai }"
          >
            <div class="plan-card-header">
              <span class="plan-badge">{{ String.fromCharCode(65 + ai) }}</span>
              <span class="plan-title">{{ alt.title.replace(/^[^：:]+[：:]\s*/, '') || `方案${String.fromCharCode(65 + ai)}` }}</span>
            </div>
            <p class="plan-desc">{{ alt.description }}</p>
            <div v-if="alt.impact" class="plan-impact">
              <svg viewBox="0 0 16 16" fill="currentColor" width="13" height="13"><path d="M8 15A7 7 0 118 1a7 7 0 010 14zm0-1.5a5.5 5.5 0 100-11 5.5 5.5 0 000 11zM7.25 4.75v3h3v1.5h-4.5v-4.5h1.5z"/></svg>
              {{ alt.impact }}
            </div>
            <button
              class="plan-apply-btn"
              :class="{ 'plan-applied': msg.selectedPlan === ai }"
              :disabled="msg.selectedPlan === ai || msg.applying === ai"
              @click="applyPlan(alt, ai, i)"
            >
              <template v-if="msg.applying === ai">
                <span class="plan-btn-spinner"></span>应用中...
              </template>
              <template v-else-if="msg.selectedPlan === ai">✓ 已应用</template>
              <template v-else>应用此方案</template>
            </button>
          </div>
        </div>
      </ChatMessage>

      <StreamingIndicator v-if="generating" />

      <!-- Error message -->
      <div v-if="errorMsg" class="chat-error">
        <span>{{ errorMsg }}</span>
        <button @click="retryLast">重试</button>
      </div>
    </div>

    <QuickPrompts v-if="messages.length === 0 && !generating" @select="handleQuickPrompt" />

    <div class="chat-input-area">
      <div class="chat-input-row">
        <input
          v-model="input"
          class="chat-input-field"
          placeholder="描述你的旅行需求..."
          :disabled="generating"
          @keyup.enter="handleSend"
        />
        <button class="send-btn" :disabled="!input.trim() || generating" @click="handleSend">
          <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
        </button>
      </div>
      <p class="input-hint">按 Enter 发送，Shift+Enter 换行</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useItineraryGenerate } from '@/composables/useItineraryGenerate'
import { useItineraryStore } from '@/stores/itinerary'
import type { ItineraryResponse } from '@/types/itinerary'
import ChatMessage from './ChatMessage.vue'
import StreamingIndicator from './StreamingIndicator.vue'
import QuickPrompts from './QuickPrompts.vue'

const props = defineProps<{ query?: string }>()
const emit = defineEmits<{ generated: [ItineraryResponse] }>()

const { generate } = useItineraryGenerate()
const itineraryStore = useItineraryStore()
const { generating, currentItinerary } = storeToRefs(itineraryStore)
const input = ref('')
const messages = ref<(MessageData)[]>([])
const messagesRef = ref<HTMLElement | null>(null)
const errorMsg = ref('')
const lastQuery = ref('')
const difyOnline = ref(true)

interface MessageData {
  role: string
  content: string
  alternatives?: any[]
  selectedPlan?: number | null
  applying?: number | null
}

onMounted(() => {
  if (props.query) { input.value = props.query; handleSend() }
})

async function handleSend() {
  if (!input.value.trim() || generating.value) return
  errorMsg.value = ''
  const query = input.value.trim()
  lastQuery.value = query
  messages.value.push({ role: 'user', content: query })
  input.value = ''
  await nextTick(); scrollToBottom()

  try {
    const itineraryId = currentItinerary.value?.id
    console.log('[ChatPanel] 当前活跃行程ID:', itineraryId, 'query:', query)

    // ---- 用户发取消/调整类消息但无活跃行程 → 提示先生成 ----
    const CANCEL_ONLY = ['计划取消', '行程取消', '不要了', '算了算了', '不去了', '取消行程', '取消计划', '全部取消']
    const isCancelOnly = CANCEL_ONLY.some(p => query.includes(p))
    if (isCancelOnly && !itineraryId) {
      messages.value.push({
        role: 'assistant',
        content: '🔔 您当前没有活跃的行程计划。请先描述您的旅行需求，我将为您生成行程方案。',
      })
      return
    }

    // ---- 有活跃行程 + 检测到重排场景关键词 → 给用户明确提示 ----
    if (itineraryId) {
      const REPLAN_SCENARIOS = [
        '天气', '下雨', '下大雨', '暴雨', '太热', '太冷', '高温',
        '航班', '延误', '飞机', '身体', '不舒服', '生病', '健康',
        '取消', '去不了', '不行', '变更', '调整', '修改', '重排',
      ]
      if (REPLAN_SCENARIOS.some(s => query.includes(s))) {
        messages.value.push({
          role: 'assistant',
          content: '🔄 正在根据您的情况调整行程方案，请稍候...',
        })
      }
    }

    const result = await generate(query, itineraryId)
    console.log('[ChatPanel] 返回结果 type:', (result as any).type, 'dest:', result.destination)

    // 移除之前的"正在调整"提示消息（如果有）
    const lastMsg = messages.value[messages.value.length - 1]
    if (lastMsg && lastMsg.role === 'assistant' && lastMsg.content.includes('🔄 正在根据')) {
      messages.value.pop()
    }

    // 检查是否为动态重排响应（而非普通行程生成）
    if ((result as any).type === 'replan') {
      difyOnline.value = true
      const alternatives: any[] = (result as any).alternatives || []
      const msgData: MessageData = {
        role: 'assistant',
        content: `🔔 检测到行程变更需求，已为您生成 **${alternatives.length}** 套备选方案，请选择：`,
        alternatives,
        selectedPlan: null,
        applying: null,
      }
      messages.value.push(msgData)
      // 不 emit 'generated'，因为这不是新行程
    } else {
      // ---- 防止垃圾结果（目的地/标题为未知）显示在右侧 ----
      const dest = result.destination || ''
      const title = result.title || ''
      if (dest === '默认目的地' || dest === '未知' || title.includes('未知') || title.includes('未指定')) {
        difyOnline.value = true
        messages.value.push({
          role: 'assistant',
          content: '未能从您的描述中识别出明确的旅行目的地。请尝试更具体地描述，例如「我想去北京3天，预算3000元」。',
        })
        // 不 emit 'generated'，右侧保持空白
      } else {
        difyOnline.value = true
        messages.value.push({ role: 'assistant', content: `✅ 已为您生成行程方案「${result.title}」` })
        emit('generated', result)
      }
    }
  } catch (err: any) {
    difyOnline.value = false
    const detail = err?.response?.data?.detail || err?.message || '未知错误'
    errorMsg.value = `生成失败：${detail}（已使用本地引擎兜底，请检查 Dify 服务）`
    console.error('[ChatPanel] generate error:', err)
  }
  await nextTick(); scrollToBottom()
}

/** 应用选中的备选方案 */
async function applyPlan(alt: any, altIndex: number, msgIndex: number) {
  const msg = messages.value[msgIndex]
  if (!msg) return

  // 标记正在应用
  msg.applying = altIndex

  try {
    const itineraryId = currentItinerary.value?.id || ''

    // ---- 从当前活跃行程中提取关键上下文，构造 Dify 可解析的明确请求 ----
    const current = currentItinerary.value
    const dest = current?.destination || ''
    const daysCount = (current?.days && current.days.length > 0) ? current.days.length : 3
    const budget = current?.total_budget || current?.budget || 0

    let applyQuery: string
    if (dest && dest !== '默认目的地' && dest !== '未知') {
      // 有有效目的地 → 构造带完整上下文的请求，让 Dify 正确提取城市+天数+预算
      applyQuery = `重新规划我的${dest}${daysCount}日行程（总预算约${budget}元），调整原因：${alt.title}。具体要求：${alt.description}。请生成完整的${daysCount}天行程，包含每天的活动安排、餐厅和酒店推荐及价格明细。`
    } else {
      // 无有效目的地时用更直接的请求
      applyQuery = `请根据以下方案为我重新生成完整的旅行行程：【${alt.title}】${alt.description}。需要包含每天的具体活动、餐厅酒店推荐和详细价格预算。`
    }

    console.log('[ChatPanel] applyPlan query:', applyQuery.substring(0, 120))

    // 调用生成接口，让后端/Dify 根据选择的方案 + 原始行程上下文重新生成
    const result = await generate(applyQuery, itineraryId)

    // 更严格的结果校验 — 必须有实际的 days 数据
    const rDest = (result.destination || '').trim()
    const rTitle = (result.title || '').trim()
    const rDays = result.days
    const hasValidDays = Array.isArray(rDays) && rDays.length > 0

    if (
      !hasValidDays ||
      rDest === '默认目的地' ||
      rDest === '未知' ||
      !rDest ||
      rTitle.includes('未知') ||
      rTitle.includes('未指定') ||
      !rTitle
    ) {
      // 行程数据无效 — 不更新右侧面板，提示用户
      msg.applying = undefined
      console.warn('[ChatPanel] applyPlan 返回无效数据:', { dest: rDest, title: rTitle, daysLen: rDays?.length })
      messages.value.push({
        role: 'assistant',
        content: `⚠️ 应用「${alt.title}」时未能获取到有效的行程数据（可能 Dify 工作流暂时不可用）。建议：直接在输入框描述您的新需求，如「重新规划北京3天行程，把故宫调到第一天」，我将为您生成新方案。`,
      })
    } else {
      // 行程数据有效 — 标记选中状态并更新右侧面板
      msg.selectedPlan = altIndex
      msg.applying = undefined

      emit('generated', result)

      // 在对话中追加确认消息
      messages.value.push({
        role: 'assistant',
        content: `✅ 已应用 **${alt.title}**！行程已按此方案重新规划，共 ${rDays.length} 天，右侧预览已更新。`,
      })
    }
  } catch (err: any) {
    msg.applying = undefined
    console.error('[ChatPanel] applyPlan error:', err)
    messages.value.push({
      role: 'assistant',
      content: `❌ 应用方案时出错：${err?.message || '未知错误'}，请重试。`,
    })
  }

  await nextTick()
  scrollToBottom()
}

function retryLast() {
  if (lastQuery.value) {
    errorMsg.value = ''
    input.value = lastQuery.value
    // Remove the last user message before retrying
    if (messages.value.length > 0 && messages.value[messages.value.length - 1].role === 'user') {
      messages.value.pop()
    }
    handleSend()
  }
}

function handleQuickPrompt(prompt: string) { input.value = prompt; handleSend() }
function clearChat() { messages.value = []; errorMsg.value = '' }

function scrollToBottom() {
  if (messagesRef.value) messagesRef.value.scrollTop = messagesRef.value.scrollHeight
}
</script>

<style scoped lang="scss">
$bg-deep: #0a0e1a;
$bg-card: #111827;
$bg-elevated: #1a2235;
$brand-amber: #f59e0b;
$text-primary: #f1f5f9;
$text-secondary: #94a3b8;
$text-muted: #64748b;
$border: #1e293b;

.chat-panel {
  display: flex; flex-direction: column; height: 100%;
  background: $bg-card;
}

.chat-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid $border;
  flex-shrink: 0;
}

.chat-header-left { display: flex; align-items: center; gap: 12px; }

.ai-icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: #0f172a;
}

.ai-name { font-size: 14px; font-weight: 600; color: $text-primary; }
.ai-status { font-size: 11px; color: #10b981; &.busy { color: $brand-amber; } }

.clear-btn {
  padding: 6px 12px; border: 1px solid $border; border-radius: 8px;
  background: transparent; color: $text-muted; font-size: 12px;
  cursor: pointer; font-family: inherit;
  transition: all 0.2s;
  &:hover { border-color: $text-muted; color: $text-secondary; }
}

.chat-messages {
  flex: 1; overflow-y: auto; padding: 16px 20px;
}

.chat-welcome {
  text-align: center; padding: 40px 0;
  .welcome-icon { color: $brand-amber; opacity: 0.5; margin-bottom: 16px; }
  h3 { font-size: 16px; font-weight: 600; color: $text-primary; margin-bottom: 8px; }
  p { font-size: 13px; color: $text-muted; max-width: 260px; margin: 0 auto; line-height: 1.6; }
}

.chat-error {
  margin-top: 12px; padding: 10px 14px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: space-between;
  gap: 10px;
  span { font-size: 12px; color: #ef4444; flex: 1; }
  button {
    padding: 4px 12px; border: 1px solid rgba(239, 68, 68, 0.4);
    background: transparent; color: #ef4444; border-radius: 6px;
    font-size: 12px; cursor: pointer; font-family: inherit;
    &:hover { background: rgba(239, 68, 68, 0.15); }
  }
}

.chat-input-area {
  padding: 14px 20px; border-top: 1px solid $border; flex-shrink: 0;
}

.chat-input-row { display: flex; gap: 8px; align-items: center; }

.chat-input-field {
  flex: 1; padding: 12px 16px;
  background: $bg-elevated; border: 1.5px solid $border;
  border-radius: 12px; outline: none;
  font-size: 14px; color: $text-primary; font-family: inherit;
  transition: border-color 0.25s;
  &::placeholder { color: $text-muted; }
  &:focus { border-color: $brand-amber; }
  &:disabled { opacity: 0.5; }
}

.send-btn {
  width: 44px; height: 44px; flex-shrink: 0;
  border: none; border-radius: 12px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #0f172a;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.25s ease;
  &:hover:not(:disabled) { transform: scale(1.05); }
  &:disabled { opacity: 0.4; cursor: not-allowed; }
}

.input-hint { text-align: center; margin-top: 6px; font-size: 11px; color: $text-muted; }

/* ==================== 动态重排备选方案卡片 ==================== */
.replan-cards {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 14px;
}

.plan-card {
  background: $bg-elevated;
  border: 1.5px solid $border;
  border-radius: 12px;
  padding: 14px 16px;
  transition: all 0.25s ease;

  &:hover {
    border-color: rgba($brand-amber, 0.4);
    background: rgba($brand-amber, 0.04);
  }

  &.plan-selected {
    border-color: $brand-amber;
    background: rgba($brand-amber, 0.08);
    box-shadow: 0 0 0 1px rgba($brand-amber, 0.15), 0 4px 12px rgba(0, 0, 0, 0.2);
  }
}

.plan-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.plan-badge {
  width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 8px;
  font-size: 13px; font-weight: 700;
  color: #fff;
  flex-shrink: 0;
  /* 按方案A/B/C给不同颜色 */
  .plan-card:nth-child(1) & { background: linear-gradient(135deg, #3b82f6, #2563eb); }
  .plan-card:nth-child(2) & { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
  .plan-card:nth-child(3) & { background: linear-gradient(135deg, #06b6d4, #0891b2); }
  .plan-card:nth-child(n+4) & { background: linear-gradient(135deg, #64748b, #475569); }
}

.plan-title {
  font-size: 14px; font-weight: 600;
  color: $text-primary;
  line-height: 1.3;
}

.plan-desc {
  font-size: 13px; color: $text-secondary;
  line-height: 1.6;
  margin: 0 0 10px 0;
}

.plan-impact {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: $brand-amber;
  margin-bottom: 12px;

  svg { flex-shrink: 0; opacity: 0.85; }
}

.plan-apply-btn {
  display: inline-flex; align-items: center; justify-content: center;
  padding: 7px 18px; border: none; border-radius: 8px;
  font-size: 13px; font-weight: 500; font-family: inherit;
  cursor: pointer;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #0f172a;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);
  }

  &:active:not(:disabled) { transform: translateY(0); }

  &:disabled { cursor: default; }

  &.plan-applied {
    background: linear-gradient(135deg, #10b981, #059669);
    color: #fff;
  }
}

.plan-btn-spinner {
  width: 14px; height: 14px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: planSpin 0.6s linear infinite;
  margin-right: 5px;
}

@keyframes planSpin {
  to { transform: rotate(360deg); }
}
</style>

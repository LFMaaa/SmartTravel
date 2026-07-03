<template>
  <div class="review-section">
    <!-- 评分概览 -->
    <div class="review-summary">
      <div class="summary-score">
        <span class="score-num">{{ avgRating }}</span>
        <span class="score-max">/5</span>
      </div>
      <div class="summary-stars">
        <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= Math.round(avgRating) }">★</span>
      </div>
      <span class="summary-count">{{ total }} 条评价</span>
    </div>

    <!-- 发表评论 -->
    <div class="review-composer" v-if="isLoggedIn">
      <div class="composer-header">
        <span class="composer-label">{{ replyTo ? `回复 ${replyTo.user_name}` : '发表评价' }}</span>
        <button v-if="replyTo" class="cancel-reply-btn" @click="cancelReply">取消回复</button>
      </div>
      <!-- 评分（仅一级评论） -->
      <div v-if="!replyTo" class="composer-rating">
        <button v-for="i in 5" :key="i" class="rating-star" :class="{ on: rating >= i }" @click="rating = i">★</button>
        <span v-if="rating" class="rating-hint">{{ ratingText(rating) }}</span>
      </div>
      <div class="composer-input-row">
        <textarea
          v-model="content"
          class="composer-textarea"
          :placeholder="replyTo ? `回复 ${replyTo.user_name}...` : '分享你的体验...'"
          rows="2"
          maxlength="500"
        ></textarea>
        <button class="composer-submit" :disabled="!content.trim() || submitting" @click="submitReview">
          <svg v-if="!submitting" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
          <svg v-else class="spinner" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" stroke-linecap="round"/></svg>
        </button>
      </div>
      <!-- 提交反馈提示 -->
      <transition name="msg-fade">
        <div v-if="submitMsg === 'success'" class="submit-toast submit-toast--success">
          <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
          评价发布成功！
        </div>
        <div v-else-if="submitMsg === 'error'" class="submit-toast submit-toast--error">
          <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
          发布失败，请稍后重试
        </div>
      </transition>
    </div>
    <div v-else class="review-login-hint">
      <router-link to="/login">登录</router-link> 后即可发表评价
    </div>

    <!-- 评论列表 -->
    <div class="review-list" v-if="items.length > 0">
      <div v-for="item in items" :key="item.id" class="review-card">
        <div class="review-avatar">{{ item.user_name[0] }}</div>
        <div class="review-body">
          <div class="review-top">
            <span class="review-name">{{ item.user_name }}</span>
            <span v-if="item.rating" class="review-rating">
              <span v-for="i in 5" :key="i" class="mini-star" :class="{ on: i <= (item.rating || 0) }">★</span>
            </span>
            <span class="review-time">{{ formatTime(item.created_at) }}</span>
          </div>
          <p class="review-content">{{ item.content }}</p>
          <div class="review-actions">
            <button class="action-btn" @click="handleLike(item)">
              <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z"/></svg>
              {{ item.likes || '' }}
            </button>
            <button class="action-btn" @click="startReply(item)">回复</button>
            <button v-if="item.user_id === currentUserId" class="action-btn danger" @click="handleDelete(item.id)">删除</button>
          </div>

          <!-- 回复列表 -->
          <div v-if="item.replies && item.replies.length > 0" class="replies">
            <div v-for="reply in item.replies" :key="reply.id" class="reply-card">
              <div class="reply-avatar">{{ reply.user_name[0] }}</div>
              <div class="reply-body">
                <div class="reply-top">
                  <span class="reply-name">{{ reply.user_name }}</span>
                  <span v-if="reply.reply_to" class="reply-to">回复 {{ reply.reply_to }}</span>
                  <span class="reply-time">{{ formatTime(reply.created_at) }}</span>
                </div>
                <p class="reply-content">{{ reply.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="review-empty">
      <span>暂无评价，快来发表第一条评价吧</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { reviewAPI } from '@/api/review'
import { useUserStore } from '@/stores/user'
import type { ReviewItem } from '@/types/review'

const props = defineProps<{ poiId: string }>()

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)
const currentUserId = computed(() => userStore.user?.id || '')

const items = ref<ReviewItem[]>([])
const total = ref(0)
const avgRating = ref(0)
const content = ref('')
const rating = ref(0)
const submitting = ref(false)
const replyTo = ref<{ id: string; user_name: string } | null>(null)
const submitMsg = ref<'success' | 'error' | null>(null)

onMounted(() => { loadReviews() })

async function loadReviews() {
  try {
    const { data } = await reviewAPI.getReviews(props.poiId)
    items.value = data.data.items
    total.value = data.data.total
    avgRating.value = data.data.avg_rating
  } catch { /* ignore */ }
}

async function submitReview() {
  if (!content.value.trim() || submitting.value) return
  submitting.value = true
  submitMsg.value = null
  try {
    await reviewAPI.createReview(props.poiId, content.value.trim(), rating.value || undefined, replyTo.value?.id)
    content.value = ''
    rating.value = 0
    replyTo.value = null
    submitMsg.value = 'success'
    await loadReviews()
    setTimeout(() => { submitMsg.value = null }, 2500)
  } catch (e: any) {
    submitMsg.value = 'error'
    console.error('评价提交失败:', e?.response?.data?.detail || e?.message || '未知错误')
    setTimeout(() => { submitMsg.value = null }, 3500)
  }
  finally { submitting.value = false }
}

function startReply(item: ReviewItem) {
  replyTo.value = { id: item.id, user_name: item.user_name }
}

function cancelReply() { replyTo.value = null }

async function handleLike(item: ReviewItem) {
  try {
    const { data } = await reviewAPI.likeReview(item.id)
    item.likes = data.data.likes
  } catch { /* ignore */ }
}

async function handleDelete(id: string) {
  try {
    await reviewAPI.deleteReview(id)
    await loadReviews()
  } catch { /* ignore */ }
}

function ratingText(r: number) {
  return ['', '很差', '较差', '一般', '推荐', '强烈推荐'][r] || ''
}

function formatTime(iso: string) {
  if (!iso) return ''
  const d = new Date(iso)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return `${d.getMonth() + 1}月${d.getDate()}日`
}
</script>

<style scoped lang="scss">
// ── Color tokens (match parent panel) ──
$bg-warm:     #FAF8F3;
$bg-oat:      #F5F0E8;
$bg-white:    #FFFFFF;
$brand-brown: #A68B7A;
$brand-sage:  #B8C4B8;
$text-primary:   #3D3D3D;
$text-secondary: #6B6B6B;
$text-muted:     #B8B0A8;
$border:       #E8D5D0;
$accent-gold:  #E5A84B;
$star-on:      #F5B948;
$star-off:     #DDD5CB;

.review-section { padding: 4px 0 8px; }

// ════════════════════════════ 评分概览 ════════════════════════════
.review-summary {
  display: flex; align-items: center; gap: 18px;
  padding: 18px 20px; background: linear-gradient(135deg, $bg-oat, #FDF9F4);
  border-radius: 14px; border: 1px solid rgba($brand-brown, 0.12);
  margin-bottom: 22px;
  position: relative; overflow: hidden;

  // 装饰光晕
  &::before {
    content: ''; position: absolute; top: -24px; right: -24px;
    width: 80px; height: 80px; border-radius: 50%;
    background: radial-gradient(circle, rgba($accent-gold, 0.08), transparent 70%);
  }
}
.summary-score-wrap { display: flex; align-items: baseline; line-height: 1; }
.summary-score {
  font-size: 32px; font-weight: 800; color: $accent-gold;
  letter-spacing: -0.5px;
  text-shadow: 0 1px 2px rgba($accent-gold, 0.15);
}
.summary-max { font-size: 15px; font-weight: 500; color: $text-muted; margin-left: 2px; }
.summary-stars { display: flex; gap: 3px; }
.star {
  font-size: 19px; color: $star-off; transition: color 0.2s ease;
  &.filled { color: $star-on; text-shadow: 0 1px 3px rgba($star-on, 0.25); }
}
.summary-count {
  font-size: 13px; color: $text-muted; margin-left: auto;
  white-space: nowrap; font-weight: 500;
}

// ════════════════════════════ 发表评价 ════════════════════════════
.review-composer { margin-bottom: 22px; }
.composer-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px;
}
.composer-label {
  font-size: 14px; font-weight: 650; color: $text-primary;
  letter-spacing: 0.2px;
}
.cancel-reply-btn {
  font-size: 12px; color: $text-muted; background: none; border: none;
  cursor: pointer; padding: 4px 10px; border-radius: 8px;
  transition: all 0.2s;
  &:hover { color: $brand-brown; background: $bg-oat; }
}

// 星级评分选择器
.composer-rating {
  display: flex; align-items: center; gap: 6px;
  margin-bottom: 10px; padding: 8px 12px;
  background: $bg-oat; border-radius: 12px; border: 1px dashed rgba($brand-brown, 0.18);
}
.rating-star {
  font-size: 26px; color: $star-off; background: none; border: none;
  cursor: pointer; padding: 1px 3px; transition: all 0.18s cubic-bezier(.34,1.56,.64,1);
  line-height: 1; position: relative;

  &:hover { color: $accent-gold; transform: scale(1.18); }
  &.on { color: $star-on; text-shadow: 0 2px 4px rgba($star-on, 0.3); }
}
.rating-hint {
  font-size: 13px; font-weight: 600; color: $accent-gold;
  margin-left: 8px; letter-spacing: 0.5px;
  animation: hintIn 0.25s ease-out;
}
@keyframes hintIn { from { opacity: 0; transform: translateX(-6px); } to { opacity: 1; } }

// 输入行
.composer-input-row {
  display: flex; gap: 10px; align-items: flex-end;
}
.composer-textarea {
  flex: 1; padding: 12px 16px;
  background: $bg-white; border: 1.5px solid $border;
  border-radius: 13px; color: $text-primary; font-size: 14px;
  font-family: inherit; outline: none; resize: none;
  min-height: 52px; max-height: 120px; line-height: 1.55;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.02);

  &::placeholder { color: $text-muted; font-style: italic; }
  &:focus {
    border-color: $brand-brown;
    box-shadow: 0 0 0 4px rgba($brand-brown, 0.07), inset 0 1px 3px rgba(0,0,0,0.01);
  }
}

// 提交按钮
.composer-submit {
  width: 46px; height: 46px; flex-shrink: 0;
  border: none; border-radius: 13px;
  background: linear-gradient(145deg, $accent-gold, #D49A35);
  color: #fff; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 3px 14px rgba($accent-gold, 0.32);
  transition: all 0.25s ease;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 22px rgba($accent-gold, 0.42);
    background: linear-gradient(145deg, #EDB65C, $accent-gold);
  }
  &:active:not(:disabled) { transform: translateY(0); }
  &:disabled { opacity: 0.35; cursor: not-allowed; box-shadow: none; }
}
.spinner { width: 20px; height: 20px; animation: spin 0.7s linear infinite; color: #fff; }
@keyframes spin { to { transform: rotate(360deg); } }

// 未登录提示
.review-login-hint {
  text-align: center; padding: 20px 16px; font-size: 14px;
  color: $text-secondary; background: $bg-oat;
  border-radius: 12px; border: 1px dashed rgba($brand-brown, 0.15);

  a { color: $brand-brown; font-weight: 650; text-decoration: none;
    border-bottom: 1.5px solid transparent;
    &:hover { border-bottom-color: $brand-brown; }
  }
}

// ════════════════════════════ 评论列表 ════════════════════════════
.review-list { display: flex; flex-direction: column; gap: 4px; }

.review-card {
  display: flex; gap: 14px;
  padding: 18px 16px;
  border-radius: 14px; border: 1px solid rgba($brand-brown, 0.09);
  background: $bg-white;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba($brand-brown, 0.18);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  }
}
.review-avatar {
  width: 38px; height: 38px; border-radius: 50%;
  background: linear-gradient(145deg, $brand-sage, #9aad96);
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; font-weight: 700; color: #fff;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(184,196,184,0.3);
}
.review-body { flex: 1; min-width: 0; }
.review-top {
  display: flex; align-items: center; gap: 8px;
  flex-wrap: wrap; margin-bottom: 6px;
}
.review-name { font-size: 13.5px; font-weight: 650; color: $text-primary; }
.review-rating { display: flex; gap: 1px; }
.mini-star { font-size: 12px; color: $star-off; &.on { color: $star-on; } }
.review-time {
  font-size: 11.5px; color: $text-muted; margin-left: auto;
  white-space: nowrap;
}
.review-content {
  font-size: 14px; color: $text-secondary; line-height: 1.72;
  margin-bottom: 10px; white-space: pre-wrap; word-break: break-word;
}

// 操作按钮组
.review-actions { display: flex; gap: 4px; padding-top: 8px; border-top: 1px solid rgba($border, 0.5); }
.action-btn {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 12px; color: $text-muted; background: transparent;
  border: none; cursor: pointer; font-family: inherit;
  padding: 4px 10px; border-radius: 8px; transition: all 0.2s;

  svg { width: 14px; height: 14px; opacity: 0.6; }
  &:hover { color: $brand-brown; background: $bg-oat; svg { opacity: 1; } }
  &.danger:hover { color: #E05D54; background: rgba(224,93,84,0.06); }
}

// ════════════════════════════ 回复列表 ════════════════════════════
.replies {
  margin-top: 12px; padding: 12px 14px;
  background: $bg-oat; border-radius: 11px;
  border-left: 3px solid rgba($brand-brown, 0.2);
}
.reply-card {
  display: flex; gap: 10px; padding: 10px 0;
  &:not(:last-child) { border-bottom: 1px solid rgba($border, 0.45); }
}
.reply-avatar {
  width: 28px; height: 28px; border-radius: 50%;
  background: linear-gradient(145deg, #c4bfb7, #a89e94);
  display: flex; align-items: center; justify-content: center;
  font-size: 11.5px; font-weight: 700; color: #fff;
  flex-shrink: 0;
}
.reply-body { flex: 1; min-width: 0; }
.reply-top { display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap; }
.reply-name { font-size: 12px; font-weight: 600; color: $text-primary; }
.reply-to { font-size: 11.5px; color: $brand-brown; font-weight: 500; }
.reply-time { font-size: 11px; color: $text-muted; margin-left: auto; white-space: nowrap; }
.reply-content { font-size: 13px; color: $text-secondary; line-height: 1.6; word-break: break-word; }

// 空状态
.review-empty {
  text-align: center; padding: 30px 16px;
  color: $text-muted; font-size: 14px;
  background: linear-gradient(180deg, transparent, rgba($bg-oat, 0.4));
  border-radius: 12px;
  position: relative;

  &::after {
    content: '✦'; display: block; font-size: 24px; color: rgba($brand-brown, 0.15);
    margin-bottom: 8px;
  }
}

// ════════════════════════════ 提交反馈 Toast ════════════════════════════
.submit-toast {
  display: flex; align-items: center; gap: 8px;
  margin-top: 10px; padding: 10px 16px;
  border-radius: 11px; font-size: 13.5px; font-weight: 600;
  line-height: 1.4; animation: msgIn 0.3s ease-out;

  &--success { background: rgba(76,175,80,0.08); color: #4CAF50; border: 1px solid rgba(76,175,80,0.18); svg { flex-shrink: 0; } }
  &--error   { background: rgba(229,93,84,0.07); color: #D45B52; border: 1px solid rgba(229,93,84,0.16); svg { flex-shrink: 0; } }
}
@keyframes msgIn { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: translateY(0); } }

.msg-fade-enter-active { transition: all 0.28s ease; }
.msg-fade-leave-active { transition: all 0.2s ease; }
.msg-fade-enter-from, .msg-fade-leave-to { opacity: 0; transform: translateY(-6px); }
</style>

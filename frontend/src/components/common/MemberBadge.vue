<template>
  <div class="member-badge">
    <el-popover
      placement="bottom-end"
      :width="320"
      trigger="hover"
      :show-after="200"
      popper-class="member-popover"
    >
      <template #reference>
        <div class="badge-trigger">
          <el-badge :value="badgeText" class="pro-badge" type="warning">
            <el-avatar :size="36" class="user-avatar">
              <el-icon :size="20"><UserFilled /></el-icon>
            </el-avatar>
          </el-badge>
        </div>
      </template>

      <div class="member-popup">
        <div class="popup-header">
          <span class="popup-title">智游 Pro 会员</span>
          <span class="popup-subtitle">解锁全部智能旅行功能</span>
        </div>

        <div class="benefit-list">
          <div v-for="b in benefits" :key="b.label" class="benefit-item">
            <el-icon :size="18" class="benefit-check"><Check /></el-icon>
            <div>
              <div class="benefit-label">{{ b.label }}</div>
              <div class="benefit-desc">{{ b.desc }}</div>
            </div>
          </div>
        </div>

        <div class="compare-table">
          <div class="compare-row compare-header">
            <span>功能</span>
            <span class="free-col">免费版</span>
            <span class="pro-col">Pro</span>
          </div>
          <div v-for="row in compareRows" :key="row.label" class="compare-row">
            <span>{{ row.label }}</span>
            <span class="free-col">{{ row.free }}</span>
            <span class="pro-col">{{ row.pro }}</span>
          </div>
        </div>

        <el-button type="primary" size="large" class="upgrade-btn" @click="$router.push('/user/member')">
          立即开通 Pro
        </el-button>
      </div>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { UserFilled, Check } from '@element-plus/icons-vue'

const badgeText = 'Pro'

const benefits = [
  { label: '无限行程生成', desc: '不限次数使用 AI 规划行程' },
  { label: '动态重规划', desc: '实时应对航班延误、天气变化' },
  { label: '深度定制', desc: '更精准的偏好匹配和个性化推荐' },
]

const compareRows = [
  { label: '行程数量', free: '3个', pro: '无限' },
  { label: '动态调整', free: '不支持', pro: '支持' },
  { label: '优先预订', free: '不支持', pro: '支持' },
  { label: '专属客服', free: '不支持', pro: '7×24' },
]
</script>

<style scoped lang="scss">
.member-badge {
  display: inline-flex;
  align-items: center;
}

.badge-trigger {
  cursor: pointer;
}

.user-avatar {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #0f172a;
}

:deep(.pro-badge .el-badge__content) {
  font-size: 10px; height: 18px; line-height: 18px;
  padding: 0 5px; font-weight: 600;
  background: #f59e0b; color: #0f172a;
}
</style>

<style lang="scss">
.member-popover {
  padding: 0 !important;
  border-radius: var(--radius-lg) !important;
  overflow: hidden;
}

.member-popup {
  padding: var(--space-lg);
}

.popup-header {
  text-align: center;
  margin-bottom: var(--space-lg);
}

.popup-title {
  display: block;
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-text-primary);
}

.popup-subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.benefit-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
}

.benefit-item {
  display: flex;
  gap: var(--space-sm);
  align-items: flex-start;

  .benefit-check {
    color: var(--color-success);
    margin-top: 2px;
  }
}

.benefit-label {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
}

.benefit-desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.compare-table {
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-bottom: var(--space-lg);
}

.compare-row {
  display: grid;
  grid-template-columns: 1fr 60px 60px;
  padding: 8px 12px;
  font-size: var(--font-size-xs);

  &:not(:last-child) {
    border-bottom: 1px solid var(--color-border-light);
  }
}

.compare-header {
  background: var(--color-bg);
  font-weight: 600;
  color: var(--color-text-primary);
}

.free-col {
  text-align: center;
  color: var(--color-text-muted);
}

.pro-col {
  text-align: center;
  color: var(--color-primary);
  font-weight: 600;
}

.upgrade-btn {
  width: 100%;
  border-radius: var(--radius-md);
  font-weight: 600;
}
</style>

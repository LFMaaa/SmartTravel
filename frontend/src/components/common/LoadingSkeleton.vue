<template>
  <div class="loading-skeleton" :class="[type]">
    <!-- 卡片骨架屏 -->
    <template v-if="type === 'card'">
      <div v-for="i in count" :key="i" class="skeleton-card shimmer-bg">
        <div class="card-image shimmer-bg" />
        <div class="card-content">
          <div class="card-title shimmer-bg" />
          <div class="card-desc shimmer-bg" />
          <div class="card-desc short shimmer-bg" />
          <div class="card-footer">
            <div class="card-tag shimmer-bg" />
            <div class="card-tag shimmer-bg" />
          </div>
        </div>
      </div>
    </template>

    <!-- 列表骨架屏 -->
    <template v-else-if="type === 'list'">
      <div v-for="i in count" :key="i" class="skeleton-list-item shimmer-bg">
        <div class="list-avatar shimmer-bg" />
        <div class="list-content">
          <div class="list-title shimmer-bg" />
          <div class="list-desc shimmer-bg" />
        </div>
      </div>
    </template>

    <!-- 行程骨架屏 -->
    <template v-else-if="type === 'itinerary'">
      <div v-for="i in count" :key="i" class="skeleton-itinerary">
        <div class="day-header shimmer-bg" />
        <div class="activity-list">
          <div v-for="j in 3" :key="j" class="activity-item shimmer-bg">
            <div class="activity-icon shimmer-bg" />
            <div class="activity-content">
              <div class="activity-title shimmer-bg" />
              <div class="activity-desc shimmer-bg" />
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- 默认网格骨架屏 -->
    <template v-else>
      <div v-for="i in count" :key="i" class="skeleton-card shimmer-bg" />
    </template>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  type?: 'card' | 'list' | 'itinerary' | 'default'
  count?: number
}>(), {
  type: 'default',
  count: 3,
})
</script>

<style scoped lang="scss">
.loading-skeleton {
  display: grid;
  gap: var(--space-lg);
  padding: var(--space-lg);

  &.card {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }

  &.list {
    grid-template-columns: 1fr;
    gap: var(--space-md);
  }

  &.itinerary {
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  }

  &.default {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

// 卡片骨架屏
.skeleton-card {
  height: 280px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);

  .card-image {
    height: 160px;
  }

  .card-content {
    padding: var(--space-md);
  }

  .card-title {
    height: 20px;
    width: 60%;
    border-radius: var(--radius-sm);
    margin-bottom: var(--space-sm);
  }

  .card-desc {
    height: 14px;
    width: 100%;
    border-radius: var(--radius-sm);
    margin-bottom: var(--space-xs);

    &.short {
      width: 80%;
    }
  }

  .card-footer {
    display: flex;
    gap: var(--space-sm);
    margin-top: var(--space-md);
  }

  .card-tag {
    height: 24px;
    width: 60px;
    border-radius: var(--radius-full);
  }
}

// 列表骨架屏
.skeleton-list-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);

  .list-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .list-content {
    flex: 1;
  }

  .list-title {
    height: 18px;
    width: 40%;
    border-radius: var(--radius-sm);
    margin-bottom: var(--space-sm);
  }

  .list-desc {
    height: 14px;
    width: 70%;
    border-radius: var(--radius-sm);
  }
}

// 行程骨架屏
.skeleton-itinerary {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;

  .day-header {
    height: 48px;
    background: var(--color-bg-alt);
  }

  .activity-list {
    padding: var(--space-md);
  }

  .activity-item {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    margin-bottom: var(--space-sm);
    background: var(--color-bg);
    border-radius: var(--radius-md);

    &:last-child {
      margin-bottom: 0;
    }

    .activity-icon {
      width: 40px;
      height: 40px;
      border-radius: var(--radius-md);
      flex-shrink: 0;
    }

    .activity-content {
      flex: 1;
    }

    .activity-title {
      height: 16px;
      width: 50%;
      border-radius: var(--radius-sm);
      margin-bottom: var(--space-xs);
    }

    .activity-desc {
      height: 12px;
      width: 80%;
      border-radius: var(--radius-sm);
    }
  }
}
</style>

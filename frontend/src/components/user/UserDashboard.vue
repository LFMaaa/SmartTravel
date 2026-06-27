<template>
  <div class="user-dashboard">
    <div class="dashboard-greeting">
      <h2>你好，{{ userStore.user?.nickname || '旅行者' }} 👋</h2>
      <p>欢迎回到智游，开启你的下一次旅程</p>
    </div>

    <div class="dashboard-stats">
      <StatsCard
        icon="MapLocation"
        :value="stats.totalTrips"
        suffix="个"
        label="行程总数"
        variant="primary"
        :trend="12"
      />
      <StatsCard
        icon="Money"
        :value="stats.totalSpent"
        suffix="元"
        label="累计消费"
        variant="secondary"
        :trend="8"
      />
      <StatsCard
        icon="Clock"
        :value="stats.upcomingTrips"
        suffix="个"
        label="即将出行"
        variant="accent"
      />
      <StatsCard
        icon="StarFilled"
        :value="stats.savedPOIs"
        suffix="个"
        label="收藏目的地"
        variant="primary"
        :trend="24"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import StatsCard from '@/components/common/StatsCard.vue'

const userStore = useUserStore()

const stats = reactive({
  totalTrips: 12,
  totalSpent: 28500,
  upcomingTrips: 2,
  savedPOIs: 38,
})
</script>

<style scoped lang="scss">
.user-dashboard {
  padding: var(--space-lg) 0;
}

.dashboard-greeting {
  margin-bottom: var(--space-xl);

  h2 {
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: var(--space-xs);
  }

  p {
    font-size: var(--font-size-sm);
    color: #94a3b8;
  }
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: var(--space-lg);
}
</style>

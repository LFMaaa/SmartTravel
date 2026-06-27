import { computed, ref, type Ref } from 'vue'
import type { DayItinerary } from '@/types/itinerary'

export function useBudget(days: Ref<DayItinerary[]>, totalBudget?: Ref<number>) {
  const overBudget = ref(false)
  const overAmount = ref(0)

  const currentTotal = computed(() => {
    if (!days.value) return 0
    let sum = 0
    for (const day of days.value) {
      for (const act of day.activities || []) {
        sum += act.price || 0
      }
      if (day.hotel) sum += day.hotel.price || 0
    }
    return sum
  })

  const avgPerDay = computed(() => {
    const count = days.value?.length || 1
    return Math.round(currentTotal.value / count)
  })

  const categoryBreakdown = computed(() => {
    const groups: Record<string, number> = { hotel: 0, attraction: 0, restaurant: 0, transport: 0 }
    if (!days.value) return groups
    for (const day of days.value) {
      for (const act of day.activities || []) {
        const type = act.type || 'attraction'
        if (groups[type] !== undefined) groups[type] += act.price || 0
      }
      if (day.hotel) groups.hotel += day.hotel.price || 0
    }
    return groups
  })

  function checkBudget() {
    if (totalBudget?.value && currentTotal.value > totalBudget.value) {
      overBudget.value = true
      overAmount.value = currentTotal.value - totalBudget.value
    } else {
      overBudget.value = false
      overAmount.value = 0
    }
  }

  function budgetStatusColor() {
    if (!totalBudget?.value) return 'var(--color-text-primary)'
    const ratio = currentTotal.value / totalBudget.value
    if (ratio > 1) return 'var(--color-danger)'
    if (ratio > 0.8) return 'var(--color-warning)'
    return 'var(--color-success)'
  }

  return {
    currentTotal,
    avgPerDay,
    categoryBreakdown,
    overBudget,
    overAmount,
    checkBudget,
    budgetStatusColor,
  }
}

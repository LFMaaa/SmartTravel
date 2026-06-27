<template>
  <div class="booking-list">
    <h4>预订清单</h4>
    <el-checkbox-group v-model="checkedItems">
      <div v-for="item in items" :key="item.id" class="booking-item">
        <el-checkbox :value="item.id">
          <span class="item-name">{{ item.name }}</span>
          <span class="item-price">¥{{ item.price }}</span>
        </el-checkbox>
      </div>
    </el-checkbox-group>
    <div class="total">
      合计：<span class="total-price">¥{{ totalPrice }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface BookingItem { id: string; name: string; price: number }
const props = defineProps<{ items: BookingItem[] }>()
const checkedItems = ref<string[]>(props.items.map((i) => i.id))

const totalPrice = computed(() =>
  props.items
    .filter((i) => checkedItems.value.includes(i.id))
    .reduce((sum, i) => sum + i.price, 0)
)
</script>

<style scoped>
.booking-list h4 { margin-bottom: 12px; }
.booking-item { margin-bottom: 8px; }
.item-name { margin-left: 8px; }
.item-price { margin-left: 12px; color: #e6a23c; }
.total { margin-top: 12px; font-size: 16px; font-weight: 600; }
.total-price { color: #f56c6c; }
</style>
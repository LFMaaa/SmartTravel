<template>
  <div class="home-view">
    <HeroSection />
    <DestinationGrid />
    <FeatureShowcase />
    <TrustBar />
  </div>
</template>

<script setup lang="ts">
import HeroSection from '@/components/home/HeroSection.vue'
import DestinationGrid from '@/components/home/DestinationGrid.vue'
import FeatureShowcase from '@/components/home/FeatureShowcase.vue'
import TrustBar from '@/components/home/TrustBar.vue'
</script>

<style scoped>
.home-view {
  overflow: hidden;
}
</style>

/**
 * 天气数据 composable
 * 根据目的地城市获取高德天气，按日期返回对应天气预报 + 图标
 */
import { ref, watch } from 'vue'
import { fetchWeatherByCity, type WeatherCast } from '@/api/weather'

/** 天气现象 → 图标类型映射 */
const WEATHER_ICON_MAP: Record<string, string> = {
  '晴': 'sunny',
  '多云': 'cloudy',
  '少云': 'partly-cloudy',
  '阴': 'overcast',
  '阵雨': 'shower',
  '雷阵雨': 'thunder',
  '雷阵雨伴冰雹': 'thunder-hail',
  '雨夹雪': 'sleet',
  '雨雪天气': 'rain-snow',
  '小雨': 'light-rain',
  '中雨': 'moderate-rain',
  '大雨': 'heavy-rain',
  '暴雨': 'storm',
  '大暴雨': 'storm',
  '特大暴雨': 'storm',
  '阵雪': 'light-snow',
  '小雪': 'light-snow',
  '中雪': 'moderate-snow',
  '大雪': 'heavy-snow',
  '暴雪': 'blizzard',
  '雾': 'fog',
  '沙尘暴': 'sand',
  '浮尘': 'dust',
  '扬沙': 'sand',
  '强沙尘暴': 'sand',
  '霾': 'haze',
}

export function useWeather() {
  const loading = ref(false)
  const forecast = ref<WeatherCast[]>([])
  const cityLabel = ref('')

  /** 根据城市名加载3天预报 */
  async function loadWeather(city: string) {
    if (!city || city === cityLabel.value && forecast.value.length > 0) return

    loading.value = true
    try {
      const data = await fetchWeatherByCity(city)
      if (data) {
        forecast.value = data.casts || []
        cityLabel.value = data.city
      }
    } finally {
      loading.value = false
    }
  }

  /** 通过日期获取当天的天气 */
  function getWeatherByDate(date: string | null): WeatherCast | null {
    if (!date || !forecast.value.length) return null
    // 匹配 YYYY-MM-DD 格式
    const d = typeof date === 'string' ? date.slice(0, 10) : ''
    return forecast.value.find(c => c.date === d) || null
  }

  /** 获取天气图标 SVG */
  function getWeatherIcon(weather: WeatherCast | null): string {
    if (!weather) return 'sunny'
    const key = weather.dayweather || ''
    return WEATHER_ICON_MAP[key] || 'sunny'
  }

  /** 获取显示温度（白天温度） */
  function getTempDisplay(weather: WeatherCast | null): string {
    if (!weather) return '--°C'
    return `${weather.daytemp}°C`
  }

  /** 获取天气描述文字 */
  function getWeatherText(weather: WeatherCast | null): string {
    if (!weather) return ''
    return weather.dayweather || ''
  }

  /** 重置 */
  function reset() {
    forecast.value = []
    cityLabel.value = ''
    loading.value = false
  }

  return {
    loading,
    forecast,
    cityLabel,
    loadWeather,
    getWeatherByDate,
    getWeatherIcon,
    getTempDisplay,
    getWeatherText,
    reset,
  }
}

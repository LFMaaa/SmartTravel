/**
 * 高德地图天气 API 服务
 * 文档: https://lbs.amap.com/api/webservice/guide/api/weatherinfo
 */

const AMAP_KEY = '81ab25ac449c92c10c1c0c79a95d41c1'
const BASE_URL = 'https://restapi.amap.com/v3/weather'

export interface WeatherCast {
  date: string
  week: string
  dayweather: string    // 白天天气现象（晴/多云/阴/小雨等）
  nightweather: string   // 夜间天气现象
  daytemp: string        // 白天温度
  nighttemp: string      // 夜间温度
  daywind: string        // 白天风向
  nightwind: string      // 夜间风向
  daypower: string       // 白天风力
  nightpower: string     // 夜间风力
}

export interface WeatherForecast {
  city: string
  adcode: string
  province: string
  reporttime: string
  casts: WeatherCast[]
}

export interface WeatherResponse {
  status: string
  count: string
  info: string
  forecasts?: WeatherForecast[]
}

/** 根据城市名称获取3天天气预报 */
export async function fetchWeatherByCity(city: string): Promise<WeatherForecast | null> {
  if (!city) return null

  try {
    const params = new URLSearchParams({
      key: AMAP_KEY,
      city,
      extensions: 'all', // 获取未来3天预报
      output: 'JSON',
    })

    const res = await fetch(`${BASE_URL}/weatherInfo?${params.toString()}`)
    const data: WeatherResponse = await res.json()

    if (data.status === '1' && data.forecasts?.length > 0) {
      return data.forecasts[0]
    }

    console.warn('[Weather] API返回异常:', data.info)
    return null
  } catch (err) {
    console.error('[Weather] 请求失败:', err)
    return null
  }
}

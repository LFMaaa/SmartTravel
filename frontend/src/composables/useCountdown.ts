import { ref, onUnmounted } from 'vue'

export function useCountdown(seconds: number) {
  const remaining = ref(seconds)
  let timer: ReturnType<typeof setInterval> | null = null

  function start() {
    stop()
    timer = setInterval(() => {
      if (remaining.value <= 0) {
        stop()
      } else {
        remaining.value--
      }
    }, 1000)
  }

  function stop() {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  function reset(s: number) {
    stop()
    remaining.value = s
  }

  onUnmounted(() => stop())

  return { remaining, start, stop, reset }
}
import { ref } from 'vue'
import { useItineraryStore } from '@/stores/itinerary'
import { useUserStore } from '@/stores/user'
import type { ItineraryResponse } from '@/types/itinerary'

export function useItineraryGenerate() {
  const store = useItineraryStore()
  const userStore = useUserStore()
  const thinkingSteps = ref<string[]>([])

  async function generate(query: string, itineraryId?: string): Promise<ItineraryResponse> {
    thinkingSteps.value = []
    const userId = userStore.user?.id || 'anonymous'
    const result = await store.generateItinerary(query, userId, itineraryId)
    return result
  }

  async function generateStream(
    query: string,
    onThinking: (step: string) => void,
    onDone: (result: ItineraryResponse) => void,
  ) {
    const token = localStorage.getItem('access_token')
    const response = await fetch('/api/v1/itinerary/generate/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ query }),
    })

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()
    if (!reader) return

    let buffer = ''
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            if (data.type === 'thinking') {
              thinkingSteps.value.push(data.content)
              onThinking(data.content)
            } else if (data.type === 'done') {
              onDone(data.data)
            }
          } catch {
            // Skip non-JSON lines
          }
        }
      }
    }
  }

  return { thinkingSteps, generate, generateStream }
}

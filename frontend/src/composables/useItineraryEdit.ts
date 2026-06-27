import { ref } from 'vue'
import type { ActivityItem, DayItinerary } from '@/types/itinerary'

export function useItineraryEdit() {
  const undoStack = ref<DayItinerary[][]>([])
  const redoStack = ref<DayItinerary[][]>([])

  function pushUndo(days: DayItinerary[]) {
    undoStack.value.push(JSON.parse(JSON.stringify(days)))
    redoStack.value = []
  }

  function undo(currentDays: DayItinerary[]): DayItinerary[] | null {
    if (undoStack.value.length === 0) return null
    redoStack.value.push(JSON.parse(JSON.stringify(currentDays)))
    return undoStack.value.pop()!
  }

  function redo(currentDays: DayItinerary[]): DayItinerary[] | null {
    if (redoStack.value.length === 0) return null
    undoStack.value.push(JSON.parse(JSON.stringify(currentDays)))
    return redoStack.value.pop()!
  }

  function moveActivity(
    days: DayItinerary[],
    fromDayIndex: number,
    fromActivityIndex: number,
    toDayIndex: number,
    toActivityIndex: number,
  ): DayItinerary[] {
    const newDays = JSON.parse(JSON.stringify(days)) as DayItinerary[]
    const activity = newDays[fromDayIndex].activities.splice(fromActivityIndex, 1)[0]
    newDays[toDayIndex].activities.splice(toActivityIndex, 0, activity)
    return newDays
  }

  function addActivity(days: DayItinerary[], dayIndex: number, activity: ActivityItem): DayItinerary[] {
    const newDays = JSON.parse(JSON.stringify(days)) as DayItinerary[]
    newDays[dayIndex].activities.push(activity)
    return newDays
  }

  function removeActivity(days: DayItinerary[], dayIndex: number, activityIndex: number): DayItinerary[] {
    const newDays = JSON.parse(JSON.stringify(days)) as DayItinerary[]
    newDays[dayIndex].activities.splice(activityIndex, 1)
    return newDays
  }

  return { undoStack, redoStack, pushUndo, undo, redo, moveActivity, addActivity, removeActivity }
}
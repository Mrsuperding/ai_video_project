import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { DigitalHuman } from '@/api/types/digital-human'

export const useDigitalHumanStore = defineStore('digitalHuman', () => {
  const items = ref<DigitalHuman[]>([])
  const currentItem = ref<DigitalHuman | null>(null)
  const loading = ref(false)

  const setItems = (list: DigitalHuman[]) => {
    items.value = list
  }

  const setCurrentItem = (item: DigitalHuman) => {
    currentItem.value = item
  }

  const clear = () => {
    items.value = []
    currentItem.value = null
  }

  return {
    items,
    currentItem,
    loading,
    setItems,
    setCurrentItem,
    clear
  }
})
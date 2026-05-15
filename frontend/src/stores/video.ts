import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { VideoProject } from '@/api/types/video'

export const useVideoStore = defineStore('video', () => {
  const projects = ref<VideoProject[]>([])
  const currentProject = ref<VideoProject | null>(null)
  const loading = ref(false)

  const setProjects = (list: VideoProject[]) => {
    projects.value = list
  }

  const setCurrentProject = (project: VideoProject) => {
    currentProject.value = project
  }

  const clear = () => {
    projects.value = []
    currentProject.value = null
  }

  return {
    projects,
    currentProject,
    loading,
    setProjects,
    setCurrentProject,
    clear
  }
})
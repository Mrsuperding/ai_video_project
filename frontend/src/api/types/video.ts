export interface VideoProject {
  id: number
  project_name: string
  script_id: number
  digital_human_id: number
  category?: string
  duration?: number
  status: 'draft' | 'pending' | 'processing' | 'completed' | 'failed'
  output_url?: string
  thumbnail_url?: string
  error_message?: string
  created_at: string
  updated_at: string
}

export interface CreateVideoProjectParams {
  project_name: string
  script_id: number
  digital_human_id: number
  category?: string
}

export interface UpdateVideoProjectParams {
  project_name?: string
  script_id?: number
  digital_human_id?: number
}
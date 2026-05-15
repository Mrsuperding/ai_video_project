export interface DigitalHuman {
  id: number
  name: string
  avatar_url?: string
  preview_url?: string
  gender?: string
  age_range?: string
  style?: string[]
  category?: string
  status: 'pending' | 'processing' | 'ready' | 'failed'
  thumbnail_url?: string
  description?: string
  tags?: string[]
  is_public: boolean
  watch_count: number
  use_count: number
  created_at: string
  updated_at: string
}

export interface CreateDigitalHumanParams {
  name: string
  gender?: string
  age_range?: string
  style?: string[]
  category?: string
  description?: string
  source?: 'photo' | 'template'
  photo_url?: string
  template_id?: number
}

export interface UpdateDigitalHumanParams {
  name?: string
  description?: string
  tags?: string[]
  is_public?: boolean
}
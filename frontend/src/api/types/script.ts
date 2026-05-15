export interface ScriptSegment {
  id?: number
  text: string
  duration?: number
  speed?: number
  pause_after?: number
  emotion?: string
}

export interface ScriptContent {
  segments: ScriptSegment[]
}

export interface Script {
  id: number
  title: string
  description?: string
  content: ScriptContent
  word_count?: number
  estimated_duration?: number
  language: string
  voice_id?: number
  category?: string
  tags?: string[]
  status: string
  usage_count: number
  created_at: string
  updated_at: string
}

export interface CreateScriptParams {
  title: string
  description?: string
  content?: ScriptContent
  language?: string
  category?: string
  tags?: string[]
}

export interface UpdateScriptParams {
  title?: string
  description?: string
  content?: ScriptContent
  category?: string
  tags?: string[]
}
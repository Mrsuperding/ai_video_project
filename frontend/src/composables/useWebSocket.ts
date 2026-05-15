import axios from 'axios'
import { ElMessage } from 'element-plus'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/api/v1/ws/stream'

interface WebSocketMessage {
  type: string
  data?: any
}

class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 3000
  private messageHandlers = new Map<string, ((data: any) => void)[]>()

  connect(token: string) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      return
    }

    const url = `${WS_URL}?token=${token}`
    this.ws = new WebSocket(url)

    this.ws.onopen = () => {
      console.log('WebSocket connected')
      this.reconnectAttempts = 0
    }

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data)
        const handlers = this.messageHandlers.get(message.type)
        if (handlers) {
          handlers.forEach(handler => handler(message.data))
        }
      } catch (e) {
        console.error('WebSocket message parse error', e)
      }
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error', error)
    }

    this.ws.onclose = () => {
      console.log('WebSocket closed')
      this.attemptReconnect(token)
    }
  }

  private attemptReconnect(token: string) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`Reconnecting... attempt ${this.reconnectAttempts}`)
      setTimeout(() => this.connect(token), this.reconnectDelay)
    } else {
      ElMessage.error('WebSocket 连接失败，请刷新页面')
    }
  }

  send(message: WebSocketMessage) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    }
  }

  on(type: string, handler: (data: any) => void) {
    const handlers = this.messageHandlers.get(type) || []
    handlers.push(handler)
    this.messageHandlers.set(type, handlers)
  }

  off(type: string, handler: (data: any) => void) {
    const handlers = this.messageHandlers.get(type) || []
    const index = handlers.indexOf(handler)
    if (index > -1) {
      handlers.splice(index, 1)
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.messageHandlers.clear()
  }
}

export default new WebSocketService()
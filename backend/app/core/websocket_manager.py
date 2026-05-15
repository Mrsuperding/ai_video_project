"""
WebSocket 管理器
"""
from typing import Dict, Set, Optional
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime


class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        # user_id -> set of websockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # task_id -> set of user_ids subscribed
        self.task_subscribers: Dict[int, Set[int]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """连接 WebSocket"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        """断开 WebSocket"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, user_id: int, message: dict):
        """发送个人消息"""
        if user_id in self.active_connections:
            dead_connections = set()
            for websocket in self.active_connections[user_id]:
                try:
                    await websocket.send_json(message)
                except Exception:
                    dead_connections.add(websocket)

            # 清理死连接
            for ws in dead_connections:
                self.active_connections[user_id].discard(ws)

    async def broadcast_to_task(self, task_id: str, event_type: str, data: dict):
        """向任务订阅者广播消息"""
        if task_id in self.task_subscribers:
            message = {
                "type": event_type,
                "data": data,
                "timestamp": int(datetime.utcnow().timestamp())
            }
            for user_id in self.task_subscribers[task_id]:
                await self.send_personal_message(user_id, message)

    async def broadcast_to_users(self, user_ids: list, event_type: str, data: dict):
        """向多个用户广播消息"""
        message = {
            "type": event_type,
            "data": data,
            "timestamp": int(datetime.utcnow().timestamp())
        }
        for user_id in user_ids:
            await self.send_personal_message(user_id, message)

    def subscribe_to_task(self, task_id: int, user_id: int):
        """订阅任务更新"""
        if task_id not in self.task_subscribers:
            self.task_subscribers[task_id] = set()
        self.task_subscribers[task_id].add(user_id)

    def unsubscribe_from_task(self, task_id: int, user_id: int):
        """取消订阅任务"""
        if task_id in self.task_subscribers:
            self.task_subscribers[task_id].discard(user_id)
            if not self.task_subscribers[task_id]:
                del self.task_subscribers[task_id]

    async def send_ping(self, websocket: WebSocket):
        """发送心跳"""
        try:
            await websocket.send_json({"type": "pong", "timestamp": int(datetime.utcnow().timestamp())})
        except Exception:
            pass


# 全局连接管理器
manager = ConnectionManager()
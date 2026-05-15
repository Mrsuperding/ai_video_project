"""
WebSocket API
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional

from app.core.websocket_manager import manager
from app.core.security import decode_token

router = APIRouter()


@router.websocket("/stream")
async def websocket_stream(
    websocket: WebSocket,
    token: Optional[str] = Query(None)
):
    """WebSocket 流式连接"""
    if not token:
        await websocket.close(code=4001, reason="Missing token")
        return

    # 验证 token
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=4001, reason="Invalid token")
        return

    user_id = payload.get("user_id")
    if not user_id:
        await websocket.close(code=4001, reason="Invalid token")
        return

    # 建立连接
    await manager.connect(websocket, user_id)

    try:
        while True:
            # 接收消息
            data = await websocket.receive_json()

            if data.get("type") == "ping":
                # 心跳
                await manager.send_ping(websocket)
            elif data.get("type") == "subscribe":
                # 订阅任务更新
                task_id = data.get("task_id")
                if task_id:
                    manager.subscribe_to_task(task_id, user_id)
            elif data.get("type") == "unsubscribe":
                # 取消订阅
                task_id = data.get("task_id")
                if task_id:
                    manager.unsubscribe_from_task(task_id, user_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception:
        manager.disconnect(websocket, user_id)
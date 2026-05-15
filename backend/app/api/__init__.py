"""API package"""

from fastapi import APIRouter
from app.api.v1 import auth, user, wallet, digital_human, voice, script, asset, video, message, statistics, admin, websocket

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(user.router, prefix="/user", tags=["用户"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["钱包"])
api_router.include_router(wallet.router, prefix="/memberships", tags=["会员"])
api_router.include_router(wallet.router, prefix="/coupons", tags=["优惠券"])
api_router.include_router(digital_human.router, prefix="/digital-humans", tags=["数字人"])
api_router.include_router(voice.router, prefix="/voice-clones", tags=["声音克隆"])
api_router.include_router(script.router, prefix="/scripts", tags=["脚本"])
api_router.include_router(script.router, prefix="/script-templates", tags=["脚本模板"])
api_router.include_router(script.router, prefix="/ai-writing", tags=["AI写作"])
api_router.include_router(asset.router, prefix="/user-assets", tags=["用户素材"])
api_router.include_router(asset.router, prefix="/platform-assets", tags=["平台素材"])
api_router.include_router(video.router, prefix="/video-projects", tags=["视频项目"])
api_router.include_router(video.router, prefix="/generation-tasks", tags=["生成任务"])
api_router.include_router(video.router, prefix="/video-outputs", tags=["视频输出"])
api_router.include_router(message.router, prefix="/messages", tags=["消息"])
api_router.include_router(message.router, prefix="/notification-settings", tags=["通知设置"])
api_router.include_router(statistics.router, prefix="/user/statistics", tags=["用户统计"])
api_router.include_router(admin.router, prefix="/admin", tags=["管理后台"])
api_router.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
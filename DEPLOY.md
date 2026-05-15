# AI Video Platform 一键部署脚本

## 环境要求

- Python 3.11+ 或 3.12
- Node.js 18+
- MySQL 5.7+ 或 8.0+
- Redis 6.0+

## 快速部署

### 1. 数据库初始化

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE ai_video_platform DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 导入数据库结构
mysql -u root -p ai_video_platform < database.sql
```

### 2. 后端部署

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量配置
copy .env.example .env
# 编辑 .env 配置数据库和Redis连接信息

# 初始化数据库（可选，如需测试数据）
python init_db.py

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. 前端部署

```bash
cd frontend

# 安装依赖
npm install

# 开发模式运行
npm run dev

# 生产环境构建
npm run build
```

## Docker 部署 (推荐)

### 使用 Docker Compose

```bash
cd backend

# 启动所有服务（MySQL、Redis、后端）
docker-compose up -d
```

### 环境变量配置 (.env)

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/ai_video_platform

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT配置
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# 应用配置
DEBUG=true
APP_NAME=AI Video Platform
APP_VERSION=1.0.0
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

## 服务地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 后端API | http://localhost:8000 | FastAPI 服务 |
| 前端 | http://localhost:3000 | Vue 3 开发服务器 |
| API文档 | http://localhost:8000/api/docs | Swagger 文档 |
| 管理后台 | http://localhost:3000/admin | 管理员界面 |

## 测试账号

| 类型 | 账号 | 密码 |
|------|------|------|
| 管理员 | admin | admin123 |
| 用户 | 13800138001 | test123 |

## 生产环境部署

### 1. 构建前端

```bash
cd frontend
npm run build
# 构建产物在 dist 目录
```

### 2. 使用 Nginx 部署前端

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/ai_video_project/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. 使用 Gunicorn 运行后端

```bash
pip install gunicorn
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

## 常见问题

### 1. 数据库连接失败
- 检查 MySQL 服务是否运行
- 验证用户名密码是否正确
- 确认数据库已创建

### 2. 端口被占用
```bash
# Windows 查看端口占用
netstat -ano | findstr :8000

# 结束进程
taskkill /F /PID <进程ID>
```

### 3. 前端无法访问后端 API
- 检查后端 CORS 配置
- 确认代理设置正确
- 检查防火墙设置
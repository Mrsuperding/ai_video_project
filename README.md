# AI Video Platform 部署说明

## 环境要求

- Python 3.11+
- Node.js 18+
- MySQL 5.7+ 或 8.0+
- Redis 6.0+

## 一键部署（Docker）

```bash
# 1. 启动所有服务
docker-compose -f docker-deploy.yml up -d

# 2. 查看服务状态
docker-compose -f docker-deploy.yml ps

# 3. 查看日志
docker-compose -f docker-deploy.yml logs -f
```

## 手动部署

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

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env
# 编辑 .env 中的数据库和Redis配置

# 初始化数据库表
python init_db.py

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. 前端部署

```bash
cd frontend

# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
```

## 服务地址

| 服务 | 地址 |
|------|------|
| 后端API | http://localhost:8000 |
| 前端 | http://localhost:3000 |
| API文档 | http://localhost:8000/api/docs |
| 管理后台 | http://localhost:3000/admin |

## 测试账号

| 类型 | 账号 | 密码 |
|------|------|------|
| 管理员 | admin | admin123 |
| 用户 | 13800138001 | test123 |

## 生产环境 Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 常见问题

### 数据库连接失败
```bash
# 检查 MySQL 服务
mysql -u root -p -e "SELECT 1"
```

### 端口被占用
```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <进程ID>
```

### 前端无法连接后端
- 检查 CORS 配置
- 确认防火墙设置
- 验证代理配置
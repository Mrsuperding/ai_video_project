# AI 数字人视频定制平台 - 后端 API 设计文档

## 一、API 设计规范

### 1.1 基础规范

| 规范项 | 说明 |
|--------|------|
| 协议 | HTTPS |
| 协议版本 | RESTful API v1 |
| 基础路径 | `/api/v1` |
| 数据格式 | JSON |
| 字符编码 | UTF-8 |
| 时间格式 | ISO 8601: `2024-01-15T10:30:00Z` (UTC) 或 `2024-01-15T18:30:00+08:00` |
| 金额格式 | 字符串: `"299.00"` (保留2位小数) |
| 布尔值 | `true` / `false` |

### 1.2 HTTP 状态码

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 删除成功，无返回内容 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证 / Token 失效 |
| 403 | Forbidden | 已认证但无权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突（如重复创建） |
| 422 | Unprocessable Entity | 业务逻辑错误（如配额不足） |
| 429 | Too Many Requests | 请求频率超限 |
| 500 | Internal Server Error | 服务器内部错误 |
| 503 | Service Unavailable | 服务暂时不可用 |

### 1.3 统一响应格式

#### 成功响应
```json
{
  "code": 0,
  "message": "success",
  "data": {
    // 业务数据
  },
  "request_id": "req_1234567890",
  "timestamp": 1705310600
}
```

#### 错误响应
```json
{
  "code": 40001,
  "message": "参数验证失败: phone格式不正确",
  "errors": {
    "phone": ["手机号格式不正确"]
  },
  "request_id": "req_1234567890",
  "timestamp": 1705310600
}
```

#### 列表响应
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      // 列表项
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 100,
      "total_pages": 5,
      "has_next": true,
      "has_previous": false
    }
  },
  "request_id": "req_1234567890",
  "timestamp": 1705310600
}
```

### 1.4 分页参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | integer | 1 | 页码（从1开始） |
| page_size | integer | 20 | 每页数量（最大100） |
| sort_by | string | created_at | 排序字段 |
| order | string | desc | asc / desc |

### 1.5 错误码定义

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 10001-19999 | 通用错误 |
| 20001-29999 | 用户认证相关 |
| 30001-39999 | 业务逻辑错误 |
| 40001-49999 | 参数验证错误 |
| 50001-59999 | 第三方服务异常 |

---

## 二、认证与授权 API

### 2.1 用户注册/登录

#### 2.1.1 发送短信验证码

```http
POST /api/v1/auth/sms/send
```

**请求参数:**
```json
{
  "phone": "13800138000",
  "code_type": "register",
  "device_id": "device_abc123",
  "ip_address": "1.2.3.4"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "expire_seconds": 300,
    "retry_after": 60
  }
}
```

**code_type 枚举:**
- `register`: 注册
- `login`: 登录
- `reset_password`: 重置密码
- `bind_phone`: 绑定手机
- `unbind_phone`: 解绑手机

---

#### 2.1.2 手机号验证码登录/注册

```http
POST /api/v1/auth/login/sms
```

**请求参数:**
```json
{
  "phone": "13800138000",
  "code": "123456",
  "device_id": "device_abc123",
  "device_type": "web",
  "user_agent": "Mozilla/5.0..."
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "user": {
      "id": 1001,
      "phone": "13800138000",
      "email": null,
      "nickname": "用户1001",
      "avatar_url": "https://cdn.example.com/avatar/default.png",
      "bio": null,
      "membership_type": "free",
      "membership_expire_at": null,
      "quota": {
        "digital_human": 3,
        "video_monthly": 10,
        "video_max_duration": 60,
        "storage_mb": 1024
      },
      "created_at": "2024-01-01T00:00:00Z"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expires_in": 3600,
      "token_type": "Bearer"
    },
    "is_new_user": false
  }
}
```

---

#### 2.1.3 密码登录

```http
POST /api/v1/auth/login/password
```

**请求参数:**
```json
{
  "account": "13800138000",
  "password": "password123",
  "device_id": "device_abc123",
  "device_type": "web",
  "user_agent": "Mozilla/5.0..."
}
```

**响应:** 同登录/注册

---

#### 2.1.4 OAuth 登录

```http
POST /api/v1/auth/login/oauth
```

**请求参数:**
```json
{
  "provider": "wechat",
  "code": "auth_code_from_wechat",
  "state": "random_state_string",
  "device_id": "device_abc123",
  "device_type": "mobile"
}
```

**provider 枚举:** `wechat`, `google`, `apple`

**响应:** 同登录/注册

---

#### 2.1.5 刷新 Token

```http
POST /api/v1/auth/refresh
```

**请求参数:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  }
}
```

---

#### 2.1.6 登出

```http
POST /api/v1/auth/logout
```

**请求头:**
```
Authorization: Bearer <access_token>
```

**响应:**
```json
{
  "code": 0,
  "message": "success"
}
```

---

### 2.2 用户信息管理

#### 2.2.1 获取当前用户信息

```http
GET /api/v1/user/profile
```

**请求头:**
```
Authorization: Bearer <access_token>
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1001,
    "phone": "13800138000",
    "email": "user@example.com",
    "nickname": "张三",
    "avatar_url": "https://cdn.example.com/avatar/1001.png",
    "bio": "AI视频创作者",
    "real_name": null,
    "real_name_verified": false,
    "membership_type": "pro",
    "membership_expire_at": "2024-12-31T23:59:59Z",
    "quota": {
      "digital_human": {
        "total": 100,
        "used": 5,
        "remaining": 95
      },
      "video_monthly": {
        "total": 500,
        "used": 120,
        "remaining": 380
      },
      "video_max_duration": 300,
      "storage_mb": {
        "total": 10240,
        "used": 2048,
        "remaining": 8192
      }
    },
    "wallet": {
      "balance": "99.50",
      "frozen_balance": "0.00"
    },
    "created_at": "2024-01-01T00:00:00Z",
    "last_login_at": "2024-01-15T10:30:00Z"
  }
}
```

---

#### 2.2.2 更新用户信息

```http
PATCH /api/v1/user/profile
```

**请求参数:**
```json
{
  "nickname": "新昵称",
  "avatar_url": "https://cdn.example.com/avatar/new.png",
  "bio": "新个人简介"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1001,
    "nickname": "新昵称",
    "avatar_url": "https://cdn.example.com/avatar/new.png",
    "bio": "新个人简介"
  }
}
```

---

#### 2.2.3 修改密码

```http
POST /api/v1/user/password/change
```

**请求参数:**
```json
{
  "old_password": "old_password123",
  "new_password": "new_password456"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "密码修改成功"
}
```

---

#### 2.2.4 重置密码

```http
POST /api/v1/user/password/reset
```

**请求参数:**
```json
{
  "phone": "13800138000",
  "code": "123456",
  "new_password": "new_password123"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "密码重置成功"
}
```

---

#### 2.2.5 绑定/解绑手机号

```http
POST /api/v1/user/phone/bind
```

**请求参数:**
```json
{
  "phone": "13800138001",
  "code": "123456"
}
```

**解绑:**
```http
POST /api/v1/user/phone/unbind
```

**请求参数:**
```json
{
  "phone": "13800138000",
  "password": "password123"
}
```

---

#### 2.2.6 绑定/解绑邮箱

```http
POST /api/v1/user/email/bind
```

**请求参数:**
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

---

#### 2.2.7 实名认证

```http
POST /api/v1/user/real-name/verify
```

**请求参数:**
```json
{
  "real_name": "张三",
  "id_card_number": "110101199001011234",
  "id_card_front_url": "https://cdn.example.com/idcard/1001_front.jpg",
  "id_card_back_url": "https://cdn.example.com/idcard/1001_back.jpg"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "提交成功，请等待审核",
  "data": {
    "status": "pending",
    "message": "实名认证信息已提交，预计1-3个工作日完成审核"
  }
}
```

---

### 2.3 用户设备管理

#### 2.3.1 获取登录设备列表

```http
GET /api/v1/user/devices
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| status | string | `active`/`inactive` |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "device_name": "MacBook Pro Chrome",
        "device_type": "web",
        "os_version": "macOS 14.0",
        "last_active_at": "2024-01-15T10:30:00Z",
        "is_current": true
      },
      {
        "id": 2,
        "device_name": "iPhone 15 Pro",
        "device_type": "ios",
        "os_version": "iOS 17.0",
        "last_active_at": "2024-01-14T18:20:00Z",
        "is_current": false
      }
    ]
  }
}
```

---

#### 2.3.2 退出登录设备

```http
DELETE /api/v1/user/devices/{device_id}
```

**响应:**
```json
{
  "code": 0,
  "message": "设备已退出登录"
}
```

---

### 2.4 OAuth 绑定管理

#### 2.4.1 获取 OAuth 绑定列表

```http
GET /api/v1/user/oauth-bindings
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "provider": "wechat",
        "nickname": "张三",
        "avatar_url": "https://wx.qlogo.cn/...",
        "binded_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

---

#### 2.4.2 解绑 OAuth

```http
DELETE /api/v1/user/oauth-bindings/{provider}
```

**响应:**
```json
{
  "code": 0,
  "message": "解绑成功"
}
```

---

## 三、钱包与支付 API

### 3.1 钱包查询

#### 3.1.1 获取钱包信息

```http
GET /api/v1/wallet
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "balance": "99.50",
    "frozen_balance": "0.00",
    "total_recharge": "199.00",
    "total_consume": "99.50"
  }
}
```

---

#### 3.1.2 获取钱包流水

```http
GET /api/v1/wallet/transactions
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| transaction_type | string | 交易类型筛选 |
| start_date | string | 开始日期 `2024-01-01` |
| end_date | string | 结束日期 |
| page | integer | 页码 |
| page_size | integer | 每页数量 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "transaction_no": "TXN20240115001001",
        "transaction_type": "consume",
        "amount": "-0.50",
        "balance_before": "100.00",
        "balance_after": "99.50",
        "related_type": "video_order",
        "related_id": 1001,
        "remark": "视频生成消耗",
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 100,
      "total_pages": 5
    }
  }
}
```

---

### 3.2 充值

#### 3.2.1 创建充值订单

```http
POST /api/v1/wallet/recharge
```

**请求参数:**
```json
{
  "amount": "100.00",
  "payment_method": "alipay"
}
```

**payment_method:** `alipay`, `wechat`, `stripe`

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_no": "REC20240115001001",
    "amount": "100.00",
    "payment_method": "alipay",
    "payment_info": {
      "qr_code": "https://qr.alipay.com/...",
      "expire_time": "2024-01-15T11:30:00Z"
    },
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

#### 3.2.2 查询充值订单状态

```http
GET /api/v1/wallet/recharge/{order_no}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_no": "REC20240115001001",
    "amount": "100.00",
    "status": "paid",
    "paid_at": "2024-01-15T10:35:00Z"
  }
}
```

---

### 3.3 会员订阅

#### 3.3.1 获取会员套餐列表

```http
GET /api/v1/memberships/plans
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "基础版",
        "type": "basic",
        "original_price": "99.00",
        "price": "99.00",
        "duration_months": 1,
        "quota": {
          "digital_human": 10,
          "video_monthly": 50,
          "video_max_duration": 180,
          "storage_mb": 2048
        },
        "features": [
          "1080p高清输出",
          "去水印",
          "优先渲染队列"
        ]
      },
      {
        "id": 2,
        "name": "专业版",
        "type": "pro",
        "original_price": "299.00",
        "price": "199.00",
        "duration_months": 1,
        "quota": {
          "digital_human": 100,
          "video_monthly": 500,
          "video_max_duration": 300,
          "storage_mb": 10240
        },
        "features": [
          "4K超清输出",
          "去水印",
          "优先渲染队列",
          "API调用权限",
          "客户支持"
        ]
      }
    ]
  }
}
```

---

#### 3.3.2 创建会员订单

```http
POST /api/v1/memberships/subscribe
```

**请求参数:**
```json
{
  "plan_id": 2,
  "duration_months": 1,
  "payment_method": "alipay",
  "coupon_code": "SAVE50"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_no": "MBR20240115001001",
    "original_price": "299.00",
    "discount_amount": "100.00",
    "actual_price": "199.00",
    "plan": {
      "id": 2,
      "name": "专业版",
      "type": "pro",
      "duration_months": 1
    },
    "payment_info": {
      "qr_code": "https://qr.alipay.com/...",
      "expire_time": "2024-01-15T11:30:00Z"
    }
  }
}
```

---

#### 3.3.3 查询会员订单状态

```http
GET /api/v1/memberships/orders/{order_no}
```

---

#### 3.3.4 获取我的会员信息

```http
GET /api/v1/memberships/my
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "membership_type": "pro",
    "start_at": "2024-01-01T00:00:00Z",
    "end_at": "2024-12-31T23:59:59Z",
    "days_remaining": 351,
    "auto_renew": true,
    "quota": {
      "digital_human": {
        "total": 100,
        "used": 5,
        "remaining": 95
      },
      "video_monthly": {
        "total": 500,
        "used": 120,
        "remaining": 380
      },
      "video_max_duration": 300,
      "storage_mb": {
        "total": 10240,
        "used": 2048,
        "remaining": 8192
      }
    }
  }
}
```

---

### 3.4 优惠券

#### 3.4.1 获取可用优惠券列表

```http
GET /api/v1/coupons/available
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| product_type | string | `membership`/`video_pack` |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "新用户首单立减",
        "description": "首单减50元",
        "coupon_type": "fixed",
        "value": "50.00",
        "min_amount": "100.00",
        "valid_to": "2024-02-29T23:59:59Z",
        "applicable_products": ["membership"]
      }
    ]
  }
}
```

---

#### 3.4.2 领取优惠券

```http
POST /api/v1/coupons/{coupon_id}/claim
```

**响应:**
```json
{
  "code": 0,
  "message": "领取成功",
  "data": {
    "id": 101,
    "coupon_code": "COUPON2024011501",
    "valid_from": "2024-01-15T00:00:00Z",
    "valid_to": "2024-02-14T23:59:59Z"
  }
}
```

---

#### 3.4.3 获取我的优惠券

```http
GET /api/v1/coupons/my
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| status | string | `unused`/`used`/`expired` |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 101,
        "coupon_code": "COUPON2024011501",
        "name": "新用户首单立减",
        "coupon_type": "fixed",
        "value": "50.00",
        "status": "unused",
        "valid_from": "2024-01-15T00:00:00Z",
        "valid_to": "2024-02-14T23:59:59Z"
      }
    ]
  }
}
```

---

## 四、数字人管理 API

### 4.1 数字人列表

#### 4.1.1 获取数字人列表

```http
GET /api/v1/digital-humans
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| status | string | 状态筛选: `all`/`ready`/`processing`/`failed` |
| page | integer | 页码 |
| page_size | integer | 每页数量 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "我的数字人-职场版",
        "description": "用于商务场景",
        "status": "ready",
        "preview_image_url": "https://cdn.example.com/dh/1_preview.jpg",
        "preview_video_url": "https://cdn.example.com/dh/1_preview.mp4",
        "preview_video_duration": 3.5,
        "usage_count": 25,
        "is_default": true,
        "authorization_type": "self",
        "authorization_status": "approved",
        "created_at": "2024-01-10T00:00:00Z"
      },
      {
        "id": 2,
        "name": "我的数字人-休闲版",
        "description": "用于生活场景",
        "status": "processing",
        "progress": 65,
        "estimated_remaining_seconds": 180,
        "usage_count": 0,
        "is_default": false,
        "authorization_type": "self",
        "created_at": "2024-01-15T09:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 3,
      "total_pages": 1
    }
  }
}
```

---

#### 4.1.2 获取数字人详情

```http
GET /api/v1/digital-humans/{digital_human_id}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 1001,
    "name": "我的数字人-职场版",
    "description": "用于商务场景",
    "source_type": "multi_photos",
    "source_photos": [
      {
        "url": "https://cdn.example.com/dh/1_photo1.jpg",
        "width": 512,
        "height": 512,
        "face_count": 1
      }
    ],
    "photo_count": 5,
    "gender": "male",
    "age_group": "young",
    "clothing_type": "business",
    "background_type": "transparent",
    "status": "ready",
    "preview_image_url": "https://cdn.example.com/dh/1_preview.jpg",
    "preview_video_url": "https://cdn.example.com/dh/1_preview.mp4",
    "usage_count": 25,
    "is_default": true,
    "authorization_type": "self",
    "authorization_status": "approved",
    "version_number": 1,
    "created_at": "2024-01-10T00:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

---

### 4.2 创建数字人

#### 4.2.1 上传照片

**步骤1: 获取上传凭证**
```http
POST /api/v1/upload/digital-human-photos/token
```

**请求参数:**
```json
{
  "file_count": 5,
  "file_size_mb": 0.5
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "upload_token": "token_abc123",
    "upload_url": "https://upload.example.com/upload",
    "expire_seconds": 3600,
    "file_prefix": "dh_1001_20240115_"
  }
}
```

**步骤2: 上传文件到 OSS** (使用返回的 upload_url)

**步骤3: 创建数字人**
```http
POST /api/v1/digital-humans
```

**请求参数:**
```json
{
  "name": "我的数字人-职场版",
  "description": "用于商务场景",
  "source_type": "multi_photos",
  "source_photos": [
    {
      "url": "https://cdn.example.com/dh_1001_20240115_photo1.jpg",
      "width": 512,
      "height": 512
    }
  ],
  "authorization_type": "self",
  "clothing_type": "business",
  "background_type": "transparent",
  "customize": {
    "hairstyle": "professional",
    "accessories": {
      "glasses": false,
      "earring": false
    }
  }
}
```

**响应:**
```json
{
  "code": 0,
  "message": "数字人创建成功，正在生成中",
  "data": {
    "id": 1,
    "name": "我的数字人-职场版",
    "status": "pending",
    "task_id": 1001,
    "estimated_seconds": 600
  }
}
```

---

#### 4.2.2 使用他人照片创建

```http
POST /api/v1/digital-humans
```

**请求参数:**
```json
{
  "name": "demo数字人",
  "source_photos": [...],
  "authorization_type": "others",
  "authorization_proof_url": "https://cdn.example.com/proof/authorization.pdf",
  "authorization_expire_at": "2024-12-31T23:59:59Z"
}
```

---

### 4.3 编辑数字人

#### 4.3.1 更新数字人信息

```http
PATCH /api/v1/digital-humans/{digital_human_id}
```

**请求参数:**
```json
{
  "name": "新名称",
  "description": "新描述"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "更新成功",
  "data": {
    "id": 1,
    "name": "新名称",
    "description": "新描述"
  }
}
```

---

#### 4.3.2 重新生成数字人

```http
POST /api/v1/digital-humans/{digital_human_id}/regenerate
```

**请求参数:**
```json
{
  "new_photos": [
    {
      "url": "https://cdn.example.com/dh_1001_new_photo1.jpg"
    }
  ]
}
```

**响应:**
```json
{
  "code": 0,
  "message": "任务已创建",
  "data": {
    "task_id": 1002,
    "estimated_seconds": 600
  }
}
```

---

### 4.4 数字人操作

#### 4.4.1 设置默认数字人

```http
POST /api/v1/digital-humans/{digital_human_id}/set-default
```

---

#### 4.4.2 删除数字人

```http
DELETE /api/v1/digital-humans/{digital_human_id}
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| delete_related_videos | boolean | 是否同时删除关联视频 |

**响应:**
```json
{
  "code": 0,
  "message": "删除成功",
  "data": {
    "retention_days": 30,
    "can_restore": true
  }
}
```

---

### 4.5 数字人生成任务

#### 4.5.1 获取任务状态

```http
GET /api/v1/digital-humans/tasks/{task_id}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1001,
    "task_type": "create",
    "status": "processing",
    "progress": 65,
    "current_step": "模型训练中",
    "estimated_seconds": 180,
    "started_at": "2024-01-15T09:00:00Z",
    "created_at": "2024-01-15T09:00:00Z"
  }
}
```

---

## 五、声音克隆 API

### 5.1 声音克隆列表

```http
GET /api/v1/voice-clones
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "我的声音",
        "gender": "male",
        "age_group": "young",
        "status": "ready",
        "sample_audio_url": "https://cdn.example.com/voice/1_sample.mp3",
        "duration": 60.5,
        "usage_count": 15,
        "is_default": true,
        "created_at": "2024-01-10T00:00:00Z"
      }
    ]
  }
}
```

---

### 5.2 创建声音克隆

#### 5.2.1 上传音频样本

**步骤1: 获取上传凭证**
```http
POST /api/v1/upload/voice-sample/token
```

**步骤2: 上传文件**

**步骤3: 创建克隆**
```http
POST /api/v1/voice-clones
```

**请求参数:**
```json
{
  "name": "我的声音",
  "source_audio_url": "https://cdn.example.com/audio/sample_30s.mp3",
  "language": "zh",
  "emotion": "neutral"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "声音克隆任务已创建",
  "data": {
    "id": 1,
    "status": "pending",
    "task_id": 2001,
    "estimated_seconds": 300
  }
}
```

---

### 5.3 声音克隆操作

#### 5.3.1 设置默认音色

```http
POST /api/v1/voice-clones/{voice_id}/set-default
```

---

#### 5.3.2 删除声音克隆

```http
DELETE /api/v1/voice-clones/{voice_id}
```

---

## 六、文案脚本 API

### 6.1 脚本列表与详情

#### 6.1.1 获取脚本列表

```http
GET /api/v1/scripts
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| status | string | `all`/`draft`/`published`/`archived` |
| category | string | 分类筛选 |
| keyword | string | 关键词搜索 |
| is_template | boolean | 是否为模板 |
| page | integer | 页码 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "title": "商品带货脚本-护肤品",
        "description": "用于护肤品推广",
        "word_count": 156,
        "estimated_duration": 45.5,
        "language": "zh",
        "category": "商品带货",
        "tags": ["护肤", "美容"],
        "status": "published",
        "usage_count": 8,
        "created_at": "2024-01-10T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 15,
      "total_pages": 1
    }
  }
}
```

---

#### 6.1.2 获取脚本详情

```http
GET /api/v1/scripts/{script_id}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "title": "商品带货脚本-护肤品",
    "description": "用于护肤品推广",
    "content": {
      "segments": [
        {
          "id": 1,
          "text": "大家好，今天给大家推荐一款超好用的护肤品",
          "duration": 8.5,
          "speed": 1.0,
          "pause_after": 0.5,
          "emotion": "neutral"
        },
        {
          "id": 2,
          "text": "它能有效保湿，让你肌肤水润饱满",
          "duration": 6.0,
          "speed": 1.0,
          "pause_after": 0.5,
          "emotion": "excited"
        }
      ]
    },
    "word_count": 156,
    "estimated_duration": 45.5,
    "language": "zh",
    "voice_id": 1,
    "base_tts_speed": 1.0,
    "category": "商品带货",
    "tags": ["护肤", "美容"],
    "status": "published",
    "created_at": "2024-01-10T00:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

---

### 6.2 脚本管理

#### 6.2.1 创建脚本

```http
POST /api/v1/scripts
```

**请求参数:**
```json
{
  "title": "新脚本",
  "description": "脚本描述",
  "content": {
    "segments": [
      {
        "text": "第一段文字",
        "speed": 1.0,
        "pause_after": 0.5,
        "emotion": "neutral"
      }
    ]
  },
  "language": "zh",
  "category": "商品带货",
  "tags": ["育儿", "教育"]
}
```

**响应:**
```json
{
  "code": 0,
  "message": "创建成功",
  "data": {
    "id": 2,
    "title": "新脚本",
    "word_count": 10,
    "estimated_duration": 3.0,
    "status": "draft"
  }
}
```

---

#### 6.2.2 更新脚本

```http
PATCH /api/v1/scripts/{script_id}
```

**请求参数:**
```json
{
  "title": "新标题",
  "content": {
    "segments": [...]
  }
}
```

---

#### 6.2.3 删除脚本

```http
DELETE /api/v1/scripts/{script_id}
```

---

#### 6.2.4 保存为模板

```http
POST /api/v1/scripts/{script_id}/save-as-template
```

**请求参数:**
```json
{
  "name": "商品带货模板",
  "description": "通用商品带货脚本模板",
  "category": "商品带货"
}
```

---

### 6.3 AI 辅助写作

#### 6.3.1 AI 生成文案

```http
POST /api/v1/ai-writing/generate
```

**请求参数:**
```json
{
  "input_type": "template",
  "template_id": 1,
  "template_params": {
    "product_name": "某品牌护肤品",
    "product_features": ["保湿", "美白", "抗衰老"],
    "target_audience": "25-35岁女性"
  },
  "style": "professional",
  "emotion": "excited",
  "target_language": "zh",
  "duration_seconds": 60
}
```

**input_type 枚举:**
- `template`: 使用模板
- `prompt`: 自由提示词

**响应:**
```json
{
  "code": 0,
  "message": "生成成功",
  "data": {
    "task_id": 3001,
    "script_id": 3,
    "content": {
      "plain_text": "大家好，今天给大家推荐一款......",
      "segments": [...]
    },
    "word_count": 180,
    "estimated_duration": 52.5
  }
}
```

---

#### 6.3.2 AI 改写/润色

```http
POST /api/v1/ai-writing/rewrite
```

**请求参数:**
```json
{
  "text": "原文本内容",
  "task_type": "polish",
  "style": "professional",
  "target_language": "zh"
}
```

**task_type 枚举:**
- `rewrite`: 改写
- `polish`: 润色
- `expand`: 扩写
- `shrink`: 缩写
- `translate`: 翻译

---

#### 6.3.3 获取 AI 任务状态

```http
GET /api/v1/ai-writing/tasks/{task_id}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 3001,
    "task_type": "generate",
    "status": "completed",
    "progress": 100,
    "result": {
      "text": "生成的完整文案",
      "segments": [...]
    },
    "input_tokens": 65,
    "output_tokens": 280,
    "cost_cents": 1
  }
}
```

---

### 6.4 脚本模板

#### 6.4.1 获取模板列表

```http
GET /api/v1/script-templates
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| category | string | 分类筛选 |
| source | string | `platform`/`user`/`market` |
| page | integer | 页码 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "商品带货模板",
        "description": "通用的商品推广脚本模板",
        "cover_image_url": "https://cdn.example.com/template/1_cover.jpg",
        "category": "商品带货",
        "tags": ["带货", "营销"],
        "input_fields": [
          {
            "name": "product_name",
            "label": "商品名称",
            "type": "text",
            "required": true,
            "placeholder": "请输入商品名称"
          }
        ],
        "usage_count": 1250,
        "rating": 4.8,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

---

#### 6.4.2 获取模板详情

```http
GET /api/v1/script-templates/{template_id}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "name": "商品带货模板",
    "description": "通用的商品推广脚本模板",
    "prompt_template": "请为{product_name}写一段推广文案，重点突出{product_features}，语气要{emotion}，时长约{duration_seconds}秒",
    "example_text": "大家好，今天给大家推荐一款超好用的...",
    "category": "商品带货",
    "input_fields": [...],
    "usage_count": 1250,
    "rating": 4.8,
    "rating_count": 85
  }
}
```

---

## 七、素材库 API

### 7.1 用户素材

#### 7.1.1 获取用户素材列表

```http
GET /api/v1/user-assets
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| asset_type | string | `Image`/`video`/`audio`/`font` |
| category | string | 分类筛选 |
| tag | string | 标签筛选 |
| keyword | string | 关键词搜索 |
| page | integer | 页码 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "背景图-办公室",
        "asset_type": "image",
        "file_url": "https://cdn.example.com/assets/1.jpg",
        "thumbnail_url": "https://cdn.example.com/assets/1_thumb.jpg",
        "width": 1920,
        "height": 1080,
        "file_size": 524288,
        "category": "background",
        "tags": ["办公", "商务"],
        "usage_count": 5,
        "created_at": "2024-01-10T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 45,
      "total_pages": 3
    }
  }
}
```

---

#### 7.1.2 上传素材

**步骤1: 获取上传凭证**
```http
POST /api/v1/upload/assets/token
```

**请求参数:**
```json
{
  "file_name": "background.jpg",
  "file_size": 524288,
  "asset_type": "image"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "upload_url": "https://upload.example.com/upload",
    "upload_token": "token_abc123",
    "asset_id": 101,
    "expire_seconds": 3600
  }
}
```

**步骤2: 上传文件到指定 URL**

**步骤3: 确认上传完成**
```http
POST /api/v1/user-assets/{asset_id}/confirm
```

**请求参数:**
```json
{
  "name": "背景图-办公室",
  "category": "background",
  "tags": ["办公", "商务"]
}
```

---

#### 7.1.3 更新素材信息

```http
PATCH /api/v1/user-assets/{asset_id}
```

**请求参数:**
```json
{
  "name": "新名称",
  "category": "新分类",
  "tags": ["新标签"]
}
```

---

#### 7.1.4 删除素材

```http
DELETE /api/v1/user-assets/{asset_id}
```

---

### 7.2 平台素材库

#### 7.2.1 获取平台素材列表

```http
GET /api/v1/platform-assets
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| asset_type | string | `background`/`bgm`/`transition`/`sticker` |
| category | string | 分类筛选 |
| license_type | string | `free`/`premium` |
| page | integer | 页码 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "asset_type": "background",
        "file_url": "https://cdn.example.com/platform/bg1.jpg",
        "thumbnail_url": "https://cdn.example.com/platform/bg1_thumb.jpg",
        "width": 1920,
        "height": 1080,
        "category": "办公",
        "license_type": "free",
        "membership_required": "free",
        "usage_count": 5200
      }
    ]
  }
}
```

---

#### 7.2.2 获取素材分类

```http
GET /api/v1/platform-assets/categories
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| asset_type | string | 素材类型 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "办公场景",
        "subcategories": [
          {"id": 11, "name": "会议室"},
          {"id": 12, "name": "办公室"}
        ]
      }
    ]
  }
}
```

---

## 八、视频生成 API

### 8.1 视频项目

#### 8.1.1 获取视频项目列表

```http
GET /api/v1/video-projects
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| status | string | `all`/`draft`/`generating`/`completed`/`failed` |
| category | string | 分类筛选 |
| keyword | string | 关键词搜索 |
| page | integer | 页码 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "project_name": "护肤品推广视频",
        "description": "为某品牌护肤品制作的推广视频",
        "status": "completed",
        "resolution": "1080p",
        "aspect_ratio": "16:9",
        "duration": 45.5,
        "thumbnail_url": "https://cdn.example.com/video/1_thumb.jpg",
        "digital_human": {
          "id": 1,
          "name": "我的数字人-职场版",
          "preview_image_url": "https://cdn.example.com/dh/1_preview.jpg"
        },
        "script": {
          "id": 1,
          "title": "商品带货脚本-护肤品"
        },
        "view_count": 8,
        "download_count": 3,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
      },
      {
        "id": 2,
        "project_name": "新产品介绍",
        "status": "generating",
        "progress": 35,
        "estimated_remaining_seconds": 420,
        "created_at": "2024-01-15T11:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 15,
      "total_pages": 1
    }
  }
}
```

---

#### 8.1.2 获取项目详情

```http
GET /api/v1/video-projects/{project_id}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 1001,
    "project_name": "护肤品推广视频",
    "description": "为某品牌护肤品制作的推广视频",
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "fps": 30,
    "max_duration": 60,
    "generation_status": "completed",
    "priority": 5,
    "digital_human_id": 1,
    "digital_human_config": {
      "position": "center",
      "scale": 1.0,
      "mode": "half_body"
    },
    "script_id": 1,
    "script_content": {
      "segments": [...]
    },
    "voice_id": 1,
    "tts_config": {
      "speed": 1.0,
      "pitch": 0,
      "emotion": "neutral"
    },
    "background_asset_id": 101,
    "background_type": "image",
    "background_value": "101",
    "bgm_asset_id": 201,
    "bgm_volume": 0.30,
    "subtitle_config": {
      "enabled": true,
      "style": "style_1",
      "position": "bottom"
    },
    "tags": ["护肤", "美容"],
    "category": "商品带货",
    "view_count": 8,
    "download_count": 3,
    "share_count": 0,
    "cost_cents": 50,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "output": {
      "id": 1,
      "video_url": "https://cdn.example.com/video/1.mp4",
      "thumbnail_url": "https://cdn.example.com/video/1_thumb.jpg",
      "duration": 45.5,
      "file_size": 15728640,
      "resolution": "1080p",
      "review_status": "auto_approved",
      "watermark_embedded": false
    }
  }
}
```

---

### 8.2 创建视频项目

#### 8.2.1 创建草稿项目

```http
POST /api/v1/video-projects
```

**请求参数（简易模式）:**
```json
{
  "project_name": "护肤产品推广视频",
  "description": "为某品牌护肤品制作的推广视频",
  "mode": "simple",
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "digital_human_id": 1,
  "script_id": 1,
  "background_asset_id": 101,
  "bgm_asset_id": 201
}
```

**请求参数（专业模式）:**
```json
{
  "project_name": "护肤产品推广视频",
  "mode": "professional",
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "fps": 30,
  "digital_human_id": 1,
  "digital_human_config": {
    "position": "center",
    "scale": 1.0,
    "mode": "half_body"
  },
  "script_id": 1,
  "voice_id": 1,
  "tts_config": {
    "speed": 1.0,
    "pitch": 0,
    "emotion": "neutral"
  },
  "timeline_config": {
    "tracks": [
      {
        "type": "video",
        "id": "digital_human",
        "items": [
          {
            "digital_human_id": 1,
            "start_time": 0,
            "end_time": 30,
            "position": "center",
            "scale": 1.0
          }
        ]
      }
    ]
  },
  "subtitle_config": {
    "enabled": true,
    "style": "style_1",
    "position": "bottom"
  }
}
```

**响应:**
```json
{
  "code": 0,
  "message": "项目创建成功",
  "data": {
    "id": 1,
    "project_name": "护肤产品推广视频",
    "status": "draft",
    "estimated_cost_cents": 50
  }
}
```

---

### 8.3 提交生成

#### 8.3.1 提交视频生成任务

```http
POST /api/v1/video-projects/{project_id}/generate
```

**请求参数:**
```json
{
  "priority": 5,
  "skip_queue": false
}
```

**响应:**
```json
{
  "code": 0,
  "message": "任务已提交",
  "data": {
    "project_id": 1,
    "task_id": 4001,
    "status": "queued",
    "queue_position": 5,
    "estimated_seconds": 900
  }
}
```

---

#### 8.3.2 取消生成任务

```http
POST /api/v1/video-projects/{project_id}/cancel
```

**响应:**
```json
{
  "code": 0,
  "message": "任务已取消"
}
```

---

### 8.4 生成任务监控

#### 8.4.1 获取任务状态

```http
GET /api/v1/generation-tasks/{task_id}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 4001,
    "project_id": 1,
    "project_name": "护肤产品推广视频",
    "task_type": "full_pipeline",
    "status": "processing",
    "progress": 35,
    "current_step": "generating",
    "model_provider": "seeddance",
    "model_name": "seeddance_v2",
    "started_at": "2024-01-15T11:00:00Z",
    "estimated_remaining_seconds": 420
  }
}
```

---

#### 8.4.2 获取任务列表

```http
GET /api/v1/generation-tasks
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| status | string | `queued`/`processing`/`completed`/`failed` |

---

### 8.5 视频输出

#### 8.5.1 获取视频输出

```http
GET /api/v1/video-outputs/{output_id} OR /api/v1/video-projects/{project_id}/output
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "project_id": 1,
    "video_url": "https://cdn.example.com/video/1.mp4",
    "thumbnail_url": "https://cdn.example.com/video/1_thumb.jpg",
    "video_file_size": 15728640,
    "resolution": "1080p",
    "duration": 45.5,
    "fps": 30,
    "codec": "H.264",
    "bitrate": 2800,
    "has_audio": true,
    "quality_score": 92,
    "review_status": "auto_approved",
    "watermark_embedded": false,
    "view_count": 8,
    "download_count": 3,
    "share_count": 0,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

#### 8.5.2 下载视频

```http
GET /api/v1/video-outputs/{output_id}/download
```

**响应:** 重定向到视频文件或返回下载链接

---

#### 8.5.3 视频分享

**创建分享链接:**
```http
POST /api/v1/video-outputs/{output_id}/share
```

**请求参数:**
```json
{
  "expire_hours": 24,
  "enable_password": true,
  "password": "123456"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "share_url": "https://platform.example.com/share/v/abc123",
    "share_token": "abc123",
    "expire_at": "2024-01-16T10:30:00Z",
    "has_password": true
  }
}
```

**获取分享视频:**
```http
GET /api/v1/share/{share_token}
```

---

### 8.6 视频管理

#### 8.6.1 更新项目信息

```http
PATCH /api/v1/video-projects/{project_id}
```

**请求参数:**
```json
{
  "project_name": "新项目名称",
  "description": "新描述",
  "tags": ["新标签"]
}
```

---

#### 8.6.2 基于项目重新生成

```http
POST /api/v1/video-projects/{project_id}/regenerate
```

**请求参数:**
```json
{
  "keep_output": false,
  "config_changes": {
    "digital_human_id": 2,
    "script_id": 2
  }
}
```

---

#### 8.6.3 删除项目

```http
DELETE /api/v1/video-projects/{project_id}
```

---

#### 8.6.4 批量操作

```http
POST /api/v1/video-projects/batch
```

**请求参数:**
```json
{
  "action": "delete",
  "project_ids": [1, 2, 3]
}
```

**action 枚举:** `delete`, `archive`, `restore`

---

## 九、通知与消息 API

### 9.1 消息列表

#### 9.1.1 获取消息列表

```http
GET /api/v1/messages
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| is_read | boolean | 是否已读 |
| message_type | string | 消息类型筛选 |
| page | integer | 页码 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "message_type": "task_complete",
        "title": "视频生成完成",
        "content": "您的视频「护肤产品推广」已生成完成",
        "action_url": "https://platform.example.com/projects/1",
        "action_text": "查看视频",
        "related_type": "video_project",
        "related_id": 1,
        "is_read": false,
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "unread_count": 3,
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 15
    }
  }
}
```

---

#### 9.1.2 获取未读消息数

```http
GET /api/v1/messages/unread-count
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "unread_count": 3
  }
}
```

---

### 9.2 消息操作

#### 9.2.1 标记已读

```http
POST /api/v1/messages/{message_id}/read
```

**批量标记已读:**
```http
POST /api/v1/messages/read-all
```

---

#### 9.2.2 删除消息

```http
DELETE /api/v1/messages/{message_id}
```

---

### 9.3 通知设置

#### 9.3.1 获取通知设置

```http
GET /api/v1/notification-settings
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "notify_task_complete": true,
    "notify_task_failed": true,
    "notify_review_result": true,
    "notify_system": true,
    "email_enabled": true,
    "email_task_complete": false,
    "email_task_failed": true,
    "email_payment": true,
    "email_security": true,
    "sms_enabled": false,
    "sms_payment": false,
    "sms_security": true
  }
}
```

---

#### 9.3.2 更新通知设置

```http
PATCH /api/v1/notification-settings
```

**请求参数:**
```json
{
  "notify_task_complete": false,
  "email_task_complete": true,
  "sms_enabled": true
}
```

---

## 十、用户统计 API

### 10.1 用户统计

#### 10.1.1 获取用户使用统计

```http
GET /api/v1/user/statistics
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| period | string | `daily`/`weekly`/`monthly`/`total` |
| start_date | string | 开始日期 |
| end_date | string | 结束日期 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "period": "monthly",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "video_projects": {
      "created": 15,
      "completed": 12,
      "failed": 1,
      "total_duration": 540,
      "avg_duration": 45.0
    },
    "digital_humans": {
      "created": 2,
      "used": 18
    },
    "cost": {
      "total_cents": 650,
      "avg_per_video_cents": 54.17
    },
    "storage": {
      "used_mb": 2048,
      "quota_mb": 10240,
      "usage_percent": 20.0
    },
    "quota": {
      "digital_human": {
        "total": 100,
        "used": 2,
        "remaining": 98
      },
      "video_monthly": {
        "total": 500,
        "used": 15,
        "remaining": 485
      }
    }
  }
}
```

---

#### 10.1.2 获取配额使用情况

```http
GET /api/v1/user/quota
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "digital_human": {
      "total": 100,
      "used": 2,
      "remaining": 98,
      "reset_at": null
    },
    "video_monthly": {
      "total": 500,
      "used": 15,
      "remaining": 485,
      "reset_at": "2024-02-01T00:00:00Z"
    },
    "video_max_duration": 300,
    "storage_mb": {
      "total": 10240,
      "used": 2048,
      "remaining": 8192
    }
  }
}
```

---

## 十一、WebSocket 实时推送 API

### 11.1 连接

```
wss://api.example.com/ws/v1/stream?token=<access_token>
```

**心跳:**
```json
{
  "type": "ping"
}
```

**响应:**
```json
{
  "type": "pong",
  "timestamp": 1705310600
}
```

---

### 11.2 事件类型

#### 11.2.1 任务进度更新

```json
{
  "type": "task_progress",
  "data": {
    "task_id": 4001,
    "task_type": "full_pipeline",
    "project_id": 1,
    "progress": 35,
    "current_step": "generating",
    "estimated_seconds": 420
  }
}
```

---

#### 11.2.2 任务完成

```json
{
  "type": "task_completed",
  "data": {
    "task_id": 4001,
    "project_id": 1,
    "task_type": "full_pipeline",
    "output_id": 1,
    "duration_seconds": 900
  }
}
```

---

#### 11.2.3 任务失败

```json
{
  "type": "task_failed",
  "data": {
    "task_id": 4001,
    "project_id": 1,
    "error_code": "MODEL_TIMEOUT",
    "error_message": "模型调用超时，已自动重试"
  }
}
```

---

#### 11.2.4 消息通知

```json
{
  "type": "notification",
  "data": {
    "message_id": 1,
    "message_type": "task_complete",
    "title": "视频生成完成",
    "content": "您的视频「护肤产品推广」已生成完成"
  }
}
```

---

## 十二、管理后台 API

### 12.1 管理员认证

#### 12.1.1 管理员登录

```http
POST /api/v1/admin/login
```

**请求参数:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "admin": {
      "id": 1,
      "username": "admin",
      "real_name": "管理员",
      "role": "admin"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expires_in": 3600
    }
  }
}
```

---

### 12.2 用户管理

#### 12.2.1 获取用户列表

```http
GET /api/v1/admin/users
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| keyword | string | 关键词(手机号/邮箱/昵称) |
| membership_type | string | 会员类型 |
| status | string | `active`/`suspended` |
| page | integer | 页码 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1001,
        "phone": "13800138000",
        "email": "user@example.com",
        "nickname": "张三",
        "avatar_url": "https://cdn.example.com/avatar/1001.png",
        "membership_type": "pro",
        "status": "active",
        "balance": "99.50",
        "created_at": "2024-01-01T00:00:00Z",
        "last_login_at": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 100
    }
  }
}
```

---

#### 12.2.2 获取用户详情

```http
GET /api/v1/admin/users/{user_id}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1001,
    "phone": "13800138000",
    "email": "user@example.com",
    "nickname": "张三",
    "avatar_url": "https://cdn.example.com/avatar/1001.png",
    "real_name": "张三",
    "id_card_number": "110***********1234",
    "real_name_verified": true,
    "membership_type": "pro",
    "membership_expire_at": "2024-12-31T23:59:59Z",
    "status": "active",
    "balance": "99.50",
    "frozen_balance": "0.00",
    "quota": {
      "digital_human": {"total": 100, "used": 2, "remaining": 98},
      "video_monthly": {"total": 500, "used": 15, "remaining": 485},
      "video_max_duration": 300,
      "storage_mb": {"total": 10240, "used": 2048, "remaining": 8192}
    },
    "register_ip": "1.2.3.4",
    "register_source": "web",
    "created_at": "2024-01-01T00:00:00Z",
    "last_login_at": "2024-01-15T10:30:00Z",
    "last_login_ip": "1.2.3.4"
  }
}
```

---

#### 12.2.3 封禁/解封用户

```http
POST /api/v1/admin/users/{user_id}/ban
```

**请求参数:**
```json
{
  "action": "ban",
  "reason": "违规操作"
}
```

**action 枚举:** `ban`, `unban`

---

### 12.3 内容审核

#### 12.3.1 获取待审核列表

```http
GET /api/v1/admin/reviews/pending
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| target_type | string | `digital_human`/`script`/`video_output` |
| page | integer | 页码 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "user_id": 1001,
        "target_type": "digital_human",
        "target_id": 10,
        "review_type": "authorization",
        "risk_score": 75,
        "risk_labels": ["possible_celebrity"],
        "submit_data": {
          "authorization_type": "others",
          "authorization_proof_url": "https://cdn.example.com/proof/10.pdf"
        },
        "created_at": "2024-01-15T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 5
    }
  }
}
```

---

#### 12.3.2 审核通过/驳回

```http
POST /api/v1/admin/reviews/{review_id}/approve
```

**请求参数( approve):**
```json
{
  "note": "审核通过"
}
```

**驳回:**
```http
POST /api/v1/admin/reviews/{review_id}/reject
```

**请求参数:**
```json
{
  "reason": "授权证明不完整",
  "note": "需要重新上传授权证明"
}
```

---

### 12.4 数据统计

#### 12.4.1 平台整体统计

```http
GET /api/v1/admin/statistics/overview
```

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| period | string | `today`/`yesterday`/`last_7_days`/`last_30_days`/`custom` |
| start_date | string | 自定义开始日期 |
| end_date | string | 自定义结束日期 |

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "period": "last_7_days",
    "start_date": "2024-01-08",
    "end_date": "2024-01-14",
    "users": {
      "new": 1250,
      "active": 5800,
      "paid": 320,
      "churned": 45
    },
    "business": {
      "video_projects_created": 850,
      "video_projects_completed": 780,
      "video_projects_failed": 12,
      "video_success_rate": 98.5,
      "digital_humans_created": 180,
      "avg_video_duration": 42.5
    },
    "finance": {
      "total_revenue_cents": 125000,
      "membership_revenue_cents": 85000,
      "single_purchase_revenue_cents": 40000,
      "total_cost_cents": 45000,
      "gross_profit_cents": 80000
    },
    "models": {
      "seeddance": {
        "calls": 680,
        "success": 650,
        "fail": 30,
        "success_rate": 95.6,
        "cost_cents": 28000
      }
    }
  }
}
```

---

#### 12.4.2 模型使用统计

```http
GET /api/v1/admin/statistics/models
```

---

#### 12.4.3 财务统计

```http
GET /api/v1/admin/statistics/finance
```

---

### 12.5 系统配置

#### 12.5.1 获取系统配置

```http
GET /api/v1/admin/configs
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "key": "membership_pro_quota_digital_human",
        "value": "100",
        "type": "number",
        "description": "专业版用户数字人配额",
        "category": "membership",
        "is_editable": true
      }
    ]
  }
}
```

---

#### 12.5.2 更新系统配置

```http
PATCH /api/v1/admin/configs
```

**请求参数:**
```json
{
  "configs": [
    {
      "key": "membership_pro_quota_digital_human",
      "value": "150"
    }
  ]
}
```

---

## 十三、错误码详细说明

| 错误码 | 错误信息 | 说明 |
|--------|----------|------|
| 0 | success | 成功 |
| 10001 | Unknown error | 未知错误 |
| 10002 | Invalid request | 无效请求 |
| 10003 | Service unavailable | 服务暂时不可用 |
| 20001 | Unauthorized | 未认证 |
| 20002 | Token expired | Token 已过期 |
| 20003 | Invalid token | 无效 Token |
| 20004 | Permission denied | 权限不足 |
| 20005 | Account suspended | 账号已封禁 |
| 20006 | Account deleted | 账号已删除 |
| 30001 | Quota exceeded | 配额不足 |
| 30002 | Insufficient balance | 余额不足 |
| 30003 | Digital human not ready | 数字人未就绪 |
| 30004 | Script too long | 脚本过长 |
| 30005 | Content rejected | 内容被拒绝 |
| 30006 | Model unavailable | 模型不可用 |
| 40001 | Invalid parameter | 参数错误 |
| 40002 | Missing required parameter | 缺少必填参数 |
| 40003 | Invalid phone format | 手机号格式错误 |
| 40004 | Invalid email format | 邮箱格式错误 |
| 40005 | Invalid password format | 密码格式错误 |
| 40006 | File upload failed | 文件上传失败 |
| 40007 | File size too large | 文件过大 |
| 40008 | File type not allowed | 文件类型不允许 |
| 40401 | User not found | 用户不存在 |
| 40402 | Digital human not found | 数字人不存在 |
| 40403 | Script not found | 脚本不存在 |
| 40404 | Asset not found | 素材不存在 |
| 40405 | Project not found | 项目不存在 |
| 50001 | Third-party service error | 第三方服务错误 |
| 50002 | Model API error | 模型 API 错误 |
| 50003 | Payment service error | 支付服务错误 |
| 50004 | SMS service error | 短信服务错误 |
| 50005 | Storage service error | 存储服务错误 |

---

## 十四、限流规则

| 接口类型 | 限制 |
|----------|------|
| 登录/注册 | 每IP每分钟 3 次 |
| 发送验证码 | 每手机号每 5 分钟 1 次 |
| 文件上传 | 每用户每分钟 10 次 |
| 视频生成 | 每用户同时最多 2 个排队任务 |
| API 调用 | 每用户每分钟 100 次 |
| 查询接口 | 每用户每秒 5 次 |

---

## 十五、Webhook 配置

### 15.1 配置 Webhook

```http
POST /api/v1/webhooks
```

**请求参数:**
```json
{
  "url": "https://your-server.com/webhook",
  "events": ["task_completed", "task_failed"],
  "secret": "your_secret_key"
}
```

**响应:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "url": "https://your-server.com/webhook",
    "events": ["task_completed", "task_failed"],
    "secret": "your_secret_key",
    "status": "active"
  }
}
```

---

### 15.2 Webhook 事件

#### Task Completed
```json
{
  "event": "task_completed",
  "timestamp": 1705310600,
  "data": {
    "task_id": 4001,
    "project_id": 1,
    "task_type": "full_pipeline",
    "output_id": 1,
    "video_url": "https://cdn.example.com/video/1.mp4",
    "duration_seconds": 45.5
  }
}
```

#### Task Failed
```json
{
  "event": "task_failed",
  "timestamp": 1705310600,
  "data": {
    "task_id": 4001,
    "project_id": 1,
    "error_code": "MODEL_TIMEOUT",
    "error_message": "模型调用超时"
  }
}
```

### 15.3 验证签名

Webhook 请求头包含:
- `X-Webhook-Signature`: HMAC-SHA256 签名
- `X-Webhook-Timestamp`: 时间戳

验证方式:
```
signature = HMAC-SHA256(secret, timestamp + request_body)
```

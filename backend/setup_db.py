"""Setup database tables"""
import os
import sqlite3

# Remove existing db
for f in ['ai_video.db', 'test.db', 'app.db', 'fresh.db']:
    if os.path.exists(f):
        os.remove(f)

# Create new database directly with SQLite
conn = sqlite3.connect('api_test.db')
cursor = conn.cursor()

# Create all tables
cursor.executescript("""
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    avatar_url VARCHAR(500),
    bio TEXT,
    real_name VARCHAR(50),
    id_card_number VARCHAR(18),
    real_name_verified VARCHAR(1) DEFAULT '0',
    membership_type VARCHAR(10) DEFAULT 'free',
    membership_expire_at DATETIME,
    quota_digital_human INTEGER DEFAULT 3,
    quota_video_monthly INTEGER DEFAULT 10,
    quota_video_max_duration INTEGER DEFAULT 60,
    quota_storage_mb INTEGER DEFAULT 1024,
    status VARCHAR(9) DEFAULT 'active',
    last_login_at DATETIME,
    last_login_ip VARCHAR(45),
    register_ip VARCHAR(45),
    register_source VARCHAR(6) DEFAULT 'web',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
);

-- User wallets
CREATE TABLE IF NOT EXISTS user_wallets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    frozen_balance DECIMAL(10, 2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Scripts table
CREATE TABLE IF NOT EXISTS scripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(100) NOT NULL,
    content TEXT,
    duration INTEGER,
    word_count INTEGER,
    voice_id INTEGER,
    bgm_id INTEGER,
    status VARCHAR(20) DEFAULT 'draft',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Digital humans table
CREATE TABLE IF NOT EXISTS digital_humans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(500),
    preview_url VARCHAR(500),
    gender VARCHAR(10),
    age_range VARCHAR(20),
    style TEXT,
    category VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    thumbnail_url VARCHAR(500),
    description TEXT,
    tags TEXT,
    is_public VARCHAR(1) DEFAULT '0',
    watch_count INTEGER DEFAULT 0,
    use_count INTEGER DEFAULT 0,
    source VARCHAR(20) DEFAULT 'photo',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Video projects table
CREATE TABLE IF NOT EXISTS video_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    script_id INTEGER,
    digital_human_id INTEGER,
    category VARCHAR(50),
    duration INTEGER,
    status VARCHAR(20) DEFAULT 'draft',
    output_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Video outputs table
CREATE TABLE IF NOT EXISTS video_outputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    video_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    duration DECIMAL(10, 2),
    file_size INTEGER,
    format VARCHAR(20),
    resolution VARCHAR(20),
    share_token VARCHAR(100),
    share_password VARCHAR(100),
    share_expire_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type VARCHAR(20) NOT NULL,
    title VARCHAR(200),
    content TEXT,
    is_read VARCHAR(1) DEFAULT '0',
    read_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Notification settings table
CREATE TABLE IF NOT EXISTS user_notification_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    email_enabled VARCHAR(1) DEFAULT '1',
    sms_enabled VARCHAR(1) DEFAULT '1',
    push_enabled VARCHAR(1) DEFAULT '1',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()

print("Database created successfully!")
conn = sqlite3.connect('api_test.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", [t[0] for t in cursor.fetchall()])
conn.close()

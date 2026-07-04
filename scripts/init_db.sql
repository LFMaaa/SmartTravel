-- ============================================================
-- SmartTravel（智游）数据库初始化脚本
-- 版本: V1.0  |  兼容: MySQL 8.4+
-- 对应 PRD §7.2 MySQL 核心表设计
-- 用法: 首次启动时由 docker-entrypoint-initdb.d 自动执行
-- ============================================================

CREATE DATABASE IF NOT EXISTS smarttravel
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE smarttravel;

-- ============================================================
-- §1. 用户表
-- PRD: users — 账号 + OAuth 绑定
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id              VARCHAR(36)  PRIMARY KEY,
    nickname        VARCHAR(50)  DEFAULT '',
    phone           VARCHAR(20)  UNIQUE,
    avatar_url      VARCHAR(500) DEFAULT NULL,
    oauth_provider  VARCHAR(20)  DEFAULT NULL         COMMENT 'wechat / alipay',
    oauth_openid    VARCHAR(100) DEFAULT NULL,
    oauth_unionid   VARCHAR(100) DEFAULT NULL,
    hashed_password VARCHAR(255) DEFAULT NULL         COMMENT '密码哈希（OAuth 用户为空）',
    salt            VARCHAR(32)  DEFAULT NULL         COMMENT '密码盐值',
    sms_code        VARCHAR(6)   DEFAULT NULL         COMMENT '短信验证码',
    sms_code_expires_at DATETIME DEFAULT NULL         COMMENT '短信验证码过期时间',
    is_pro          BOOLEAN      DEFAULT FALSE        COMMENT '是否为Pro会员',
    pro_expire_at   DATETIME     DEFAULT NULL         COMMENT 'Pro会员过期时间',
    last_login_at   DATETIME     DEFAULT NULL,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_oauth (oauth_provider, oauth_openid),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §2. 用户偏好表
-- PRD: user_preferences — JSON 存储，避免过度拆表
-- ============================================================
CREATE TABLE IF NOT EXISTS user_preferences (
    id                    VARCHAR(36) PRIMARY KEY,
    user_id               VARCHAR(36) NOT NULL UNIQUE,
    travel_style          JSON DEFAULT NULL           COMMENT '{"pace":"悠闲","type":"文化","companion":"家庭"}',
    budget_range          JSON DEFAULT NULL           COMMENT '{"min":2000,"max":5000,"per_day":500}',
    constraints           JSON DEFAULT NULL           COMMENT '{"no_climbing":true,"max_walk_steps":8000}',
    favorite_destinations JSON DEFAULT NULL           COMMENT '["成都","京都","大理"]',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §3. 行程主表
-- PRD: itineraries — 一次出行计划的顶层容器
-- ============================================================
CREATE TABLE IF NOT EXISTS itineraries (
    id                    VARCHAR(36)  PRIMARY KEY,
    user_id               VARCHAR(36)  NOT NULL,
    title                 VARCHAR(200) NOT NULL DEFAULT '未命名行程',
    destination           VARCHAR(100) NOT NULL        COMMENT '主要目的地城市',
    start_date            DATE         DEFAULT NULL,
    end_date              DATE         DEFAULT NULL,
    days                  INT          NOT NULL DEFAULT 1,
    total_budget          DECIMAL(10,2) DEFAULT NULL,
    status                ENUM('draft','planned','in_progress','completed','cancelled')
                                      DEFAULT 'draft',
    source                ENUM('ai_generated','manual','cloned','replanned')
                                      DEFAULT 'ai_generated',
    dify_workflow_run_id  VARCHAR(100) DEFAULT NULL    COMMENT 'Dify 运行ID，用于调试追踪',
    raw_input             JSON         DEFAULT NULL    COMMENT '用户原始自然语言输入',
    created_at            DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_status  (user_id, status),
    INDEX idx_destination  (destination),
    INDEX idx_created      (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §4. 行程日表
-- PRD: itinerary_days — 行程中每一天的容器
-- ============================================================
CREATE TABLE IF NOT EXISTS itinerary_days (
    id            VARCHAR(36) PRIMARY KEY,
    itinerary_id  VARCHAR(36) NOT NULL,
    day_number    INT         NOT NULL,
    date          DATE        DEFAULT NULL,
    weather       JSON        DEFAULT NULL             COMMENT '{temp,condition,icon} 来自和风天气',
    day_notes     TEXT        DEFAULT NULL,
    FOREIGN KEY (itinerary_id) REFERENCES itineraries(id) ON DELETE CASCADE,
    UNIQUE KEY uk_itinerary_day (itinerary_id, day_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §5. 日程活动表
-- PRD: day_activities — 每个活动单元的详细信息
-- ============================================================
CREATE TABLE IF NOT EXISTS day_activities (
    id                    VARCHAR(36)  PRIMARY KEY,
    day_id                VARCHAR(36)  NOT NULL,
    activity_type         ENUM('attraction','hotel','restaurant','transport','other')
                                      NOT NULL,
    name                  VARCHAR(200) NOT NULL,
    address               VARCHAR(500) DEFAULT NULL,
    latitude              DECIMAL(10,7) DEFAULT NULL,
    longitude             DECIMAL(10,7) DEFAULT NULL,
    duration_minutes      INT          DEFAULT 60,
    estimated_cost        DECIMAL(10,2) DEFAULT 0,
    sort_order            INT          NOT NULL,
    transportation        VARCHAR(50)  DEFAULT NULL     COMMENT 'walk/drive/bus/metro/taxi',
    travel_time_from_prev INT          DEFAULT 0        COMMENT '从上个活动过来的交通时间（分钟）',
    ai_reason             TEXT         DEFAULT NULL     COMMENT 'AI 推荐理由',
    metadata              JSON         DEFAULT NULL     COMMENT '扩展字段：图片/评分/联系电话等',
    FOREIGN KEY (day_id) REFERENCES itinerary_days(id) ON DELETE CASCADE,
    INDEX idx_day_order (day_id, sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §6. 行程版本表
-- PRD: itinerary_versions — 支持 undo/redo 和多方案对比
-- ============================================================
CREATE TABLE IF NOT EXISTS itinerary_versions (
    id                  VARCHAR(36)  PRIMARY KEY,
    itinerary_id        VARCHAR(36)  NOT NULL,
    version_number      INT          NOT NULL,
    change_description  VARCHAR(200) DEFAULT NULL,
    snapshot            JSON         NOT NULL            COMMENT '完整行程快照',
    trigger_event       VARCHAR(100) DEFAULT NULL        COMMENT '触发原因: user_edit / ai_replan / flight_delay',
    created_at          DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (itinerary_id) REFERENCES itineraries(id) ON DELETE CASCADE,
    UNIQUE KEY uk_version (itinerary_id, version_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §7. 订单主表
-- PRD: orders — 一次支付订单
-- ============================================================
CREATE TABLE IF NOT EXISTS orders (
    id              VARCHAR(36)  PRIMARY KEY,
    user_id         VARCHAR(36)  NOT NULL,
    itinerary_id    VARCHAR(36)  DEFAULT NULL,
    status          ENUM('pending','paid','timeout','cancelled','refunded')
                                DEFAULT 'pending',
    payment_status  ENUM('unpaid','paid','refunding','refunded')
                                DEFAULT 'unpaid',
    total_amount    DECIMAL(10,2) NOT NULL DEFAULT 0,
    delay_token     VARCHAR(100) DEFAULT NULL            COMMENT '延迟支付 Token（Redis Key）',
    expire_at       DATETIME     DEFAULT NULL            COMMENT '延迟支付过期时间',
    paid_at         DATETIME     DEFAULT NULL,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_status (user_id, status),
    INDEX idx_expire      (expire_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §8. 订单项表
-- PRD: order_items — 订单中每项预订资源
-- ============================================================
CREATE TABLE IF NOT EXISTS order_items (
    id              VARCHAR(36)  PRIMARY KEY,
    order_id        VARCHAR(36)  NOT NULL,
    resource_type   ENUM('hotel','ticket','flight','restaurant','insurance')
                                NOT NULL,
    resource_id     VARCHAR(100) NOT NULL,
    resource_name   VARCHAR(200) NOT NULL,
    unit_price      DECIMAL(10,2) NOT NULL,
    quantity        INT          DEFAULT 1,
    booking_date    DATE         DEFAULT NULL,
    check_in        DATETIME     DEFAULT NULL,
    check_out       DATETIME     DEFAULT NULL,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §9. 预订记录表
-- PRD: bookings — 行程与订单的关联，记录实际预订状态
-- ============================================================
CREATE TABLE IF NOT EXISTS bookings (
    id              VARCHAR(36) PRIMARY KEY,
    itinerary_id    VARCHAR(36) NOT NULL,
    order_id        VARCHAR(36) DEFAULT NULL,
    resource_type   VARCHAR(50) NOT NULL,
    resource_id     VARCHAR(100) NOT NULL,
    status          ENUM('reserved','confirmed','cancelled','refunded')
                               DEFAULT 'reserved',
    check_in        DATETIME    DEFAULT NULL,
    check_out       DATETIME    DEFAULT NULL,
    created_at      DATETIME    DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (itinerary_id) REFERENCES itineraries(id) ON DELETE CASCADE,
    FOREIGN KEY (order_id)     REFERENCES orders(id)     ON DELETE SET NULL,
    INDEX idx_itinerary (itinerary_id),
    INDEX idx_order     (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §10. 通知消息表
-- 用于 notification-service 推送记录持久化
-- ============================================================
CREATE TABLE IF NOT EXISTS notifications (
    id              VARCHAR(36)  PRIMARY KEY,
    user_id         VARCHAR(36)  NOT NULL,
    type            ENUM('replan_alert','payment_reminder','schedule_reminder','system')
                                NOT NULL,
    title           VARCHAR(200) NOT NULL,
    content         JSON         DEFAULT NULL,
    is_read         BOOLEAN      DEFAULT FALSE,
    resource_type   VARCHAR(50)  DEFAULT NULL,
    resource_id     VARCHAR(36)  DEFAULT NULL,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_read  (user_id, is_read),
    INDEX idx_created    (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §11. 操作审计日志表
-- PRD: audit_logs — 关键操作追踪（面试演示用）
-- ============================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id              VARCHAR(36)  PRIMARY KEY,
    user_id         VARCHAR(36)  DEFAULT NULL,
    action          VARCHAR(50)  NOT NULL               COMMENT '操作类型: login/generate/replan/create_order/pay',
    resource_type   VARCHAR(50)  NOT NULL               COMMENT '资源类型: user/itinerary/order/booking',
    resource_id     VARCHAR(36)  DEFAULT NULL,
    detail          JSON         DEFAULT NULL           COMMENT '操作详情',
    ip_address      VARCHAR(45)  DEFAULT NULL,
    user_agent      VARCHAR(500) DEFAULT NULL,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_time   (user_id, created_at),
    INDEX idx_resource    (resource_type, resource_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §12. POI 表（景点/酒店/餐厅基础数据）
-- 用于搜索服务数据源，ES 索引同步来源
-- ============================================================
CREATE TABLE IF NOT EXISTS poi (
    id              VARCHAR(36)  PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    type            ENUM('attraction','hotel','restaurant','transport','other')
                                NOT NULL,
    city            VARCHAR(50)  NOT NULL,
    district        VARCHAR(100) DEFAULT NULL,
    address         VARCHAR(500) DEFAULT NULL,
    latitude        DECIMAL(10,7) NOT NULL,
    longitude       DECIMAL(10,7) NOT NULL,
    price_range     JSON         DEFAULT NULL            COMMENT '{"min":100,"max":500}',
    rating          FLOAT        DEFAULT 0,
    tags            JSON         DEFAULT NULL            COMMENT '["历史文化","亲子","美食"]',
    description     TEXT         DEFAULT NULL,
    opening_hours   VARCHAR(500) DEFAULT NULL,
    image_url       VARCHAR(500) DEFAULT NULL,
    popularity_score FLOAT       DEFAULT 0,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type_city   (type, city),
    INDEX idx_location    (latitude, longitude),
    INDEX idx_popularity  (popularity_score DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- §13. POI 评论/评价表
-- 用户对景点/酒店/餐厅的评价，支持多级回复（类似抖音评论）
-- ============================================================
CREATE TABLE IF NOT EXISTS poi_reviews (
    id              VARCHAR(36)  PRIMARY KEY,
    poi_id          VARCHAR(36)  NOT NULL            COMMENT '被评价的 POI ID',
    user_id         VARCHAR(36)  NOT NULL            COMMENT '评价用户 ID',
    parent_id       VARCHAR(36)  DEFAULT NULL        COMMENT '父评论 ID（回复时指向被回复的评论，NULL=一级评论）',
    content         TEXT         NOT NULL            COMMENT '评论内容',
    rating          TINYINT      DEFAULT NULL        COMMENT '评分 1-5（仅一级评论有评分，回复为 NULL）',
    likes           INT          DEFAULT 0           COMMENT '点赞数',
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES poi_reviews(id) ON DELETE CASCADE,
    INDEX idx_poi (poi_id),
    INDEX idx_parent (parent_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
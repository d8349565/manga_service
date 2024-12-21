# Manga_service

这是一个基于 FastAPI 开发的漫画网站后端服务，提供漫画内容管理、用户管理、阅读进度追踪等功能。

项目主要是把采集到的漫画数据通过网页加载阅读，可在同WiFi局域网内的电脑、平板、手机等各类设备上看漫画。

**仅用于交流学习，勿做他用。**

## 主要功能

### 1. 用户系统

- 用户注册与登录(登入页面：http://localhost:8812/static/login.html)
- 用户 token 认证
- 用户角色管理(普通用户/管理员)

### 2. 漫画管理

- 通过爬虫将漫画数据导入数据库，数据库结构如下：
- 在manga_site/backend/app/core/config.py 中修改MySQL 数据库配置。
```
[User] 用户表
├── id: Integer (PK)
├── email: String (唯一索引)
├── hashed_password: String
├── role: Enum(admin/user)
└── is_active: Boolean

[Comic] 漫画表
├── id: Integer (PK)
├── title: String (索引)
├── author: String
├── description: Text
└── cover_image: String

[Chapter] 章节表
├── id: Integer (PK)
├── comic_id: Integer (FK -> Comic.id)
├── chapter_number: Integer
├── title: String
└── images: Text (JSON)

[ReadingProgress] 阅读进度表
├── id: Integer (PK)
├── user_id: Integer (FK -> User.id)
├── comic_id: Integer (FK -> Comic.id)
├── chapter_id: Integer (FK -> Chapter.id)
├── scroll_position: Float
└── last_read_at: DateTime

关系:
- Comic 1:N Chapter (一本漫画有多个章节)
- User N:M Comic (通过 ReadingProgress 多对多关联)
- Chapter 1:N ReadingProgress (一个章节可以被多个用户阅读)
```
### 3. 阅读功能

- 漫画阅读器
- 支持PWA，实现添加到主屏幕功能
- 阅读进度自动保存
- 支持章节导航(上一章/下一章)
- 阅读历史记录
- 缓存
- ......

## 技术特点

- 基于 FastAPI 框架开发
- SQLite 数据库存储（其他分支为 MySQL 数据库版本）
- Docker 容器化部署
- 异步处理
- 清华镜像源加速

## 项目结构

```
backend/
├── app/
│   ├── api/            # API 路由
│   ├── core/           # 核心配置
│   ├── db/             # 数据库相关
│   ├── models/         # 数据模型
├── static/             # 静态文件
│   ├── admin.html      # 管理后台页面
│   ├── comics.html     # 漫画列表页面
│   ├── chapters.html   # 章节列表页面
│   ├── login.html      # 登录页面
│   ├── reader.html     # 阅读器页面
│   └── manifest.json   # PWA配置文件
├── Dockerfile          # Docker 配置
└── docker-compose.yml  # Docker Compose 配置
```

## 快速开始

### 使用 Docker 部署

1. 构建并启动服务：
```bash
git clone https://github.com/d8349565/manga_service.git
cd backend
docker-compose up -d
```

2. 服务将在 8812 端口启动

### 本地开发

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行服务：
```bash
cd backend
python main.py
```

## API 接口

### 认证相关
- POST `/api/auth/register` - 用户注册
- POST `/api/auth/login` - 用户登录
- GET `/api/auth/me` - 获取当前用户信息

### 漫画相关
- GET `/api/comics` - 获取漫画列表
- POST `/api/comics` - 创建新漫画
- GET `/api/comics/{comic_id}` - 获取漫画详情
- DELETE `/api/comics/{comic_id}` - 删除漫画

### 章节相关
- GET `/api/comics/{comic_id}/chapters` - 获取章节列表
- POST `/api/comics/{comic_id}/chapters` - 创建新章节
- GET `/api/chapters/{chapter_id}` - 获取章节详情

### 阅读相关
- GET `/api/reader/comics/{comic_id}/read/{chapter_id}` - 获取阅读内容
- GET `/api/reader/comics/{comic_id}/progress` - 获取阅读进度
- POST `/api/reader/progress` - 更新阅读进度
- GET `/api/reader/history` - 获取阅读历史

## 数据存储

- 用户数据、漫画信息存储在 SQLite 数据库中（web 分支为MySQL 数据库版本）
- 使用 Docker volume 持久化数据

## 注意事项

1. 首次使用需要重新注册管理员账户密码（默认为 账户 admin 密码 admin）
1. docker 部署、内网穿透、域名、ddns 等设置请自行搜索完成。
1. 项目地址：https://github.com/d8349565/manga_service

# 漫画阅读网站

一个基于 FastAPI 和 SQLite 的在线漫画阅读网站。

## 功能特点

- 用户系统
  - 用户注册和登录
  - 管理员账号管理
  - JWT token 认证
  
- 漫画管理
  - 漫画上传和管理
  - 章节管理
  - 图片优化和处理
  
- 阅读功能
  - 在线阅读
  - 阅读进度保存
  - 收藏功能
  - 阅读历史记录
  
- 其他功能
  - 响应式设计
  - 图片优化
  - 用户设置

## 技术栈

### 后端
- FastAPI
- SQLAlchemy
- Pydantic
- JWT
- Pillow

### 前端
- HTML5
- CSS3
- JavaScript

## 安装和运行

1. 克隆项目 
git clone <repository-url>
cd manga_site
2. 创建虚拟环境
python -m venv venv
source venv/bin/activate # Linux/Mac
或
.\venv\Scripts\activate # Windows
3. 安装依赖
pip install -r requirements.txt
cp .env.example .env
编辑 .env 文件，设置必要的环境变量
5. 运行项目
cd backend
uvicorn main:app --reload

访问 http://localhost:8000 即可使用。

## 项目结构
manga_site/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ └── endpoints/
│ │ ├── core/
│ │ ├── db/
│ │ ├── models/
│ │ └── utils/
│ ├── static/
│ └── main.py
└── requirements.txt

## API 文档

启动服务后访问 http://localhost:8000/docs 查看完整的 API 文档。

## 主要 API 端点

- `/api/auth/register` - 用户注册
- `/api/auth/login` - 用户登录
- `/api/comics` - 漫画管理
- `/api/chapters` - 章节管理
- `/api/reader` - 阅读相关

## 开发说明

### 数据库

项目使用 SQLite 数据库，数据库文件会自动创建。主要数据表包括：
- users - 用户信息
- comics - 漫画信息
- chapters - 章节信息
- reading_progress - 阅读进度

### 图片存储

图片文件存储在 `uploads` 目录下，目录结构如下：
uploads/
├── covers/ # 漫画封面
└── chapters/ # 章节图片
└── {comic_id}/
└── {chapter_number}/

### 权限控制

- 普通用户：阅读、收藏、记录阅读进度
- 管理员：额外拥有漫画管理权限
  - 上传新漫画
  - 管理章节
  - 删除内容

## 前端页面

- `/static/comics.html` - 漫画列表页
- `/static/chapters.html` - 章节列表页
- `/static/reader.html` - 阅读页面
- `/static/favorites.html` - 收藏页面
- `/static/history.html` - 历史记录页
- `/static/settings.html` - 设置页面
- `/static/admin.html` - 管理页面

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。

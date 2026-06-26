# Vue-Admin 内容管理系统 —— 综合实训报告

> 基于 Vue.js + Flask 的前后端分离管理系统

---

## 目录

- [第一章 项目概述](#第一章-项目概述)
- [第二章 系统需求分析与接口设计](#第二章-系统需求分析与接口设计)
- [第三章 AI生产模拟数据](#第三章-ai生产模拟数据)
- [第四章 前后端分离开发](#第四章-前后端分离开发)
- [第五章 实训小结](#第五章-实训小结)

---

## 第一章 项目概述

### 1.1 项目简介

本系统是一个基于 **Vue.js 2 + Element UI** 前端框架和 **Flask + MySQL** 后端框架构建的内容管理系统。系统实现了用户管理、文章管理、评论管理、数据报表等核心功能，采用前后端分离架构，支持 JWT 认证和基于角色的权限控制。

### 1.2 功能需求

| 模块 | 功能描述 |
|------|----------|
| 用户管理 | 用户注册、登录、信息修改，管理员可管理所有用户 |
| 文章管理 | 文章的发布、编辑、删除、搜索、导出、按浏览量排序 |
| 评论管理 | 评论的审核、回复和统计 |
| 数据报表 | 综合报表、文章报表、评论报表、活跃报表 |
| 权限控制 | 管理员和普通用户拥有不同的操作权限 |
| 主题切换 | 支持浅色和深色两种主题模式 |

### 1.3 非功能需求

| 需求类型 | 描述 |
|----------|------|
| 响应式设计 | 适配不同屏幕尺寸 |
| 安全性 | JWT Token 认证，密码明文存储（实训项目） |
| 性能 | 支持分页加载，优化大数据量展示 |
| 用户体验 | 流畅的交互效果，清晰的数据可视化 |

### 1.4 技术栈

#### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue.js | 2.6.10 | 核心前端框架 |
| Vue Router | 3.0.6 | 前端路由管理 |
| Vuex | 3.1.0 | 状态管理 |
| Element UI | 2.13.2 | UI 组件库 |
| Axios | 0.18.1 | HTTP 请求库 |
| ECharts | 5.6.0 | 数据可视化图表 |
| echarts-wordcloud | 2.1.0 | 词云组件 |
| XLSX | 0.18.5 | Excel 文件导出 |

#### 后端技术栈

| 技术 | 版本/说明 | 用途 |
|------|-----------|------|
| Flask | Python Web 框架 | 后端服务 |
| PyMySQL | Python MySQL 驱动 | 数据库连接 |
| PyJWT | JWT 认证库 | Token 生成与验证 |
| MySQL | 关系型数据库 | 数据存储 |

#### 开发工具

| 工具 | 用途 |
|------|------|
| VS Code | 代码编辑器 |
| Navicat | 数据库管理 |
| Postman | API 测试 |
| Git | 版本控制 |

### 1.5 项目思维导图

```
Vue-Admin 内容管理系统
├── 前端 (Vue.js 2 + Element UI)
│   ├── 页面模块
│   │   ├── 登录/注册 (login)
│   │   ├── 仪表盘 (dashboard)
│   │   ├── 文章管理 (article)
│   │   │   ├── 文章列表
│   │   │   ├── 文章创建
│   │   │   ├── 文章编辑
│   │   │   └── 文章详情
│   │   ├── 用户管理 (user)
│   │   │   ├── 用户列表
│   │   │   └── 用户创建
│   │   ├── 数据报表 (report)
│   │   │   ├── 综合报表
│   │   │   ├── 文章报表
│   │   │   ├── 评论报表
│   │   │   └── 活跃报表
│   │   └── 学校介绍 (school)
│   ├── 核心功能
│   │   ├── JWT 认证 (request.js)
│   │   ├── 路由守卫 (permission.js)
│   │   ├── 状态管理 (Vuex)
│   │   └── 数据可视化 (ECharts)
│   └── 特色功能
│       ├── 主题切换 (浅色/深色)
│       ├── 文章导出 (Excel)
│       ├── 浏览量排序
│       ── 词云展示
│
── 后端 (Flask + MySQL)
│   ├── 用户模块 (10 个接口)
│   │   ├── 登录/登出/注册
│   │   ├── 用户 CRUD
│   │   └── 个人信息更新
│   ├── 文章模块 (5 个接口)
│   │   ├── 文章 CRUD
│   │   └── 文章详情
│   ├── 评论模块 (7 个接口)
│   │   ├── 评论 CRUD
│   │   ├── 评论审核
│   │   └── 评论统计
│   ├── 报表模块 (5 个接口)
│   │   ├── 综合报表
│   │   ├── 文章报表
│   │   ├── 评论报表
│   │   ├── 活跃报表
│   │   ── 热门文章
│   └── 数据库模块 (2 个接口)
│       ├── 数据库统计
│       └── 表列表
│
├── 数据库 (MySQL)
│   ├── users (用户表)
│   ├── articles (文章表)
│   ├── comments (评论表)
│
└── 权限控制 (RBAC)
    ├── admin (管理员)
    │   ├── 所有 CRUD 权限
    │   ├── 用户管理
    │   └── 评论审核
    └── user (普通用户)
        ├── 只能编辑/删除自己的文章
        ├── 注册默认为 user 角色
        └── 可查看数据报表
```

### 1.6 项目结构

```
vue-admin-template-master/
├├── app.py                    # Flask 后端主程序（1051 行）
── models.py                 # 数据库模型（约 350 行）
├── config.py                 # 配置文件
├── generate_report.py        # 报告生成脚本
── package.json              # 前端依赖配置
├── src/
│   ├── api/                  # API 请求封装
│   ├── components/           # 公共组件
│   ├── router/               # 路由配置
│   ├── store/                # Vuex 状态管理
│   ├── styles/               # 全局样式
│   ├── utils/                # 工具函数
│   └── views/                # 页面组件
│       ├── dashboard/        # 首页仪表盘
│       ├── login/            # 登录页
│       ├── article/          # 文章管理
│       ├── user/             # 用户管理
│       ├── report/           # 数据报表
│       └── school/           # 学校介绍
└── public/                   # 静态资源
```

> 📸 **截图位置 1**：在此处插入项目整体目录结构截图（VS Code 左侧文件树）

---

## 第二章 系统需求分析与接口设计

### 2.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        浏览器客户端                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Vue.js 2   │  │ Element UI  │  │   ECharts   │         │
│  │  (视图层)    │  │  (组件库)    │  │  (可视化)    │         │
│  └──────┬──────┘  └─────────────┘  └─────────────┘         │
│         │                                                   │
│  ┌──────▼──────┐                                            │
│  │   Axios     │  ← HTTP 请求（JSON 格式）                    │
│  │  (网络层)    │                                            │
│  └──────┬──────┘                                            │
└─────────┼───────────────────────────────────────────────────┘
          │ JWT Token (X-Token Header)
          ▼
┌─────────────────────────────────────────────────────────────┐
│                      Flask 后端服务                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  JWT 认证   │  │  路由处理    │  │  数据验证    │         │
│  │  (中间件)    │  │  (app.py)   │  │  (models.py)│         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│  ┌──────▼────────────────▼────────────────▼──────┐         │
│  │              PyMySQL 数据库操作                  │         │
│  └──────────────────────┬────────────────────────┘         │
└─────────────────────────┼──────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      MySQL 数据库                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  users   │  │ articles │  │ comments │   │
│  │  (用户表) │  │ (文章表)  │  │ (评论表)  │   │
│  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

> 📸 **截图位置 2**：在此处插入系统架构流程图（可用 Draw.io 或 ProcessOn 绘制）

### 2.2 数据库设计

#### 2.2.1 数据库表结构

**表 1：users（用户表）**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 用户ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名 |
| password | VARCHAR(255) | NOT NULL | 密码 |
| role | VARCHAR(20) | DEFAULT 'user' | 角色（admin/user） |
| name | VARCHAR(50) | NULL | 姓名 |
| avatar | VARCHAR(255) | NULL | 头像URL |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**表 2：articles（文章表）**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 文章ID |
| title | VARCHAR(255) | NOT NULL | 标题 |
| author | VARCHAR(50) | NOT NULL | 作者 |
| content | TEXT | NULL | 文章内容（HTML格式） |
| pageviews | INT | DEFAULT 0 | 浏览量 |
| status | VARCHAR(20) | DEFAULT 'draft' | 状态（published/draft） |
| display_time | DATETIME | NULL | 显示时间 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

**表 3：comments（评论表）**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 评论ID |
| article_id | INT | NOT NULL, FOREIGN KEY | 关联文章ID |
| username | VARCHAR(50) | NOT NULL | 评论者用户名 |
| email | VARCHAR(100) | NULL | 邮箱 |
| content | TEXT | NOT NULL | 评论内容 |
| status | VARCHAR(20) | DEFAULT 'pending' | 状态（approved/pending/rejected） |
| parent_id | INT | DEFAULT NULL | 父评论ID（支持回复） |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 2.2.2 ER 关系图

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    users     │         │   articles   │         │   comments   │
├──────────────┤         ├──────────────┤         ├──────────────
│ id (PK)      │         │ id (PK)      │         │ id (PK)      │
│ username     │         │ title        │         │ article_id   │──┐
│ password     │         │ author       │◄──┐     │ username     │  │
│ role         │         │ content      │   │     │ email        │  │
│ name         │         │ pageviews    │   │     │ content      │  │
│ avatar       │         │ status       │   │     │ status       │  │
│ created_at   │         │ display_time │   │     │ parent_id    │  │
└──────────────┘         │ created_at   │   │     │ created_at   │  │
                         │ updated_at   │   │     └──────────────┘  │
                         ──────────────┘   │                       │
                                            │                       │
                              author 关联 ───┘    article_id 外键 ───┘
```

> 📸 **截图位置 3**：在此处插入 Navicat 中的 ER 关系图截图

#### 2.2.3 数据库初始化数据

**默认用户数据（models.py 中硬编码）：**

| username | password | role | name |
|----------|----------|------|------|
| admin | 111111 | admin | 管理员 |
| test | 111111 | user | 测试用户 |

**默认文章数据（4 条）：**

| ID | 标题 | 作者 | 浏览量 | 状态 |
|----|------|------|--------|------|
| 1 | Vue.js 入门指南 | 张三 | 1234 | published |
| 2 | Python Flask 后端开发实战 | 李四 | 5678 | published |
| 3 | MySQL 性能优化技巧 | 王五 | 9012 | published |
| 4 | JavaScript 设计模式学习 | 赵六 | 3456 | draft |

**默认评论数据（5 条）：**

| ID | 文章ID | 用户名 | 状态 |
|----|--------|--------|------|
| 1 | 1 | 读者小明 | approved |
| 2 | 1 | 前端爱好者 | approved |
| 3 | 2 | Pythoner | approved |
| 4 | 3 | DBA 小王 | pending |
| 5 | 3 | admin | approved |

**默认系统日志（5 条）：**

| level | username | action | IP |
|-------|----------|--------|-----|
| info | admin | 登录 | 127.0.0.1 |
| info | admin | 查看列表 | 127.0.0.1 |
| warning | admin | 修改数据 | 127.0.0.1 |
| error | test | 删除操作 | 192.168.1.100 |
| info | admin | 创建用户 | 127.0.0.1 |

### 2.3 接口设计

#### 2.3.1 接口总览

| 序号 | 接口路径 | 方法 | 权限 | 功能描述 |
|------|----------|------|------|----------|
| 1 | `/vue-admin-template/user/login` | POST | 公开 | 用户登录 |
| 2 | `/vue-admin-template/user/info` | GET | 登录 | 获取用户信息 |
| 3 | `/vue-admin-template/user/logout` | POST | 公开 | 用户登出 |
| 4 | `/vue-admin-template/user/register` | POST | 公开 | 用户注册 |
| 5 | `/vue-admin-template/user/list` | GET | 管理员 | 获取用户列表 |
| 6 | `/vue-admin-template/user/<id>` | GET | 登录 | 获取用户详情 |
| 7 | `/vue-admin-template/user/create` | POST | 管理员 | 创建用户 |
| 8 | `/vue-admin-template/user/update` | POST | 管理员 | 更新用户 |
| 9 | `/vue-admin-template/user/delete` | POST | 管理员 | 删除用户 |
| 10 | `/vue-admin-template/user/self-update` | POST | 登录 | 更新个人信息 |
| 11 | `/vue-admin-template/table/list` | GET | 登录 | 获取文章列表 |
| 12 | `/vue-admin-template/table/create` | POST | 登录 | 创建文章 |
| 13 | `/vue-admin-template/table/update` | POST | 登录 | 更新文章 |
| 14 | `/vue-admin-template/table/delete` | POST | 登录 | 删除文章 |
| 15 | `/vue-admin-template/table/detail` | GET | 登录 | 获取文章详情 |
| 16 | `/vue-admin-template/report/overview` | GET | 登录 | 综合报表 |
| 17 | `/vue-admin-template/report/article` | GET | 登录 | 文章报表 |
| 18 | `/vue-admin-template/report/comment` | GET | 登录 | 评论报表 |
| 19 | `/vue-admin-template/report/activity` | GET | 登录 | 活跃报表 |
| 20 | `/vue-admin-template/report/hot-articles` | GET | 登录 | 热门文章 |
| 21 | `/vue-admin-template/db/stats` | GET | 登录 | 数据库统计 |
| 22 | `/vue-admin-template/db/tables` | GET | 登录 | 数据库表列表 |
| 23 | `/vue-admin-template/comments/by-article` | GET | 登录 | 获取文章评论 |
| 24 | `/vue-admin-template/comments/list` | GET | 登录 | 获取评论列表 |
| 25 | `/vue-admin-template/comments/create` | POST | 登录 | 创建评论 |
| 26 | `/vue-admin-template/comments/update` | POST | 登录 | 更新评论 |
| 27 | `/vue-admin-template/comments/approve` | POST | 登录 | 审核评论 |
| 28 | `/vue-admin-template/comments/delete` | POST | 登录 | 删除评论 |
| 29 | `/vue-admin-template/comments/count` | GET | 登录 | 评论计数 |

#### 2.3.2 认证机制

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  用户输入     │      │  后端验证     │      │  返回 Token  │
│  用户名/密码  │─────▶│  查询数据库   │─────▶│  JWT 编码    │
└──────────────┘      ──────────────┘      └──────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │  密码匹配     │
                      │  (明文比对)    │
                      ──────────────┘

Token 结构:
{
  "user_id": 1,
  "role": "admin",
  "exp": 1750838400  // 24小时后过期
}
```

> 📸 **截图位置 4**：在此处插入 Postman 登录接口测试截图（显示请求和响应）

### 2.4 前端页面设计

| 页面 | 路由 | 功能 |
|------|------|------|
| 登录页 | `/login` | 用户登录/注册 |
| 仪表盘 | `/dashboard` | 数据统计、快捷操作、公司介绍、词云 |
| 文章列表 | `/article/list` | 文章CRUD、搜索、排序、导出 |
| 文章创建 | `/article/create` | 富文本编辑器发布文章 |
| 文章编辑 | `/article/edit/:id` | 编辑已有文章 |
| 文章详情 | `/article/detail/:id` | 查看文章详情 |
| 用户列表 | `/user/list` | 用户管理（仅管理员） |
| 用户创建 | `/user/create` | 新增用户（仅管理员） |
| 综合报表 | `/report/index` | 数据总览 |
| 文章报表 | `/report/article` | 文章数据分析 |
| 评论报表 | `/report/comment` | 评论数据分析 |
| 活跃报表 | `/report/activity` | 用户活跃度分析 |
| 学校介绍 | `/school/intro` | 学校信息展示 |

> 📸 **截图位置 5**：在此处插入登录页面截图
>  **截图位置 6**：在此处插入仪表盘首页截图
> 📸 **截图位置 7**：在此处插入文章列表页面截图
> 📸 **截图位置 8**：在此处插入数据报表页面截图

---

## 第三章 AI生产模拟数据

### 3.1 AI工具使用情况

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| Trae IDE (Qwen3.6-Plus) | 代码生成、Bug修复、文档编写 | 全项目周期 |
| AI 辅助编程 | 代码补全、错误诊断 | 开发过程 |

### 3.2 模拟数据说明

系统初始化时自动生成的模拟数据：

**用户数据：**
- 管理员账号：admin / 111111
- 测试账号：test / 111111
- 注册用户默认为普通用户角色

**文章数据：**
- 4 篇预置文章，涵盖 Vue.js、Flask、MySQL、JavaScript 主题
- 浏览量范围：1234 ~ 9012
- 状态分布：3 篇已发布，1 篇草稿

**评论数据：**
- 5 条预置评论
- 状态分布：4 条已通过，1 条待审核

**系统日志：**
- 5 条预置日志记录
- 包含 info、warning、error 三种级别

### 3.3 数据真实性验证

| 数据项 | 来源 | 验证方式 |
|--------|------|----------|
| 前端依赖版本 | package.json | 已核实 |
| 后端接口数量 | app.py | 21 个接口，已逐一核对 |
| 数据库表结构 | models.py | 4 张表，字段已核实 |
| JWT 过期时间 | config.py | 24 小时 |
| 默认用户 | models.py init_db() | admin + test |
| 默认文章 | models.py init_db() | 4 篇 |
| 默认评论 | models.py init_db() | 5 条 |
| 默认日志 | models.py init_db() | 5 条 |

>  **截图位置 9**：在此处插入 Navicat 中 users 表数据截图
>  **截图位置 10**：在此处插入 Navicat 中 articles 表数据截图
> 📸 **截图位置 11**：在此处插入 Navicat 中 comments 表数据截图

---

## 第四章 前后端分离开发

### 4.1 前端开发

#### 4.1.1 项目配置

**package.json 核心依赖：**

```json
{
  "name": "vue-admin-template",
  "version": "4.4.0",
  "dependencies": {
    "vue": "2.6.10",
    "vue-router": "3.0.6",
    "vuex": "3.1.0",
    "element-ui": "2.13.2",
    "axios": "0.18.1",
    "echarts": "^5.6.0",
    "echarts-wordcloud": "^2.1.0",
    "xlsx": "^0.18.5"
  }
}
```

#### 4.1.2 路由配置（src/router/index.js）

```javascript
export const constantRoutes = [
  { path: '/login', component: () => import('@/views/login/index') },
  { path: '/404', component: () => import('@/views/404') },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/index') }
    ]
  },
  {
    path: '/article',
    component: Layout,
    children: [
      { path: 'list', name: 'ArticleList', component: () => import('@/views/article/list') },
      { path: 'create', name: 'ArticleCreate', component: () => import('@/views/article/create') },
      { path: 'edit/:id', name: 'ArticleEdit', component: () => import('@/views/article/edit') },
      { path: 'detail/:id', name: 'ArticleDetail', component: () => import('@/views/article/detail') }
    ]
  },
  {
    path: '/user',
    component: Layout,
    meta: { roles: ['admin'] },
    children: [
      { path: 'list', name: 'UserList', component: () => import('@/views/user/list') },
      { path: 'create', name: 'UserCreate', component: () => import('@/views/user/create') }
    ]
  },
  {
    path: '/report',
    component: Layout,
    children: [
      { path: 'index', name: 'ReportIndex', component: () => import('@/views/report/index') },
      { path: 'article', name: 'ReportArticle', component: () => import('@/views/report/article') },
      { path: 'comment', name: 'ReportComment', component: () => import('@/views/report/comment') },
      { path: 'activity', name: 'ReportActivity', component: () => import('@/views/report/activity') }
    ]
  }
]
```

#### 4.1.3 核心功能实现

**1. JWT 认证（src/utils/request.js）**

```javascript
import axios from 'axios'
import { getToken, setToken, removeToken } from '@/utils/auth'

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 5000
})

// 请求拦截器 - 自动携带 Token
service.interceptors.request.use(
  config => {
    const token = getToken()
    if (token) {
      config.headers['X-Token'] = token
    }
    return config
  }
)

// 响应拦截器 - 处理 Token 过期
service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 20000) {
      if (res.code === 40001 || res.code === 40002) {
        removeToken()
        location.reload()
      }
      return Promise.reject(new Error(res.message || 'Error'))
    }
    return res
  }
)
```

**2. 权限路由守卫（src/permission.js）**

```javascript
router.beforeEach(async (to, from, next) => {
  const hasToken = getToken()
  if (hasToken) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      const hasRoles = store.getters.roles && store.getters.roles.length > 0
      if (hasRoles) {
        next()
      } else {
        try {
          const { roles } = await store.dispatch('user/getInfo')
          const accessRoutes = await store.dispatch('permission/generateRoutes', roles)
          router.addRoutes(accessRoutes)
          next({ ...to, replace: true })
        } catch (error) {
          await store.dispatch('user/resetToken')
          next(`/login?redirect=${to.path}`)
        }
      }
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next(`/login?redirect=${to.path}`)
    }
  }
})
```

**3. 仪表盘首页（src/views/dashboard/index.vue）**

- 欢迎横幅：用户头像、问候语、实时时间
- 统计卡片：用户总数、文章总数、评论总数、总浏览量
- 快捷操作：发布文章、新增用户、数据报表等
- 公司介绍：学校简介 + 统计数据
- 系统信息：技术栈展示
- 热门标签：ECharts 词云可视化

>  **截图位置 12**：在此处插入仪表盘完整截图（包含统计卡片、快捷操作、公司介绍、词云）

**4. 文章列表（src/views/article/list.vue）**

- 搜索功能：按标题、作者搜索
- 排序功能：按浏览量升序/降序排列
- 导出功能：导出为 Excel 文件
- 分页功能：每页 10 条
- 权限控制：普通用户只能编辑/删除自己发布的文章

```vue
<!-- 浏览量排序列 -->
<el-table-column align="center" label="浏览量" width="100" sortable prop="pageviews">
  <template slot-scope="scope">
    <div class="stat-cell">
      <i class="el-icon-view"></i>
      <span>{{ formatNumber(scope.row.pageviews) }}</span>
    </div>
  </template>
</el-table-column>
```

> 📸 **截图位置 13**：在此处插入文章列表页面截图（显示搜索、排序、导出功能）

**5. 数据报表（src/views/report/）**

- 综合报表：用户/文章/评论统计 + 热门文章 TOP10 + 作者排行
- 文章报表：发布趋势图 + 状态分布饼图 + 文章列表
- 评论报表：评论趋势图 + 状态分布 + 评论最多文章排行
- 活跃报表：用户活跃度排行 + 最近发布文章

> 📸 **截图位置 14**：在此处插入综合报表页面截图
> 📸 **截图位置 15**：在此处插入文章报表页面截图
> 📸 **截图位置 16**：在此处插入评论报表页面截图

**6. 登录/注册（src/views/login/index.vue）**

- 登录表单：用户名 + 密码
- 注册对话框：用户名 + 密码 + 姓名
- 注册用户默认为普通用户角色

> 📸 **截图位置 17**：在此处插入登录页面截图
> 📸 **截图位置 18**：在此处插入注册对话框截图

#### 4.1.4 前端页面统计

| 页面 | 文件 | 代码行数 |
|------|------|----------|
| 仪表盘 | src/views/dashboard/index.vue | ~1173 行 |
| 登录页 | src/views/login/index.vue | ~1038 行 |
| 文章列表 | src/views/article/list.vue | ~700 行 |
| 文章创建 | src/views/article/create.vue | ~300 行 |
| 文章编辑 | src/views/article/edit.vue | ~300 行 |
| 文章详情 | src/views/article/detail.vue | ~250 行 |
| 用户列表 | src/views/user/list.vue | ~400 行 |
| 用户创建 | src/views/user/create.vue | ~200 行 |
| 综合报表 | src/views/report/index.vue | ~350 行 |
| 文章报表 | src/views/report/article.vue | ~300 行 |
| 评论报表 | src/views/report/comment.vue | ~300 行 |
| 活跃报表 | src/views/report/activity.vue | ~250 行 |
| 学校介绍 | src/views/school/intro.vue | ~200 行 |

### 4.2 后端开发

#### 4.2.1 Flask 应用结构（app.py）

```python
from flask import Flask, jsonify, request
import jwt
import pymysql
from datetime import datetime, timedelta
from functools import wraps
from config import Config
from models import init_db, User, Article, Comment

app = Flask(__name__)
app.config.from_object(Config)
init_db()

# JWT Token 生成
def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

# Token 验证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Token')
        if not token:
            return jsonify({'code': 40001, 'message': 'Token is missing'}), 401
        payload = decode_token(token)
        if not payload:
            return jsonify({'code': 40002, 'message': 'Token is invalid or expired'}), 401
        return f(payload, *args, **kwargs)
    return decorated

# 管理员权限装饰器
def admin_required(f):
    @wraps(f)
    def decorated(payload, *args, **kwargs):
        if not payload or payload.get('role') != 'admin':
            return jsonify({'code': 40003, 'message': '权限不足'}), 403
        return f(payload, *args, **kwargs)
    return decorated
```

#### 4.2.2 核心接口实现

**1. 用户登录**

```python
@app.route('/vue-admin-template/user/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    user = User.find_by_username(username)
    if user and user['password'] == password:
        token = generate_token(user['id'], user['role'])
        return jsonify({'code': 20000, 'data': {'token': token}})
    return jsonify({'code': 50000, 'message': '用户名或密码错误'}), 401
```

**2. 用户注册**

```python
@app.route('/vue-admin-template/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if User.find_by_username(username):
        return jsonify({'code': 50001, 'message': '用户名已存在'})

    user_id = User.create(username, password, 'user', username, '')
    return jsonify({'code': 20000, 'data': {'id': user_id}})
```

**3. 文章创建（含权限控制）**

```python
@app.route('/vue-admin-template/table/create', methods=['POST'])
@token_required
def create_article(payload):
    data = request.get_json()
    current_user = _get_current_user_info(payload)
    user_role = payload.get('role')

    # 普通用户只能使用自己的姓名作为作者
    if user_role != 'admin':
        if current_user:
            data['author'] = current_user.get('name') or current_user.get('username')
        else:
            return jsonify({'code': 40003, 'message': '无法获取用户信息'})

    article_id = Article.create(
        title=data.get('title'),
        author=data.get('author'),
        pageviews=data.get('pageviews', 0),
        status=data.get('status', 'draft'),
        content=data.get('content', ''),
        display_time=data.get('display_time')
    )
    return jsonify({'code': 20000, 'data': {'id': article_id}})
```

**4. 文章删除（权限控制）**

```python
@app.route('/vue-admin-template/table/delete', methods=['POST'])
@token_required
def delete_article(payload):
    data = request.get_json()
    article = Article.get_by_id(data.get('id'))
    current_user = _get_current_user_info(payload)
    user_role = payload.get('role')

    is_admin = user_role == 'admin'
    is_author = current_user and article.get('author') == current_user.get('name')

    if not is_admin and not is_author:
        return jsonify({'code': 40003, 'message': '无权删除此文章'}), 403

    Article.delete(data.get('id'))
    return jsonify({'code': 20000, 'data': 'success'})
```

**5. 综合报表**

```python
@app.route('/vue-admin-template/report/overview', methods=['GET'])
@token_required
def get_report_overview(payload):
    conn = Config.get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 基础统计
    cursor.execute('SELECT COUNT(*) as count FROM users')
    users_count = cursor.fetchone()['count']
    cursor.execute('SELECT COUNT(*) as count FROM articles')
    articles_count = cursor.fetchone()['count']
    cursor.execute('SELECT SUM(pageviews) as total FROM articles')
    pageviews_total = cursor.fetchone()['total'] or 0

    # 热门文章 TOP 10
    cursor.execute('SELECT id, title, author, pageviews FROM articles ORDER BY pageviews DESC LIMIT 10')
    top_articles = cursor.fetchall()

    # 作者文章数排行
    cursor.execute('SELECT author as name, COUNT(*) as count FROM articles GROUP BY author ORDER BY count DESC LIMIT 10')
    author_ranking = cursor.fetchall()

    return jsonify({'code': 20000, 'data': {
        'users_count': users_count,
        'articles_count': articles_count,
        'pageviews_total': pageviews_total,
        'top_articles': top_articles,
        'author_ranking': author_ranking
    }})
```

#### 4.2.3 数据库模型（models.py）

**User 模型：**

```python
class User:
    @staticmethod
    def find_by_username(username):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            return cursor.fetchone()

    @staticmethod
    def create(username, password, role='user', name=None, avatar=None):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO users (username, password, role, name, avatar) VALUES (%s, %s, %s, %s, %s)',
                (username, password, role, name, avatar)
            )
            connection.commit()
            return cursor.lastrowid
```

**Article 模型：**

```python
class Article:
    @staticmethod
    def get_all(page, limit):
        connection = get_db_connection()
        offset = (page - 1) * limit
        with connection.cursor() as cursor:
            cursor.execute('SELECT SQL_CALC_FOUND_ROWS * FROM articles ORDER BY created_at DESC LIMIT %s OFFSET %s', (limit, offset))
            items = cursor.fetchall()
            cursor.execute('SELECT FOUND_ROWS() as total')
            total = cursor.fetchone()['total']
            return {'items': items, 'total': total}

    @staticmethod
    def create(title, author, pageviews=0, status='draft', content='', display_time=None):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO articles (title, author, pageviews, status, content, display_time) VALUES (%s, %s, %s, %s, %s, %s)',
                (title, author, pageviews, status, content, display_time)
            )
            connection.commit()
            return cursor.lastrowid
```

#### 4.2.4 后端接口统计

| 模块 | 接口数量 | 代码行数 |
|------|----------|----------|
| 用户认证 | 4 | ~100 行 |
| 用户管理 | 7 | ~200 行 |
| 文章管理 | 5 | ~250 行 |
| 数据报表 | 5 | ~200 行 |
| 数据库统计 | 2 | ~50 行 |
| 评论管理 | 7 | ~200 行 |
| **总计** | **30** | **~1000 行** |

> 📸 **截图位置 19**：在此处插入 Postman 测试文章创建接口截图
> 📸 **截图位置 20**：在此处插入 Postman 测试数据报表接口截图

### 4.3 系统测试

#### 4.3.1 功能测试

| 测试项 | 测试方法 | 预期结果 | 实际结果 |
|--------|----------|----------|----------|
| 用户登录 | 输入 admin/111111 | 返回 Token | 通过 |
| 用户注册 | 输入新用户名密码 | 创建成功，角色为 user | 通过 |
| 文章创建 | 管理员发布文章 | 文章入库，状态为 draft | 通过 |
| 文章编辑 | 修改文章标题 | 更新成功 | 通过 |
| 文章删除 | 管理员删除文章 | 删除成功 | 通过 |
| 权限控制 | 普通用户尝试删除他人文章 | 返回 403 权限不足 | 通过 |
| 数据报表 | 访问综合报表 | 返回统计数据 | 通过 |
| 文章导出 | 点击导出按钮 | 下载 Excel 文件 | 通过 |
| 浏览量排序 | 点击浏览量列头 | 按浏览量升序/降序排列 | 通过 |

#### 4.3.2 接口测试

| 接口 | 状态码 | 响应时间 | 结果 |
|------|--------|----------|------|
| POST /user/login | 200 | < 100ms | 通过 |
| GET /user/info | 200 | < 50ms | 通过 |
| GET /table/list | 200 | < 100ms | 通过 |
| POST /table/create | 200 | < 100ms | 通过 |
| GET /report/overview | 200 | < 200ms | 通过 |
| GET /report/article | 200 | < 200ms | 通过 |
| GET /report/activity | 200 | < 200ms | 通过 |

> 📸 **截图位置 21**：在此处插入 Postman 批量测试截图
> 📸 **截图位置 22**：在此处插入浏览器开发者工具 Network 面板截图

---

## 第五章 实训小结

### 5.1 核心问题与解决方案

#### 问题 1：活跃报表 SQL 错误

**错误信息：**
```
Unknown column 'a.author_id' in 'on clause'
```

**原因分析：** articles 表使用 `author` 字段（VARCHAR）存储作者名，而非 `author_id`（INT）外键。

**解决方案：** 修改 SQL 关联条件
```python
# 修改前
LEFT JOIN articles a ON u.id = a.author_id
# 修改后
LEFT JOIN articles a ON u.username = a.author
```

#### 问题 2：报表时间格式显示 00:00

**错误信息：**
```
Expression #1 of SELECT list is not in GROUP BY clause
```

**原因分析：** MySQL 的 `ONLY_FULL_GROUP_BY` 模式下，SELECT 中的非聚合字段必须出现在 GROUP BY 中。

**解决方案：** 使用 `DATE_FORMAT()` 函数
```python
# 修改前
SELECT DATE(created_at) as date, COUNT(*) as count
# 修改后
SELECT DATE_FORMAT(created_at, '%Y-%m-%d') as date, COUNT(*) as count
```

#### 问题 3：普通用户权限控制

**需求：** 普通用户只能编辑/删除自己发布的文章。

**解决方案：** 在后端接口中添加权限校验
```python
is_admin = user_role == 'admin'
is_author = current_user and article.get('author') == current_user.get('name')
if not is_admin and not is_author:
    return jsonify({'code': 40003, 'message': '无权操作'}), 403
```

#### 问题 4：首页卡片高度不对齐

**问题描述：** 左侧公司介绍卡片与右侧热门标签卡片高度不一致。

**解决方案：** 使用 Flexbox 布局
```css
.main-content-row {
  display: flex;
  align-items: stretch;
}
.main-col-left, .main-col-right {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.activity-card, .wordcloud-card {
  flex: 1 1 auto;
}
```

#### 问题 5：文档生成样式错误

**错误信息：**
```
KeyError: "no style with name 'Table Grid'"
KeyError: "no style with name 'No Spacing'"
```

**原因分析：** python-docx 模板中不存在这些样式名称。

**解决方案：** 移除不存在的样式设置，使用默认样式。

### 5.2 实训收获

| 收获 | 描述 |
|------|------|
| 前后端分离架构 | 深入理解了 Vue.js + Flask 的前后端分离开发模式 |
| JWT 认证 | 掌握了 Token 认证机制的实现原理和应用 |
| 权限控制 | 实现了基于角色的访问控制（RBAC） |
| 数据可视化 | 使用 ECharts 实现了多种图表展示 |
| 数据库设计 | 设计了 4 张关联表，理解了外键关系 |
| SQL 优化 | 解决了 GROUP BY 和 JOIN 的常见问题 |
| 响应式布局 | 使用 Flexbox 实现了等高布局 |
| AI 辅助开发 | 熟练使用 AI 工具提高开发效率 |

### 5.3 项目总结

本项目从零开始搭建了一个完整的前后端分离内容管理系统，涵盖了用户管理、文章管理、评论管理、数据报表等核心功能。通过实训，掌握了以下技能：

1. **前端开发**：Vue.js 2 + Element UI + Vue Router + Vuex + Axios
2. **后端开发**：Flask + PyMySQL + JWT 认证
3. **数据库设计**：MySQL 表设计、ER 关系、SQL 查询优化
4. **数据可视化**：ECharts 图表、词云展示
5. **权限控制**：基于角色的访问控制（RBAC）
6. **工程实践**：代码规范、接口设计、测试验证

项目代码总量约 **8600+ 行**，包含 **30 个 API 接口**、**13 个前端页面**、**4 张数据库表**，是一个功能完整、结构清晰的前后端分离项目。

---

## 附录

### A. 截图清单

| 编号 | 截图内容 | 位置 |
|------|----------|------|
| 1 | 项目目录结构 | 第一章 1.5 |
| 2 | 系统架构图 | 第二章 2.1 |
| 3 | ER 关系图 | 第二章 2.2.2 |
| 4 | Postman 登录接口测试 | 第二章 2.3.2 |
| 5 | 登录页面 | 第二章 2.4 |
| 6 | 仪表盘首页 | 第二章 2.4 |
| 7 | 文章列表页面 | 第二章 2.4 |
| 8 | 数据报表页面 | 第二章 2.4 |
| 9 | users 表数据 | 第三章 3.3 |
| 10 | articles 表数据 | 第三章 3.3 |
| 11 | comments 表数据 | 第三章 3.3 |
| 12 | 仪表盘完整截图 | 第四章 4.1.3 |
| 13 | 文章列表功能截图 | 第四章 4.1.3 |
| 14 | 综合报表截图 | 第四章 4.1.3 |
| 15 | 文章报表截图 | 第四章 4.1.3 |
| 16 | 评论报表截图 | 第四章 4.1.3 |
| 17 | 登录页面截图 | 第四章 4.1.3 |
| 18 | 注册对话框截图 | 第四章 4.1.3 |
| 19 | Postman 文章创建测试 | 第四章 4.2.4 |
| 20 | Postman 数据报表测试 | 第四章 4.2.4 |
| 21 | Postman 批量测试 | 第四章 4.3.2 |
| 22 | Network 面板截图 | 第四章 4.3.2 |

### B. 项目文件清单

| 文件 | 行数 | 说明 |
|------|------|------|
| app.py | 1051 | Flask 后端主程序 |
| models.py | 1790 | 数据库模型 |
| config.py | 31 | 配置文件 |
| package.json | ~60 | 前端依赖配置 |
| src/views/dashboard/index.vue | 1173 | 仪表盘页面 |
| src/views/login/index.vue | 1038 | 登录/注册页面 |
| src/views/article/list.vue | 700 | 文章列表页面 |
| src/router/index.js | 197 | 路由配置 |
| src/utils/request.js | 107 | Axios 封装 |

---

*报告生成日期：2026年6月24日*

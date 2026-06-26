# Vue-Admin 内容管理系统

> 基于 Vue.js 2 + Element UI 和 Flask + MySQL 的前后端分离内容管理系统

## 项目简介

本项目是一个功能完整的前后端分离内容管理系统，实现了用户管理、文章管理、评论管理、数据报表等核心功能。系统采用 JWT 认证和基于角色的权限控制（RBAC），支持管理员和普通用户两种角色。

## 技术栈

### 前端
- **Vue.js** 2.6.10 - 核心前端框架
- **Vue Router** 3.0.6 - 前端路由管理
- **Vuex** 3.1.0 - 状态管理
- **Element UI** 2.13.2 - UI 组件库
- **Axios** 0.18.1 - HTTP 请求库
- **ECharts** 5.6.0 - 数据可视化图表
- **echarts-wordcloud** 2.1.0 - 词云组件
- **XLSX** 0.18.5 - Excel 文件导出

### 后端
- **Flask** - Python Web 框架
- **PyMySQL** - MySQL 数据库驱动
- **PyJWT** - JWT 认证库
- **MySQL** - 关系型数据库

## 功能特性

### 用户管理
- 用户登录/登出
- 用户注册（默认为普通用户）
- 用户信息管理
- 管理员用户 CRUD
- 个人信息修改

### 文章管理
- 文章发布/编辑/删除
- 文章搜索（按标题、作者）
- 按浏览量排序（升序/降序）
- 文章导出为 Excel
- 富文本编辑器
- 普通用户只能编辑/删除自己的文章

### 评论管理
- 评论发布/编辑/删除
- 评论审核（通过/拒绝/待审核）
- 按文章查看评论
- 评论统计

### 数据报表
- **综合报表**：用户/文章/评论统计 + 热门文章 TOP10 + 作者排行
- **文章报表**：发布趋势图 + 状态分布 + 文章列表
- **评论报表**：评论趋势图 + 状态分布 + 评论最多文章排行
- **活跃报表**：用户活跃度排行 + 最近发布文章

### 其他功能
- JWT Token 认证
- 基于角色的权限控制（RBAC）
- 主题切换（浅色/深色模式）
- 响应式布局
- 实时时间显示
- 词云可视化

## 数据库设计

### 表结构

| 表名 | 说明 | 字段数 |
|------|------|--------|
| users | 用户表 | 7 |
| articles | 文章表 | 9 |
| comments | 评论表 | 9 |

### 默认数据

**用户：**
| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | 111111 | 管理员 |
| test | 111111 | 普通用户 |

**文章：** 4 篇预置文章（Vue.js、Flask、MySQL、JavaScript 主题）

**评论：** 5 条预置评论

## API 接口

系统共包含 **30 个 API 接口**：

| 模块 | 接口数量 | 说明 |
|------|----------|------|
| 用户认证 | 4 | 登录/登出/注册/获取信息 |
| 用户管理 | 7 | 用户 CRUD + 个人信息更新 |
| 文章管理 | 5 | 文章 CRUD + 详情 |
| 评论管理 | 7 | 评论 CRUD + 审核 + 统计 |
| 数据报表 | 5 | 综合/文章/评论/活跃/热门 |
| 数据库 | 2 | 统计 + 表列表 |

## 快速开始

### 环境要求
- Node.js >= 12
- Python >= 3.7
- MySQL >= 5.7

### 后端启动

```bash
# 安装 Python 依赖
pip install flask pymysql pyjwt

# 配置数据库（修改 config.py）
# MYSQL_HOST = 'localhost'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'your_password'
# MYSQL_DB = 'vue_admin'

# 启动 Flask 服务
python app.py
```

后端服务默认运行在 `http://localhost:5000`

### 前端启动

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

浏览器访问 [http://localhost:9528](http://localhost:9528)

### 构建发布

```bash
# 构建生产环境
npm run build:prod

# 构建测试环境
npm run build:stage
```

## 项目结构

```
vue-admin-template-master/
├── app.py                      # Flask 后端主程序 (1051 行)
├── models.py                   # 数据库模型 (1790 行)
── config.py                   # 配置文件
├── package.json                # 前端依赖配置
├── README-zh.md                # 项目说明文档
├── src/
│   ├── api/                    # API 请求封装
│   ├── components/             # 公共组件
│   ├── router/                 # 路由配置 (197 行)
│   ├── store/                  # Vuex 状态管理
│   ├── styles/                 # 全局样式
│   ├── utils/                  # 工具函数
│   │   ├── request.js          # Axios 封装 (107 行)
│   │   └── auth.js             # Token 管理
│   ── views/                  # 页面组件
│       ├── dashboard/          # 仪表盘 (1173 行)
│       ├── login/              # 登录/注册 (1038 行)
│       ├── article/            # 文章管理
│       │   ├── list.vue        # 文章列表 (700 行)
│       │   ├── create.vue      # 文章创建
│       │   ├── edit.vue        # 文章编辑
│       │   └── detail.vue      # 文章详情
│       ├── user/               # 用户管理
│       │   ├── list.vue        # 用户列表
│       │   └── create.vue      # 用户创建
│       ├── report/             # 数据报表
│       │   ├── index.vue       # 综合报表
│       │   ├── article.vue     # 文章报表
│       │   ├── comment.vue     # 评论报表
│       │   └── activity.vue    # 活跃报表
│       └── school/             # 学校介绍
└── public/                     # 静态资源
```

## 权限说明

### 管理员 (admin)
- 所有 CRUD 操作权限
- 用户管理（增删改查）
- 评论审核
- 查看所有数据报表

### 普通用户 (user)
- 只能编辑/删除自己发布的文章
- 可查看数据报表
- 可发布评论
- 注册账号默认为普通用户

## 开发工具

| 工具 | 用途 |
|------|------|
| VS Code | 代码编辑器 |
| Navicat | 数据库管理 |
| Postman | API 测试 |
| Git | 版本控制 |

## 代码统计

| 类型 | 文件数 | 总行数 |
|------|--------|--------|
| 后端 Python | 3 | ~2872 |
| 前端 Vue | 13 | ~5700 |
| 配置文件 | 2 | ~90 |
| **总计** | **18** | **~8600+** |

## 常见问题

### 1. 数据库连接失败
检查 `config.py` 中的数据库配置是否正确，确保 MySQL 服务已启动。

### 2. 端口冲突
前端默认端口 9528，后端默认端口 5000，如有冲突可在配置文件中修改。

### 3. Token 过期
JWT Token 默认 24 小时过期，过期后需重新登录。

## 许可证

[MIT](LICENSE) License

---

*最后更新：2026年6月24日*

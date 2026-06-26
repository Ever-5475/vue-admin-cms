# Vue-Admin Content Management System

> A full-stack content management system based on Vue.js 2 + Element UI and Flask + MySQL

[中文文档](README-zh.md)

## Features

- **User Management**: Login/Register, JWT authentication, RBAC
- **Article Management**: CRUD, search, sort by views, export to Excel
- **Comment Management**: CRUD, moderation, statistics
- **Data Reports**: Dashboard, article trends, comment analysis, activity reports
- **Theme Switching**: Light/Dark mode
- **Responsive Design**: Works on desktop and mobile

## Tech Stack

### Frontend
- Vue.js 2.6.10
- Vue Router 3.0.6
- Vuex 3.1.0
- Element UI 2.13.2
- Axios 0.18.1
- ECharts 5.6.0

### Backend
- Flask
- PyMySQL
- PyJWT
- MySQL

## Quick Start

### Backend

```bash
pip install flask pymysql pyjwt
python app.py
```

### Frontend

```bash
npm install
npm run dev
```

Visit http://localhost:9528

## Default Accounts

| Username | Password | Role |
|----------|----------|------|
| admin | 111111 | Admin |
| test | 111111 | User |

## License

[MIT](LICENSE)

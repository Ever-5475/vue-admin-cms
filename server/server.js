require('dotenv').config()
const express = require('express')
const cors = require('cors')
const mysql = require('mysql2/promise')
const bcrypt = require('bcryptjs')
const jwt = require('jsonwebtoken')

const app = express()
const port = 3000

// 中间件
app.use(cors())
app.use(express.json())

// 先创建不带数据库名的连接，用于创建数据库
const createPool = mysql.createPool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
})

// 全局连接池（稍后初始化）
let pool = null

// 初始化数据库
async function initDB() {
  try {
    // 第一步：连接到MySQL服务器（不指定数据库）
    const tempConnection = await createPool.getConnection()

    // 创建数据库（如果不存在）
    await tempConnection.execute(`CREATE DATABASE IF NOT EXISTS ${process.env.DB_NAME}`)
    console.log(`数据库 ${process.env.DB_NAME} 创建成功或已存在`)

    tempConnection.release()

    // 第二步：创建带数据库名的连接池
    pool = mysql.createPool({
      host: process.env.DB_HOST,
      port: process.env.DB_PORT,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_NAME,
      waitForConnections: true,
      connectionLimit: 10,
      queueLimit: 0
    })

    // 第三步：创建用户表
    const connection = await pool.getConnection()
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        nickname VARCHAR(50),
        avatar VARCHAR(255),
        role VARCHAR(20) DEFAULT 'admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
      )
    `)
    console.log('users表创建成功或已存在')

    // 第四步：检查是否有默认管理员账户
    const [rows] = await connection.execute('SELECT * FROM users WHERE username = ?', ['admin'])
    if (rows.length === 0) {
      const hashedPassword = await bcrypt.hash('123456', 10)
      await connection.execute(
        'INSERT INTO users (username, password, nickname, role) VALUES (?, ?, ?, ?)',
        ['admin', hashedPassword, '管理员', 'admin']
      )
      console.log('默认管理员账户已创建: admin / 123456')
    } else {
      console.log('管理员账户已存在')
    }
    connection.release()

    console.log('数据库初始化完成')
  } catch (err) {
    console.error('数据库初始化失败:', err)
  }
}

// 登录接口
app.post('/vue-admin-template/user/login', async (req, res) => {
  try {
    const { username, password } = req.body

    const [rows] = await pool.execute('SELECT * FROM users WHERE username = ?', [username])
    if (rows.length === 0) {
      return res.status(200).json({ code: 50000, message: '用户名或密码错误' })
    }

    const user = rows[0]
    const isPasswordValid = await bcrypt.compare(password, user.password)

    if (!isPasswordValid) {
      return res.status(200).json({ code: 50000, message: '用户名或密码错误' })
    }

    // 生成JWT token
    const token = jwt.sign(
      { id: user.id, username: user.username },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRE }
    )

    res.status(200).json({
      code: 20000,
      data: {
        token: token
      }
    })
  } catch (err) {
    console.error('登录失败:', err)
    res.status(200).json({ code: 50000, message: '服务器内部错误' })
  }
})

// 获取用户信息接口
app.get('/vue-admin-template/user/info', async (req, res) => {
  try {
    const token = req.headers['x-token']

    if (!token) {
      return res.status(200).json({ code: 50008, message: 'Token无效' })
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    const [rows] = await pool.execute('SELECT username, nickname, role FROM users WHERE id = ?', [decoded.id])

    if (rows.length === 0) {
      return res.status(200).json({ code: 50008, message: '用户不存在' })
    }

    const user = rows[0]
    res.status(200).json({
      code: 20000,
      data: {
        roles: [user.role],
        name: user.nickname || user.username,
        avatar: user.avatar || ''
      }
    })
  } catch (err) {
    console.error('获取用户信息失败:', err)
    res.status(200).json({ code: 50008, message: 'Token过期' })
  }
})

// 退出登录接口
app.post('/vue-admin-template/user/logout', (req, res) => {
  res.status(200).json({
    code: 20000,
    message: '退出成功'
  })
})

// 启动服务器
initDB().then(() => {
  app.listen(port, () => {
    console.log(`后端服务运行在 http://localhost:${port}`)
  })
})

<template>
  <div class="login-container">
    <!-- 左上角Logo -->
    <div class="top-left-logo">
      <img src="https://chengyi.jmu.edu.cn/images/logo2022.png" alt="Logo" />
    </div>

    <!-- 标题文字 - 位于logo正下方，页面左侧中间 -->
    <div class="center-title">
      <h3 class="main-title">
        <i class="el-icon-s-platform"></i>
        诚毅公司管理系统
      </h3>
      <p class="main-subtitle">Vue Admin Template</p>
    </div>

    <!-- 视频动态壁纸背景 -->
    <video
      ref="videoBg"
      class="video-background"
      :src="currentVideo"
      autoplay
      loop
      muted
      playsinline
      preload="auto"
      crossorigin="anonymous"
    ></video>
    <div class="video-overlay"></div>

    <!-- 玻璃效果登录框 -->
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form glass-card" auto-complete="on" label-position="left" v-show="!isRegisterMode">

      <div class="title-container">
        <img src="https://chengyi.jmu.edu.cn/images/logo2022.png" alt="Logo" class="logo-image" />
      </div>

      <el-form-item prop="username" :error="serverError.username">
        <span class="svg-container svg-container-username">
          <i class="el-icon-user"></i>
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="请输入用户名"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
          @input="clearServerError('username')"
        />
      </el-form-item>

      <el-form-item prop="password" :error="serverError.password">
        <span class="svg-container svg-container-password">
          <i class="el-icon-lock"></i>
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="请输入密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
          @input="clearServerError('password')"
        />
        <span class="show-pwd" @click="showPwd">
          <i :class="passwordType === 'password' ? 'el-icon-view' : 'el-icon-hide'"></i>
        </span>
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        class="login-button"
        @click.native.prevent="handleLogin"
      >
        {{ loading ? '登录中...' : '登 录' }}
      </el-button>

      <div class="register-link">
        <span>没有账号？</span>
        <el-button type="text" class="register-btn" @click="switchToRegister">去注册</el-button>
      </div>
    </el-form>

    <!-- 玻璃效果注册框 -->
    <el-form ref="registerForm" :model="registerForm" :rules="registerRules" class="login-form glass-card" auto-complete="on" label-position="left" v-show="isRegisterMode">

      <div class="title-container">
        <h3 class="title">
          <i class="el-icon-user-solid"></i>
          用户注册
        </h3>
        <p class="subtitle">创建你的账号</p>
      </div>

      <el-form-item prop="username" :error="registerServerError.username">
        <span class="svg-container svg-container-username">
          <i class="el-icon-user"></i>
        </span>
        <el-input
          ref="regUsername"
          v-model="registerForm.username"
          placeholder="请输入用户名"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
          @keyup.enter.native="handleRegister"
          @input="clearRegisterServerError('username')"
        />
      </el-form-item>

      <el-form-item prop="name">
        <span class="svg-container svg-container-name">
          <i class="el-icon-s-custom"></i>
        </span>
        <el-input
          v-model="registerForm.name"
          placeholder="请输入姓名"
          name="name"
          type="text"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleRegister"
        />
      </el-form-item>

      <el-form-item prop="password" :error="registerServerError.password">
        <span class="svg-container svg-container-password">
          <i class="el-icon-lock"></i>
        </span>
        <el-input
          :key="registerPasswordType"
          ref="regPassword"
          v-model="registerForm.password"
          :type="registerPasswordType"
          placeholder="请输入密码"
          name="password"
          tabindex="3"
          auto-complete="on"
          @keyup.enter.native="handleRegister"
          @input="clearRegisterServerError('password')"
        />
        <span class="show-pwd" @click="showRegisterPwd">
          <i :class="registerPasswordType === 'password' ? 'el-icon-view' : 'el-icon-hide'"></i>
        </span>
      </el-form-item>

      <el-form-item prop="confirmPassword" :error="registerServerError.confirmPassword">
        <span class="svg-container svg-container-password">
          <i class="el-icon-lock"></i>
        </span>
        <el-input
          ref="regConfirmPassword"
          v-model="registerForm.confirmPassword"
          :type="registerPasswordType"
          placeholder="请确认密码"
          name="confirmPassword"
          tabindex="4"
          auto-complete="on"
          @keyup.enter.native="handleRegister"
          @input="clearRegisterServerError('confirmPassword')"
        />
        <span class="show-pwd" @click="showRegisterPwd">
          <i :class="registerPasswordType === 'password' ? 'el-icon-view' : 'el-icon-hide'"></i>
        </span>
      </el-form-item>

      <el-button
        :loading="registerLoading"
        type="primary"
        class="login-button"
        @click.native.prevent="handleRegister"
      >
        {{ registerLoading ? '注册中...' : '注 册' }}
      </el-button>

      <div class="register-link">
        <span>已有账号？</span>
        <el-button type="text" class="register-btn" @click="switchToLogin">去登录</el-button>
      </div>
    </el-form>

    <!-- 版权信息 -->
    <div class="copyright-footer">
      <p>Copyright © 2026-2026 集美大学诚毅学院</p>
    </div>
  </div>
</template>

<script>
import { validUsername } from '@/utils/validate'

export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('请输入正确的用户名'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能少于6位'))
      } else {
        callback()
      }
    }
    // 视频列表 - 循环播放
    const videoList = [
      require('./1.mp4'),
      require('./2.mp4'),
      require('./3.mp4'),
      require('./4.mp4')
    ]
    // 从 localStorage 读取当前视频索引（刷新页面时保持不变）
    const savedIndex = Number(localStorage.getItem('login_video_index'))
    const currentIndex = (isNaN(savedIndex) || savedIndex < 0 || savedIndex >= videoList.length) ? 0 : savedIndex
    return {
      videoList,
      currentIndex,
      isRegisterMode: false, // 是否为注册模式
      loginForm: {
        username: 'admin',
        password: '111111'
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      serverError: { username: '', password: '' },
      // 注册相关
      registerForm: {
        username: '',
        name: '',
        password: '',
        confirmPassword: ''
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 20, message: '用户名长度为2-20个字符', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9_\u4e00-\u9fa5]+$/, message: '用户名只能包含字母、数字、下划线和中文', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码不能少于6位', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value !== this.registerForm.password) {
                callback(new Error('两次输入的密码不一致'))
              } else {
                callback()
              }
            },
            trigger: 'blur'
          }
        ]
      },
      registerLoading: false,
      registerPasswordType: 'password',
      registerServerError: { username: '', password: '', confirmPassword: '' }
    }
  },
  computed: {
    currentVideo() {
      return this.videoList[this.currentIndex]
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    _setupRefraction() {
      // 物理动态折射：采样视频四周8个点位的像素颜色，写入 CSS 变量
      // 边框色彩会随视频内容实时变化
      const video = this.$refs.videoBg
      if (!video) return

      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      const SAMPLE_W = 32
      const SAMPLE_H = 24
      canvas.width = SAMPLE_W
      canvas.height = SAMPLE_H

      // 将像素值增强后转为 CSS rgb 字符串（增强折射效果的色彩感知）
      const toRgb = (arr) => {
        const r = Math.min(255, Math.floor(arr[0] * 1.35 + 20))
        const g = Math.min(255, Math.floor(arr[1] * 1.35 + 20))
        const b = Math.min(255, Math.floor(arr[2] * 1.35 + 20))
        return `rgb(${r}, ${g}, ${b})`
      }

      // 8 个采样点：顺时针从左上角开始
      const points = [
        { x: 2, y: 2 },
        { x: SAMPLE_W / 2, y: 2 },
        { x: SAMPLE_W - 2, y: 2 },
        { x: SAMPLE_W - 2, y: SAMPLE_H / 2 },
        { x: SAMPLE_W - 2, y: SAMPLE_H - 2 },
        { x: SAMPLE_W / 2, y: SAMPLE_H - 2 },
        { x: 2, y: SAMPLE_H - 2 },
        { x: 2, y: SAMPLE_H / 2 }
      ]

      const root = document.documentElement
      const sample = () => {
        if (!video.videoWidth || video.paused) return
        try {
          ctx.drawImage(video, 0, 0, SAMPLE_W, SAMPLE_H)
          points.forEach((p, i) => {
            const data = ctx.getImageData(p.x, p.y, 1, 1).data
            root.style.setProperty(`--edge-color-${i}`, toRgb(data))
          })
        } catch (e) {
          // 跨域或视频未就绪时静默
        }
      }

      sample()
      video.addEventListener('playing', sample, { once: true })
      this._refractionTimer = setInterval(sample, 120)
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      // 提交前先清空上一次的服务端错误
      this.clearServerError('username')
      this.clearServerError('password')

      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(() => {
            // 登录成功：标记用户已进入过系统，退出登录时需要切换视频
            localStorage.setItem('login_video_should_rotate', '1')
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(error => {
            this.loading = false

            // ===== 服务端错误：转成表单项内联提示（与本地校验一致）=====
            let msg = ''
            if (error && typeof error === 'object') {
              msg = error.userMessage || error.message || ''
            } else if (typeof error === 'string') {
              msg = error
            }

            // 根据后端返回的中文 message 判断是账号还是密码问题
            const str = (msg || '').toString()
            // 含有 "用户" / "账号" / "不存在" / "未找到" / "不正确" → 归到用户名
            // 含有 "密码" → 归到密码
            if (/密码/.test(str)) {
              this.serverError.password = str || '请输入正确的密码'
            } else if (/用户|账号|不存在|未找到|不正确|用户名/.test(str) || /401/.test(str)) {
              this.serverError.username = str || '用户名或密码不正确'
            } else {
              // 其他情况：两个字段都提示
              this.serverError.username = str || '登录失败，请检查后重试'
            }
          })
        } else {
          return false
        }
      })
    },
    clearServerError(field) {
      if (field) {
        this.serverError[field] = ''
      } else {
        this.serverError = { username: '', password: '' }
      }
    },
    switchToRegister() {
      this.isRegisterMode = true
      this.registerForm = { username: '', name: '', password: '', confirmPassword: '' }
      this.registerServerError = { username: '', password: '', confirmPassword: '' }
      this.$nextTick(() => {
        this.$refs.registerForm && this.$refs.registerForm.clearValidate()
      })
    },
    switchToLogin() {
      this.isRegisterMode = false
      this.serverError = { username: '', password: '' }
      this.$nextTick(() => {
        this.$refs.loginForm && this.$refs.loginForm.clearValidate()
      })
    },
    showRegisterPwd() {
      this.registerPasswordType = this.registerPasswordType === 'password' ? '' : 'password'
    },
    clearRegisterServerError(field) {
      this.registerServerError[field] = ''
    },
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (!valid) return
        this.registerLoading = true
        this.$store.dispatch('user/register', this.registerForm).then(() => {
          this.$message.success('注册成功，请登录')
          this.registerLoading = false
          this.switchToLogin()
          this.loginForm.username = this.registerForm.username
        }).catch(error => {
          this.registerLoading = false
          let msg = ''
          if (error && typeof error === 'object') {
            msg = error.userMessage || error.message || ''
          } else if (typeof error === 'string') {
            msg = error
          }
          const str = (msg || '').toString()
          if (/用户名|账号|已存在|重复/.test(str)) {
            this.registerServerError.username = str || '用户名已存在'
          } else if (/姓名|名字|已存在|重复/.test(str)) {
            this.registerServerError.username = str || '姓名已存在'
          } else if (/密码/.test(str)) {
            this.registerServerError.password = str || '密码格式不正确'
          } else {
            this.registerServerError.username = str || '注册失败，请重试'
          }
        })
      })
    }
  },
  created() {
    // 只有当用户已登录过（标记存在）时，才切换到下一个视频
    // 这样：刷新页面 -> 不切换；登录 -> 退出 -> 再次进入登录页 -> 切换到下一个视频
    const shouldRotate = localStorage.getItem('login_video_should_rotate')
    if (shouldRotate === '1') {
      this.currentIndex = (this.currentIndex + 1) % this.videoList.length
      localStorage.setItem('login_video_index', String(this.currentIndex))
      // 重置标记，直到下一次登录成功后才允许再次切换
      localStorage.setItem('login_video_should_rotate', '0')
    }
  },
  mounted() {
    // 启动物理动态折射：采样视频四周颜色
    this.$nextTick(() => {
      this._setupRefraction()
    })
  },
  beforeDestroy() {
    if (this._refractionTimer) {
      clearInterval(this._refractionTimer)
    }
  }
}
</script>

<style lang="scss">
/* 全局输入框样式 */
$bg: #1a1a2e;
$light_gray: #fff;
$cursor: #fff;
$primary_color: #409eff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
    &:-webkit-autofill {
      box-shadow: 0 0 0px 1000px rgba(200, 200, 210, 0.95) inset !important;
      -webkit-text-fill-color: #333 !important;
      transition: background-color 5000s ease-in-out 0s;
    }
  }
}

.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: rgba(255, 255, 255, 0.95);
      border: 2px solid rgba(120, 120, 130, 0.35);
      -webkit-appearance: none;
      border-radius: 25px;
      padding: 12px 20px 12px 45px;
      color: #1a1a1a;
      height: 47px;
      caret-color: $primary_color;
      transition: all 0.3s ease;
      font-size: 16px;
      font-weight: 500;
      letter-spacing: 1px;
      text-shadow: none;
      line-height: 1.5;

      &::placeholder {
        color: #8a8a90;
        font-weight: 400;
        letter-spacing: 2px;
      }

      &:focus {
        background: rgba(255, 255, 255, 1);
        border-color: $primary_color;
        box-shadow: 0 0 0 3px rgba($primary_color, 0.2);
      }
    }
  }

  .el-form-item {
    border: none;
    background: transparent;
    border-radius: 5px;
    color: #454545;
    margin-bottom: 22px;
    // 固定高度，避免出现错误提示时布局跳动
    height: 72px;
    position: relative;
  }

  // 错误提示统一样式和位置：纯文字 + 微阴影，去掉反射/胶囊背景
  .el-form-item__error {
    font-size: 13px;
    color: #d9363e;
    font-weight: 700;
    letter-spacing: 2px;
    text-align: center;
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    white-space: nowrap;
    // 仅保留极轻阴影：在毛玻璃底色上保证可读性，但不做折射效果
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
    padding: 3px 0;
    line-height: 1;
  }

  .el-form-item__content {
    // 让内部输入框内容水平居中对齐
    display: flex;
    justify-content: center;
    align-items: center;
    line-height: 47px;
    position: relative;
  }
}
</style>

<style lang="scss" scoped>
// 颜色定义 - 水墨融合配色方案（相邻颜色自然过渡）
$color-coral: #FF6B6B;     // 珊瑚红
$color-amber: #FECA57;     // 琥珀黄
$color-emerald: #48DBFB;   // 翠绿/青绿
$color-blue: #54A0FF;      // 天蓝色
$color-violet: #9C88FF;    // 梦幻紫
$primary_color: #409eff;   // 主色调
$glass-bg: rgba(220, 220, 225, 0.85); // 浅灰色玻璃背景

.login-container {
  min-height: 100vh;
  width: 100%;
  background: #000;
  overflow: hidden;
  position: relative;

  // 视频动态壁纸背景
  .video-background {
    position: absolute;
    top: 50%;
    left: 50%;
    min-width: 100%;
    min-height: 100%;
    width: auto;
    height: auto;
    transform: translate(-50%, -50%);
    object-fit: cover;
    z-index: 0;
    pointer-events: none;
  }

  // 视频暗化叠加层 - 保证文字可读性
  .video-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.12);
    z-index: 1;
    pointer-events: none;
  }



  // 玻璃效果登录框（置于视频之上）- 移动到页面最右侧中间
  .login-form.glass-card {
    position: absolute;
    right: 190px;
    top: calc(50% - 23px);
    transform: translateY(-50%);
    z-index: 10;
    width: 450px;
    max-width: 95%;
    padding: 55px 45px;
    margin: 0;

    // 圆角玻璃 - 边缘靠物理折射与动态取色形成
    border-radius: 24px;
    border: none;
    // ── 稳定底色 + 四角柔和高光：透明度再下调约10%，更通透 ──
    background:
      rgba(255, 255, 255, 0.62),
      radial-gradient(circle at 18px 18px, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.04) 25%, rgba(255, 255, 255, 0) 60px),
      radial-gradient(circle at calc(100% - 18px) 18px, rgba(255, 255, 255, 0.16) 0%, rgba(255, 255, 255, 0.035) 25%, rgba(255, 255, 255, 0) 60px),
      radial-gradient(circle at 18px calc(100% - 18px), rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.025) 25%, rgba(255, 255, 255, 0) 65px),
      radial-gradient(circle at calc(100% - 18px) calc(100% - 18px), rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.02) 25%, rgba(255, 255, 255, 0) 65px);
    background-blend-mode: normal;
    // ── 关键：对背景视频做毛玻璃模糊 + 轻微提亮，隔绝背景干扰 ──
    // 这是让文字随背景变化仍保持清晰的核心机制
    backdrop-filter: blur(10px) saturate(160%) brightness(1.08);
    -webkit-backdrop-filter: blur(10px) saturate(160%) brightness(1.08);
    // 外缘阴影也同步轻一点
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.06),
      0 2px 8px rgba(0, 0, 0, 0.03),
      0 0 40px rgba(255, 255, 255, 0.14),
      inset 0 0 30px rgba(255, 255, 255, 0.06);

    // 入场动画
    animation: glassSlideIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);

    // ── 物理动态折射边缘：曲面棱镜，把背后视频画面曲折折射（细边款） ──
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      border-radius: 24px;
      pointer-events: none;
      z-index: 2;

      // ① 曲面棱镜折射：细腻模糊 + 适度饱和，避免过强
      backdrop-filter: blur(2.5px) saturate(190%) contrast(120%) brightness(1.1);
      -webkit-backdrop-filter: blur(2.5px) saturate(190%) contrast(120%) brightness(1.1);

      // ② 沿边缘的弧形高光 + 暗角（微调版）：角高光更柔和、边暗角更克制
      background:
        // 4 个角的弧形高光（光强下调，让曲面感更"薄"）
        radial-gradient(ellipse at 18px 18px, rgba(255, 255, 255, 0.35) 0%, rgba(255, 255, 255, 0.1) 25%, rgba(255, 255, 255, 0) 65px),
        radial-gradient(ellipse at calc(100% - 18px) 18px, rgba(255, 255, 255, 0.32) 0%, rgba(255, 255, 255, 0.08) 25%, rgba(255, 255, 255, 0) 65px),
        radial-gradient(ellipse at 18px calc(100% - 18px), rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0) 70px),
        radial-gradient(ellipse at calc(100% - 18px) calc(100% - 18px), rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0.04) 25%, rgba(255, 255, 255, 0) 70px),
        // 4 条边的暗角收窄：尺寸调小，暗度下调，曲面更精致
        radial-gradient(ellipse 90px 12px at 50% 0%, rgba(0, 0, 0, 0.05) 0%, rgba(0, 0, 0, 0.015) 40%, rgba(0, 0, 0, 0) 70%),
        radial-gradient(ellipse 90px 12px at 50% 100%, rgba(0, 0, 0, 0.06) 0%, rgba(0, 0, 0, 0.02) 40%, rgba(0, 0, 0, 0) 70%),
        radial-gradient(ellipse 12px 90px at 0% 50%, rgba(0, 0, 0, 0.04) 0%, rgba(0, 0, 0, 0.015) 40%, rgba(0, 0, 0, 0) 70%),
        radial-gradient(ellipse 12px 90px at 100% 50%, rgba(0, 0, 0, 0.04) 0%, rgba(0, 0, 0, 0.015) 40%, rgba(0, 0, 0, 0) 70%),
        // ③ 8 点采样色棱镜发光
        conic-gradient(
          from 45deg,
          var(--edge-color-0, rgba(255, 255, 255, 0.55)) 0deg,
          var(--edge-color-1, rgba(255, 255, 255, 0.4)) 45deg,
          var(--edge-color-2, rgba(255, 255, 255, 0.35)) 90deg,
          var(--edge-color-3, rgba(255, 255, 255, 0.3)) 135deg,
          var(--edge-color-4, rgba(255, 255, 255, 0.3)) 180deg,
          var(--edge-color-5, rgba(255, 255, 255, 0.35)) 225deg,
          var(--edge-color-6, rgba(255, 255, 255, 0.4)) 270deg,
          var(--edge-color-7, rgba(255, 255, 255, 0.55)) 315deg,
          var(--edge-color-0, rgba(255, 255, 255, 0.55)) 360deg
        );

      // mask 限制仅在边缘 1.5px（更细的边框）
      -webkit-mask:
        linear-gradient(#000, #000) content-box,
        linear-gradient(#000, #000);
      mask:
        linear-gradient(#000, #000) content-box,
        linear-gradient(#000, #000);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      padding: 1.5px;

      // 更克制的融合（透明度整体下调）
      opacity: 0.6;
      filter: blur(0.8px) saturate(140%);
    }

    // 玻璃反光效果 - 顶部弧形亮带（透明度同步下调）
    &::after {
      content: '';
      position: absolute;
      top: 1px;
      left: 12%;
      right: 12%;
      height: 75px;
      background: linear-gradient(
        180deg,
        rgba(255, 255, 255, 0.28) 0%,
        rgba(255, 255, 255, 0.13) 25%,
        rgba(255, 255, 255, 0.04) 55%,
        rgba(255, 255, 255, 0) 100%
      );
      border-radius: 23px 23px 50% 50% / 23px 23px 100% 100%;
      pointer-events: none;
      z-index: 1;
      opacity: 0.8;
      filter: blur(1px);
    }
  }

  .tips {
    text-align: center;
    margin-top: 20px;
    display: flex;
    justify-content: center;
    gap: 10px;
  }

  .register-link {
    text-align: center;
    margin-top: 18px;
    font-size: 14px;
    color: #555;
    // 增强文字可见性
    background: rgba(255, 255, 255, 0.8);
    padding: 8px 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);

    .register-btn {
      font-size: 14px;
      color: $primary_color;
      padding: 0;
      margin-left: 4px;
      font-weight: 600;
      text-shadow: 0 1px 2px rgba(64, 158, 255, 0.2);

      &:hover {
        color: darken($primary_color, 10%);
        transform: scale(1.05);
        transition: all 0.3s ease;
      }
    }
  }

  .svg-container {
    padding: 8px 10px 8px 18px;
    color: #4a4a55;
    vertical-align: middle;
    width: 35px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 600;
    // 移除背景框，只保留图案
    background: transparent;
    box-shadow: none;
    transition: all 0.3s ease;

    i {
      color: #409eff;
      // 增强图标亮度和可见性
      filter: drop-shadow(0 0 8px rgba(64, 158, 255, 0.6)) drop-shadow(0 0 12px rgba(64, 158, 255, 0.4));
      font-size: 22px;
    }

    &:hover {
      i {
        filter: drop-shadow(0 0 12px rgba(64, 158, 255, 0.8)) drop-shadow(0 0 16px rgba(64, 158, 255, 0.6));
        transform: scale(1.15);
      }
    }
  }

  // 用户名框图标 - 荧光蓝色
  .svg-container-username {
    i {
      color: #00d4ff;
      filter: drop-shadow(0 0 8px rgba(0, 212, 255, 1)) drop-shadow(0 0 16px rgba(0, 212, 255, 0.8)) drop-shadow(0 0 24px rgba(0, 212, 255, 0.6));
    }
    &:hover i {
      filter: drop-shadow(0 0 12px rgba(0, 212, 255, 1)) drop-shadow(0 0 24px rgba(0, 212, 255, 0.9)) drop-shadow(0 0 36px rgba(0, 212, 255, 0.7));
      transform: scale(1.15);
    }
  }

  // 密码框图标 - 荧光绿色
  .svg-container-password {
    i {
      color: #00ff88;
      filter: drop-shadow(0 0 8px rgba(0, 255, 136, 1)) drop-shadow(0 0 16px rgba(0, 255, 136, 0.8)) drop-shadow(0 0 24px rgba(0, 255, 136, 0.6));
    }
    &:hover i {
      filter: drop-shadow(0 0 12px rgba(0, 255, 136, 1)) drop-shadow(0 0 24px rgba(0, 255, 136, 0.9)) drop-shadow(0 0 36px rgba(0, 255, 136, 0.7));
      transform: scale(1.15);
    }
  }

  // 姓名框图标 - 荧光橙色
  .svg-container-name {
    i {
      color: #ff8c00;
      filter: drop-shadow(0 0 8px rgba(255, 140, 0, 1)) drop-shadow(0 0 16px rgba(255, 140, 0, 0.8)) drop-shadow(0 0 24px rgba(255, 140, 0, 0.6));
    }
    &:hover i {
      filter: drop-shadow(0 0 12px rgba(255, 140, 0, 1)) drop-shadow(0 0 24px rgba(255, 140, 0, 0.9)) drop-shadow(0 0 36px rgba(255, 140, 0, 0.7));
      transform: scale(1.15);
    }
  }

  .title-container {
    position: relative;
    text-align: center;
    margin-bottom: 35px;

    .logo-image {
      width: 220px;
      height: auto;
      margin-bottom: 16px;
      filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
      transition: transform 0.3s ease;

      &:hover {
        transform: scale(1.05);
      }
    }
  }

  .show-pwd {
    position: absolute;
    right: 18px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 17px;
    color: rgba(100, 100, 110, 0.7);
    cursor: pointer;
    user-select: none;
    transition: all 0.3s ease;
    z-index: 10;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;

    &:hover {
      color: $primary_color;
      transform: translateY(-50%) scale(1.15);
      background: rgba(64, 158, 255, 0.08);
    }
  }

  .login-button {
    width: 100%;
    height: 50px;
    border-radius: 25px;
    font-size: 17px;
    font-weight: 600;
    letter-spacing: 3px;
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.5);
    color: #333;
    transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
    margin-top: 10px;
    box-shadow: 0 4px 15px rgba(255, 255, 255, 0.25);

    &:hover {
      transform: translateY(-3px) scale(1.02);
      background: rgba(255, 255, 255, 0.95);
      box-shadow: 0 8px 25px rgba(255, 255, 255, 0.35);
    }

    &:active {
      transform: translateY(0) scale(0.98);
    }
  }
}

// ==================== 关键帧动画 ====================

// 主渐变循环动画 (7秒周期)
@keyframes gradientCycle {
  0% {
    background-position: 0% 50%;
  }
  25% {
    background-position: 100% 50%;
  }
  50% {
    background-position: 100% 100%;
  }
  75% {
    background-position: 0% 100%;
  }
  100% {
    background-position: 0% 50%;
  }
}

// 水墨漂浮效果 - 层1
@keyframes inkFloat1 {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.6;
  }
  33% {
    transform: translate(30px, -30px) rotate(120deg) scale(1.1);
    opacity: 0.75;
  }
  66% {
    transform: translate(-20px, 20px) rotate(240deg) scale(0.95);
    opacity: 0.65;
  }
}

// 水墨漂浮效果 - 层2
@keyframes inkFloat2 {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.5;
  }
  33% {
    transform: translate(-25px, 25px) rotate(-120deg) scale(1.08);
    opacity: 0.65;
  }
  66% {
    transform: translate(20px, -20px) rotate(-240deg) scale(0.92);
    opacity: 0.55;
  }
}

// 水墨漂浮效果 - 层3
@keyframes inkFloat3 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.4;
  }
  50% {
    transform: translate(15px, -15px) scale(1.15);
    opacity: 0.55;
  }
}

// 融合脉冲效果



// 玻璃卡片入场动画
@keyframes glassSlideIn {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.95);
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    backdrop-filter: blur(20px);
  }
}

// 响应式设计
@media screen and (max-width: 600px) {
  .login-container {
    .login-form.glass-card {
      padding: 40px 30px;
      right: 20px;
      width: 92%;
    }

    .center-title {
      top: 150px;
      left: 20px;

      .main-title {
        font-size: 28px;
      }
    }

    .top-left-logo {
      img {
        width: 250px;
      }
    }

    .copyright-footer {
      padding: 10px 0;
      font-size: 11px;
    }
  }
}

// 左上角Logo样式
.top-left-logo {
  position: fixed;
  top: 60px;
  left: 80px;
  z-index: 100;

  img {
    width: 400px;
    height: auto;
    filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3)) brightness(1.1);
    transition: all 0.3s ease;
    opacity: 0.9;

    &:hover {
      transform: scale(1.08);
      opacity: 1;
      filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.4)) brightness(1.15);
    }
  }
}

// 页面中间标题 - 位于logo正下方，页面左侧
.center-title {
  position: fixed;
  top: 220px;
  left: 110px;
  z-index: 100;
  text-align: left;

  .main-title {
    font-size: 56px;
    color: #fff;
    margin: 0 0 16px 0;
    font-weight: 800;
    letter-spacing: 6px;
    text-shadow:
      0 0 10px rgba(64, 158, 255, 0.8),
      0 0 20px rgba(64, 158, 255, 0.6),
      0 0 30px rgba(64, 158, 255, 0.4),
      0 0 40px rgba(64, 158, 255, 0.3),
      0 0 50px rgba(64, 158, 255, 0.2),
      0 2px 4px rgba(0, 0, 0, 0.3);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;

    i {
      margin-right: 12px;
      color: #fff;
      filter: drop-shadow(0 0 10px rgba(255, 255, 255, 1)) drop-shadow(0 0 20px rgba(255, 255, 255, 0.8)) drop-shadow(0 0 30px rgba(255, 255, 255, 0.6));
      font-size: 48px;
    }
  }

  .main-subtitle {
    font-size: 24px;
    color: #fff;
    margin: 0;
    letter-spacing: 4px;
    font-weight: 600;
    font-family: "Consolas", "Courier New", monospace;
    text-transform: none;
    text-shadow:
      0 0 8px rgba(145, 204, 117, 0.7),
      0 0 16px rgba(145, 204, 117, 0.5),
      0 0 24px rgba(145, 204, 117, 0.3),
      0 0 32px rgba(145, 204, 117, 0.2),
      0 2px 3px rgba(0, 0, 0, 0.2);
  }
}

// 版权信息样式
.copyright-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  text-align: center;
  padding: 20px 0;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 10;
  transition: all 0.3s ease;

  // 深色模式（默认）
  background: rgba(0, 0, 0, 0.6);
  border-top: 2px solid rgba(255, 255, 255, 0.2);

  p {
    margin: 0;
    color: #fff;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 2px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease;
  }
}

// 浅色模式下的版权信息
body.theme-light .copyright-footer {
  background: rgba(255, 255, 255, 0.8);
  border-top: 2px solid rgba(64, 158, 255, 0.3);

  p {
    color: #409eff;
    text-shadow: 0 2px 4px rgba(64, 158, 255, 0.2);
  }
}
</style>

<template>
  <div class="dashboard-container">
    <!-- 欢迎横幅 -->
    <div class="welcome-banner">
      <div class="ink-bg" ref="inkBg"></div>
      <div class="banner-content">
        <div class="welcome-info">
          <el-avatar :size="90" :src="avatarSrc" class="user-avatar"></el-avatar>
          <div class="welcome-text">
            <h1>👋 你好，{{ name }}！</h1>
            <p class="subtitle">{{ welcomeMessage }}</p>
            <div class="time-display">
              <i class="el-icon-time"></i>
              <span>{{ currentTime }}</span>
              <el-divider direction="vertical"></el-divider>
              <i class="el-icon-date"></i>
              <span>{{ currentDate }}</span>
            </div>
          </div>
        </div>
        <div class="banner-actions">
          <el-button type="primary" icon="el-icon-plus" round @click="$router.push('/article/create')">发布文章</el-button>
          <el-button v-if="isAdmin" type="success" icon="el-icon-user" round @click="$router.push('/user/create')">新增用户</el-button>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="24" style="margin-bottom: 10px; text-align: right;">
        <el-button size="mini" icon="el-icon-refresh" :loading="loadingStats" @click="fetchStats">刷新数据</el-button>
        <span style="font-size: 12px; color: #909399; margin-left: 10px;">最后更新: {{ lastUpdateTime }}</span>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6" v-for="(stat, index) in stats" :key="index">
        <div class="stat-card" :class="stat.type" @click="handleStatClick(stat)"
             @mousemove="handleCardMouseMove($event, index)" @mouseleave="handleCardMouseLeave(index)">
          <div class="stat-bg-image" :style="{backgroundImage: `url(${stat.bgImage})`}"></div>
          <div class="stat-bg"></div>
          <div class="stat-content">
            <div class="stat-header">
              <div class="stat-icon">
                <i :class="stat.icon"></i>
              </div>
              <div v-if="loadingStats" class="loading-indicator">
                <i class="el-icon-loading"></i>
              </div>
            </div>
            <div class="stat-value">
              <span class="number">{{ formatNumber(stat.value) }}</span>
              <span class="unit">{{ stat.unit }}</span>
            </div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 主要内容区 -->
    <el-row :gutter="20" style="margin-top: 25px;" type="flex" class="main-content-row">
      <!-- 左侧内容 -->
      <el-col :xs="24" :sm="24" :md="16" class="main-col-left">
        <!-- 快捷操作 -->
        <el-card shadow="hover" class="action-card">
          <div slot="header" class="card-title">
            <i class="el-icon-s-operation"></i>
            <span>快捷操作</span>
          </div>
          <div class="quick-actions-grid">
            <div class="action-item" v-for="(action, index) in filteredQuickActions" :key="index" @click="$router.push(action.path)" @mouseenter="onActionHover(index)">
              <div class="action-icon" :class="{ rotated: rotatedActions[index] }" :style="{background: action.gradient}">
                <i :class="action.icon"></i>
              </div>
              <span class="action-label">{{ action.label }}</span>
            </div>
          </div>
        </el-card>

        <!-- 公司介绍 -->
        <el-card shadow="hover" class="activity-card">
          <div slot="header" class="card-title">
            <i class="el-icon-office-building"></i>
            <span>公司介绍</span>
            <el-button type="text" @click="$router.push('/school/intro')">查看详情</el-button>
          </div>
          <div class="company-intro-content">
            <div class="intro-text">
              <p>集美大学诚毅学院是经国家教育部批准，由集美大学与福建集美大学教育发展有限公司联合举办的独立学院，成立于2003年。</p>
              <p>学院秉承陈嘉庚先生"诚毅"校训，坚持"以学生为本"的办学理念，致力于培养具有创新精神、实践能力和社会责任感的高素质应用型人才。</p>
            </div>
            <div class="intro-stats">
              <div class="stat-item">
                <i class="el-icon-school"></i>
                <span>占地面积</span>
                <strong>600亩</strong>
              </div>
              <div class="stat-item">
                <i class="el-icon-user"></i>
                <span>在校学生</span>
                <strong>10000+</strong>
              </div>
              <div class="stat-item">
                <i class="el-icon-reading"></i>
                <span>专业数量</span>
                <strong>30+</strong>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧边栏 -->
      <el-col :xs="24" :sm="24" :md="8" class="main-col-right">
        <!-- 词云 -->
        <el-card shadow="hover" class="wordcloud-card">
          <div slot="header" class="card-title">
            <i class="el-icon-picture-outline"></i>
            <span>热门标签</span>
          </div>
          <div ref="wordCloudChart" class="wordcloud-chart"></div>
        </el-card>

        <!-- 系统信息 -->
        <el-card shadow="hover" class="system-card">
          <div slot="header" class="card-title">
            <i class="el-icon-s-tools"></i>
            <span>系统信息</span>
          </div>
          <div class="system-info-list">
            <div class="info-row" v-for="(info, index) in systemInfo" :key="index">
              <span class="info-label">{{ info.label }}</span>
              <el-tag :type="info.tagType" size="small">{{ info.value }}</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import request from '@/utils/request'
import * as echarts from 'echarts'
import 'echarts-wordcloud'

export default {
  name: 'Dashboard',
  data() {
    return {
      welcomeMessage: '',
      currentTime: '',
      timer: null,
      refreshTimer: null,
      loadingStats: false,
      lastUpdateTime: '加载中...',
      stats: [
        {
          label: '用户总数', value: 0, unit: '人', icon: 'el-icon-user-solid', type: 'primary',
          tagType: '', trend: '实时', change: 0,
          bgImage: require('@/views/log/1.jpg')
        },
        {
          label: '文章总数', value: 0, unit: '篇', icon: 'el-icon-document', type: 'success',
          tagType: 'success', trend: '实时', change: 0,
          bgImage: require('@/views/log/2.jpg')
        },
        {
          label: '评论总数', value: 0, unit: '条', icon: 'el-icon-chat-line-round', type: 'warning',
          tagType: 'warning', trend: '实时', change: 0,
          bgImage: require('@/views/log/3.jpg')
        },
        {
          label: '总浏览量', value: 0, unit: '次', icon: 'el-icon-view', type: 'danger',
          tagType: 'danger', trend: '实时', change: 0,
          bgImage: require('@/views/log/4.jpg')
        }
      ],
      quickActions: [
        { label: '发布文章', icon: 'el-icon-edit-outline', path: '/article/create', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
        { label: '新增用户', icon: 'el-icon-user', path: '/user/create', gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', adminOnly: true },
        { label: '数据报表', icon: 'el-icon-data-analysis', path: '/report/index', gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' },
        { label: '学校介绍', icon: 'el-icon-office-building', path: '/school/intro', gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' },
        { label: '文章列表', icon: 'el-icon-document', path: '/article/list', gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
        { label: '用户列表', icon: 'el-icon-user-solid', path: '/user/list', gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)', adminOnly: true }
      ],
      rotatedActions: {},
      systemInfo: [
        { label: '系统版本', value: 'v2.0.0', tagType: '' },
        { label: '后端框架', value: 'Flask + MySQL', tagType: 'success' },
        { label: '前端框架', value: 'Vue 2 + Element UI', tagType: 'warning' },
        { label: '认证方式', value: 'JWT Token', tagType: 'danger' },
        { label: '运行状态', value: '正常运行', tagType: 'success' }
      ],
      wordCloudData: [],
      wordCloudChart: null,
      cardRotations: {}
    }
  },
  computed: {
    ...mapGetters(['name', 'avatar', 'isAdmin']),
    avatarSrc() {
      if (this.avatar && this.avatar.trim() !== '') {
        return this.avatar
      }
      return require('@/views/login/5.gif')
    },
    currentDate() {
      const date = new Date()
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      })
    },
    filteredQuickActions() {
      return this.quickActions.filter(action => {
        if (action.adminOnly && !this.isAdmin) {
          return false
        }
        return true
      })
    }
  },
  mounted() {
    this.setWelcomeMessage()
    this.updateTime()
    this.timer = setInterval(this.updateTime, 1000)
    // 首次加载数据
    this.fetchStats()
    this.fetchHotArticles()
    // 所有用户每10分钟自动刷新
    this.refreshTimer = setInterval(() => {
      this.fetchStats()
      this.fetchHotArticles()
    }, 600000)
    // 初始化墨水背景动画
    this.initInkBg()
    // 初始化词云
    this.$nextTick(() => {
      this.initWordCloud()
    })
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer)
    }
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer)
    }
    // 销毁词云实例
    if (this.wordCloudChart) {
      this.wordCloudChart.dispose()
    }
  },
  methods: {
    setWelcomeMessage() {
      const messages = [
        '欢迎回来干活，今天顺顺利利！',
        '系统一切正常，干活不踩坑。',
        '好好处理手头工作，今天轻松下班。'
      ]
      this.welcomeMessage = messages[Math.floor(Math.random() * messages.length)]
    },
    updateTime() {
      this.currentTime = new Date().toLocaleTimeString('zh-CN')
    },
    formatNumber(num) {
      if (num === 0 || num === null || num === undefined) return '0'
      const n = Number(num)
      if (n >= 10000) {
        return (n / 10000).toFixed(1) + '万'
      }
      return n.toLocaleString()
    },
    // 从后端获取实时统计数据
    async fetchStats() {
      this.loadingStats = true
      try {
        const data = await request({
          url: '/vue-admin-template/db/stats',
          method: 'get'
        })
        if (data && data.code === 20000) {
          const payload = data.data

          this.stats[0].value = Number(payload.users) || 0
          this.stats[1].value = Number(payload.articles) || 0
          this.stats[2].value = Number(payload.comments) || 0
          this.stats[3].value = Number(payload.pageviews) || 0

          this.lastUpdateTime = new Date().toLocaleTimeString('zh-CN')
        }
      } catch (error) {
      } finally {
        this.loadingStats = false
      }
    },
    // 获取热门文章数据用于词云
    async fetchHotArticles() {
      try {
        const res = await request({
          url: '/vue-admin-template/report/hot-articles',
          method: 'get'
        })
        if (res && res.code === 20000 && res.data) {
          this.wordCloudData = res.data.map((article, index) => {
            const fontFamilies = [
              'sans-serif', 'Arial', 'Microsoft YaHei', 'SimHei', 'SimSun',
              'KaiTi', 'FangSong', 'STHeiti', 'PingFang SC', 'Helvetica'
            ]
            const colors = [
              '#5470c6', '#91cc75', '#fac858', '#ee6666',
              '#73c0de', '#3ba272', '#fc8452', '#9a60b4',
              '#ea7ccc', '#5470c6', '#91cc75', '#fac858'
            ]
            return {
              name: article.title,
              value: Math.floor(Math.random() * 100) + 10,
              id: article.id,
              textStyle: {
                fontFamily: fontFamilies[Math.floor(Math.random() * fontFamilies.length)],
                fontSize: Math.floor(Math.random() * 40) + 14,
                color: colors[Math.floor(Math.random() * colors.length)]
              }
            }
          })
          // 数据更新后重新渲染词云
          if (this.wordCloudChart) {
            this.wordCloudChart.setOption({
              series: [{
                data: this.wordCloudData
              }]
            })
          }
        }
      } catch (error) {
        console.error('获取热门文章失败:', error)
      }
    },
    handleStatClick(stat) {
      if (stat.label === '用户总数') {
        if (!this.isAdmin) {
          this.$message.warning('需要管理员权限')
          return
        }
        this.$router.push('/user/list')
      } else if (stat.label === '文章总数') {
        this.$router.push('/article/list')
      } else if (stat.label === '评论总数') {
        if (!this.isAdmin) {
          this.$message.warning('需要管理员权限')
          return
        }
        this.$router.push('/report/comment')
      } else {
        this.$message.info(`${stat.label}: ${this.formatNumber(stat.value)} ${stat.unit}`)
      }
    },
    onActionHover(index) {
      if (!this.rotatedActions[index]) {
        this.$set(this.rotatedActions, index, true)
      }
    },
    handleCardMouseMove(event, index) {
      const card = event.currentTarget
      const rect = card.getBoundingClientRect()
      const x = event.clientX - rect.left
      const y = event.clientY - rect.top
      const centerX = rect.width / 2
      const centerY = rect.height / 2
      const rotateX = ((y - centerY) / centerY) * -20
      const rotateY = ((x - centerX) / centerX) * 20
      this.$set(this.cardRotations, index, { rotateX, rotateY })
      card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(0.95)`
    },
    handleCardMouseLeave(index) {
      this.$set(this.cardRotations, index, { rotateX: 0, rotateY: 0 })
      // 直接操作DOM元素来恢复原位
      const cards = document.querySelectorAll('.stat-card')
      if (cards[index]) {
        cards[index].style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) scale(1)'
      }
    },
    // 墨水背景动画相关方法
    initInkBg() {
      if (this.$refs.inkBg) {
        this.$refs.inkBg.style.backgroundImage = this.buildGradient(this.buildSequence())
      }
    },
    hexToRgb(hex) {
      const h = hex.replace('#', '')
      return {
        r: parseInt(h.slice(0, 2), 16),
        g: parseInt(h.slice(2, 4), 16),
        b: parseInt(h.slice(4, 6), 16)
      }
    },
    buildSequence() {
      const COLOR_RING = [
        '#FF0000', '#FF3300', '#FF6600', '#FF9900', '#FFFF00',
        '#CCFF00', '#66FF33', '#00CC33', '#00CC99', '#0099CC',
        '#0066FF', '#3333CC', '#330099', '#660099', '#9900CC',
        '#CC00CC', '#CC0099', '#FF0066', '#FF0033', '#FF0000',
      ]
      const len = COLOR_RING.length - 1
      const startOffset = Math.random() * len
      const n = 24
      const seq = []
      for (let i = 0; i < n; i++) {
        const t = (startOffset + (i / n) * len) % len
        const idx = Math.floor(t)
        const frac = t - idx
        const c1 = this.hexToRgb(COLOR_RING[idx])
        const c2 = this.hexToRgb(COLOR_RING[idx + 1])
        seq.push({
          r: Math.round(c1.r * (1 - frac) + c2.r * frac),
          g: Math.round(c1.g * (1 - frac) + c2.g * frac),
          b: Math.round(c1.b * (1 - frac) + c2.b * frac),
        })
      }
      seq.push(seq[0])
      return seq
    },
    buildGradient(seq) {
      const n = seq.length - 1
      const stops = seq.map((c, i) => {
        const r = Math.round(c.r * 0.55)
        const g = Math.round(c.g * 0.55)
        const b = Math.round(c.b * 0.55)
        return `rgb(${r}, ${g}, ${b}) ${((i / n) * 100).toFixed(2)}%`
      })
      return `linear-gradient(90deg, ${stops.join(', ')})`
    },
    initWordCloud() {
      if (!this.$refs.wordCloudChart) return
      this.wordCloudChart = echarts.init(this.$refs.wordCloudChart)
      const option = {
        tooltip: {
          show: true,
          formatter: function(params) {
            return params.name + '<br/>浏览量: ' + params.value + '次'
          }
        },
        series: [{
          type: 'wordCloud',
          shape: 'cloud',
          left: 'center',
          top: 'center',
          width: '90%',
          height: '90%',
          right: null,
          bottom: null,
          sizeRange: [12, 60],
          rotationRange: [-45, 45],
          rotationStep: 15,
          gridSize: 8,
          drawOutOfBound: false,
          shrinkToFit: true,
          layoutAnimation: true,
          textStyle: {
            fontWeight: 'bold'
          },
          emphasis: {
            focus: 'self',
            textStyle: {
              shadowBlur: 10,
              shadowColor: '#333'
            }
          },
          data: this.wordCloudData
        }]
      }
      this.wordCloudChart.setOption(option)
      // 添加点击事件
      this.wordCloudChart.on('click', (params) => {
        if (params.data && params.data.id) {
          this.$router.push(`/article/detail/${params.data.id}`)
        }
      })
      // 响应窗口大小变化
      window.addEventListener('resize', () => {
        this.wordCloudChart && this.wordCloudChart.resize()
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: calc(100vh - 84px);

  // 加载指示器
  .loading-indicator {
    font-size: 16px;
    color: #409eff;
    animation: spin 1s linear infinite;
  }

  // 欢迎横幅
  .welcome-banner {
    background-color: #0a0812;
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 25px;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(10, 8, 18, 0.6);
    animation: slideInDown 0.8s ease-out;

    // 墨水背景动画
    .ink-bg {
      position: absolute;
      inset: -15%;
      z-index: 0;
      background-color: #0a0812;
      background-size: 400% 100%;
      background-repeat: repeat-x;
      filter: blur(60px) saturate(1.15);
      animation: inkLoop 40s linear infinite;
    }

    .banner-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
      z-index: 2;
    }

    .welcome-info {
      display: flex;
      align-items: center;

      .user-avatar {
        border: 4px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;

        &:hover {
          transform: scale(1.1) rotate(5deg);
        }
      }

      .welcome-text {
        margin-left: 25px;

        h1 {
          margin: 0 0 8px 0;
          font-size: 28px;
          font-weight: 700;
          background: linear-gradient(90deg, #00ff87, #60efff, #00ff87);
          background-size: 200% auto;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          animation: gradientMove 3s linear infinite, fadeInLeft 0.8s ease-out;
          filter: drop-shadow(0 0 8px rgba(0, 255, 135, 0.6)) drop-shadow(0 0 20px rgba(96, 239, 255, 0.4));
        }

        .subtitle {
          margin: 0 0 12px 0;
          font-size: 16px;
          color: #ffeb3b;
          text-shadow: 0 0 10px rgba(255, 235, 59, 0.8), 0 0 20px rgba(255, 235, 59, 0.6), 0 0 30px rgba(255, 235, 59, 0.4);
          animation: glow 2s ease-in-out infinite alternate, fadeInLeft 1s ease-out;
        }

        .time-display {
          display: flex;
          align-items: center;
          font-size: 14px;
          opacity: 0.9;
          gap: 8px;
          animation: fadeInLeft 1.2s ease-out;

          i {
            font-size: 16px;
          }
        }
      }
    }

    .banner-actions {
      display: flex;
      gap: 12px;

      .el-button {
        border-radius: 25px;
        padding: 12px 28px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;

        &:hover {
          transform: translateY(-3px);
          box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
      }
    }
  }

  // 统计卡片
  .stat-cards {
    .stat-card {
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(10px) saturate(160%) brightness(1.08);
      -webkit-backdrop-filter: blur(10px) saturate(160%) brightness(1.08);
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
      transition: transform 0.1s ease-out, box-shadow 0.3s ease, background 0.3s ease;
      animation: zoomIn 0.6s ease-out;

      &:nth-child(1) { animation-delay: 0.1s; }
      &:nth-child(2) { animation-delay: 0.2s; }
      &:nth-child(3) { animation-delay: 0.3s; }
      &:nth-child(4) { animation-delay: 0.4s; }

      &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: transparent;
        opacity: 0;
        transition: opacity 0.3s ease;
      }

      &.primary { --card-color: transparent; }
      &.success { --card-color: transparent; }
      &.warning { --card-color: transparent; }
      &.danger { --card-color: transparent; }

      &:hover {
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.45);

        &::before {
          opacity: 0;
        }

        .stat-bg-image {
          filter: blur(8px) brightness(0.8);
          transform: scale(1.1);
        }

        .stat-bg {
          transform: scale(1.1);
          opacity: 0;
        }

        .stat-value .number {
          text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }

        .stat-label {
          text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
        }

        .stat-value .unit {
          color: #00ff87;
          text-shadow: 0 0 5px #00ff87, 0 0 10px #00ff87, 0 0 20px #00ff87;
        }
      }

      .stat-bg-image {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        z-index: 0;
        transition: all 0.4s ease;
      }

      .stat-bg {
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: transparent;
        transition: all 0.4s ease;
        z-index: 0;
      }

      .stat-content {
        position: relative;
        z-index: 1;

        .stat-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;

          .stat-icon {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
          }
        }

        .stat-value {
          margin-bottom: 8px;

          .number {
            font-size: 36px;
            font-weight: 800;
            color: #303133;
            line-height: 1;
          }

          .unit {
            font-size: 14px;
            color: #606266;
            margin-left: 4px;
            transition: all 0.3s ease;
          }
        }

        .stat-label {
          font-size: 14px;
          color: #606266;
          font-weight: 500;
          margin-bottom: 12px;
        }
      }
    }
  }

  // 卡片通用样式
  .action-card,
  .activity-card,
  .system-card,
  .wordcloud-card {
    border-radius: 16px;
    border: none;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    animation: fadeInUp 0.6s ease-out;

    &:hover {
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
      transform: translateY(-4px);
    }

    ::v-deep .el-card__header {
      border-bottom: 2px solid #f0f2f5;
      padding: 16px 20px;
    }

    ::v-deep .el-card__body {
      padding: 20px;
    }
  }

  // 主要内容区 - Flexbox 等高布局
  .main-content-row {
    display: flex;
    align-items: stretch;
  }

  .main-col-left,
  .main-col-right {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .main-col-left .action-card,
  .main-col-right .system-card {
    flex: 0 0 auto;
  }

  .main-col-left .activity-card,
  .main-col-right .wordcloud-card {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;

    ::v-deep .el-card__body {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
  }

  // 快捷操作与系统信息卡片
  .action-card,
  .system-card {
    ::v-deep .el-card__body {
      min-height: auto;
    }
  }

  .wordcloud-card {
    ::v-deep .el-card__header {
      border-bottom: 2px solid #e8e8e8;
      padding: 26px 20px;
    }
    .wordcloud-chart {
      width: 100%;
      flex: 1;
      min-height: 200px;
    }
  }

  .activity-card {
    ::v-deep .el-card__body {
      min-height: auto;
    }
  }

  // 公司介绍内容样式
  .company-intro-content {
    padding: 15px 0;

    .intro-text {
      margin-bottom: 25px;

      p {
        font-size: 15px;
        line-height: 2;
        color: #4a4a4a;
        margin-bottom: 15px;
        text-indent: 2em;
        font-family: 'Microsoft YaHei', 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
        letter-spacing: 0.8px;
        text-align: justify;
      }

      p:first-child {
        font-size: 16px;
        font-weight: 600;
        color: #2c3e50;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }
    }

    .intro-stats {
      display: flex;
      justify-content: space-around;
      padding: 25px 15px;
      border-top: 2px dashed #e4e7ed;
      gap: 15px;

      .stat-item {
        text-align: center;
        padding: 20px 15px;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        flex: 1;
        min-width: 100px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);

        &:hover {
          transform: translateY(-8px) scale(1.05);
          box-shadow: 0 12px 24px rgba(102, 126, 234, 0.4);
        }

        i {
          font-size: 32px;
          display: block;
          margin-bottom: 10px;
          filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
        }

        span {
          font-size: 13px;
          opacity: 0.9;
          display: block;
          margin-bottom: 8px;
          letter-spacing: 1px;
        }

        strong {
          font-size: 24px;
          font-weight: bold;
          display: block;
          text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
      }
    }
  }

  .card-title {
    display: flex;
    align-items: center;
    font-size: 17px;
    font-weight: 700;
    color: #303133;

    i {
      margin-right: 10px;
      font-size: 20px;
      color: #409eff;
    }

    .el-button {
      margin-left: auto;
      font-weight: 500;
    }

    .realtime-tag {
      margin-left: 10px;
      font-size: 12px;
      color: #67c23a;
      font-weight: 500;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      animation: pulse 2s ease-in-out infinite;

      i {
        font-size: 12px;
        margin-right: 2px;
        color: #67c23a;
      }
    }
  }

  .empty-tip {
    padding: 40px 0;
    text-align: center;
    color: #909399;
    font-size: 14px;
  }

  // 快捷操作网格
  .quick-actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px;
    padding: 10px 0;

    .action-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px 10px;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      background: #fafafa;

      &:hover {
        transform: translateY(-5px) scale(1.05);
        background: white;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
      }

      .action-icon {
        width: 56px;
        height: 56px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        color: white;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);

        &.rotated {
          animation: rotateCounterClockwise 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }
      }

      .action-label {
        font-size: 14px;
        font-weight: 600;
        color: #303133;
      }
    }
  }

  // 最近活动
  .activity-list {
    .activity-item {
      display: flex;
      align-items: flex-start;
      padding: 14px 0;
      border-bottom: 1px solid #f5f7fa;
      transition: all 0.3s ease;

      &:last-child {
        border-bottom: none;
      }

      &:hover {
        background: #fafafa;
        padding-left: 10px;
        border-radius: 8px;
      }

      .activity-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 12px;
        margin-top: 6px;
        flex-shrink: 0;

        &.success { background: #67c23a; box-shadow: 0 0 10px rgba(103, 194, 58, 0.5); }
        &.primary { background: #409eff; box-shadow: 0 0 10px rgba(64, 158, 255, 0.5); }
        &.warning { background: #e6a23c; box-shadow: 0 0 10px rgba(230, 162, 60, 0.5); }
        &.danger { background: #f56c6c; box-shadow: 0 0 10px rgba(245, 108, 108, 0.5); }
        &.info { background: #909399; box-shadow: 0 0 10px rgba(144, 147, 153, 0.5); }
      }

      .activity-content {
        flex: 1;

        .activity-text {
          font-size: 14px;
          color: #303133;
          line-height: 1.5;
          margin-bottom: 4px;
          word-break: break-all;

          strong {
            color: #409eff;
            font-weight: 600;
          }

          em {
            color: #67c23a;
            font-style: normal;
            font-weight: 500;
          }
        }

        .activity-time {
          font-size: 12px;
          color: #909399;
        }
      }
    }
  }

  // 系统信息
  .system-info-list {
    .info-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid #f5f7fa;
      transition: all 0.3s ease;

      &:last-child {
        border-bottom: none;
      }

      &:hover {
        background: #fafafa;
        padding: 12px 10px;
        margin: 0 -10px;
        border-radius: 8px;
      }

      .info-label {
        font-size: 14px;
        color: #606266;
        font-weight: 500;
      }
    }
  }
}

// 动画定义
@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes rotateCounterClockwise {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(-360deg);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes gradientMove {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}

@keyframes glow {
  from {
    text-shadow: 0 0 10px rgba(255, 235, 59, 0.8), 0 0 20px rgba(255, 235, 59, 0.6), 0 0 30px rgba(255, 235, 59, 0.4);
  }
  to {
    text-shadow: 0 0 15px rgba(255, 235, 59, 1), 0 0 30px rgba(255, 235, 59, 0.8), 0 0 45px rgba(255, 235, 59, 0.6), 0 0 60px rgba(255, 235, 59, 0.4);
  }
}

// 墨水背景动画关键帧：移动一整张渐变图，首尾同色无缝接回
@keyframes inkLoop {
  from { background-position: 0% 0%; }
  to   { background-position: 400% 0%; }
}

// 响应式设计
@media screen and (max-width: 1200px) {
  .welcome-banner .banner-content {
    flex-direction: column;
    text-align: center;

    .welcome-info {
      flex-direction: column;
      margin-bottom: 20px;

      .welcome-text {
        margin-left: 0;
        margin-top: 15px;
      }
    }
  }
}

@media screen and (max-width: 768px) {
  .stat-cards .stat-card .stat-content .stat-value .number {
    font-size: 28px;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

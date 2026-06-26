<template>
  <div class="app-container school-intro">
    <!-- Banner轮播图 -->
    <div class="banner-container">
      <div class="banner-slides">
        <div v-for="(banner, index) in banners" :key="index"
             :class="['banner-slide', { active: index === currentBannerIndex }]">
          <img :src="banner" alt="Banner" class="banner-image"
               @mouseenter="isBannerHover = true" @mouseleave="isBannerHover = false" />
        </div>
      </div>
      <div class="banner-overlay" :class="{ visible: isBannerHover }">
        <h1 class="banner-title">集美大学诚毅学院</h1>
        <p class="banner-subtitle">诚以待人 · 毅以处事</p>
      </div>
      <div class="banner-arrow banner-arrow-left" @click="prevBanner">
        <i class="el-icon-arrow-left"></i>
      </div>
      <div class="banner-arrow banner-arrow-right" @click="nextBanner">
        <i class="el-icon-arrow-right"></i>
      </div>
      <div class="banner-indicators">
        <span v-for="(banner, index) in banners" :key="index"
              :class="['indicator', { active: index === currentBannerIndex }]"
              @click="goToBanner(index)">
        </span>
      </div>
    </div>

    <!-- 公司简介 -->
    <el-card shadow="hover" class="intro-card">
      <div slot="header" class="card-header">
        <i class="el-icon-office-building"></i>
        <span>公司简介</span>
      </div>
      <div class="card-content">
        <p>集美大学诚毅学院是经国家教育部批准，由集美大学与福建集美大学教育发展有限公司联合举办的独立学院，成立于2003年。</p>
        <p>学院秉承陈嘉庚先生"诚毅"校训，坚持"以学生为本"的办学理念，致力于培养具有创新精神、实践能力和社会责任感的高素质应用型人才。</p>
        <p>学院位于福建省厦门市集美区，占地面积约600亩，校园环境优美，教学设施完善，师资力量雄厚。</p>
      </div>
    </el-card>

    <!-- 发展历程 -->
    <el-card shadow="hover" class="history-card">
      <div slot="header" class="card-header">
        <i class="el-icon-time"></i>
        <span>发展历程</span>
      </div>
      <div class="card-content">
        <el-timeline class="custom-timeline">
          <el-timeline-item timestamp="2003年" placement="top" color="#667eea">
            <div class="timeline-content">
              <h4><i class="el-icon-flag"></i> 学院成立</h4>
              <p>集美大学诚毅学院经教育部批准正式成立</p>
            </div>
          </el-timeline-item>
          <el-timeline-item timestamp="2005年" placement="top" color="#764ba2">
            <div class="timeline-content">
              <h4><i class="el-icon-notebook-2"></i> 首批专业设置</h4>
              <p>开设经济学、管理学、文学、工学等学科门类</p>
            </div>
          </el-timeline-item>
          <el-timeline-item timestamp="2010年" placement="top" color="#f093fb">
            <div class="timeline-content">
              <h4><i class="el-icon-office-building"></i> 校园扩建</h4>
              <p>新校区投入使用，教学设施全面升级</p>
            </div>
          </el-timeline-item>
          <el-timeline-item timestamp="2015年" placement="top" color="#4facfe">
            <div class="timeline-content">
              <h4><i class="el-icon-edit"></i> 教学改革</h4>
              <p>推进应用型人才培养模式改革</p>
            </div>
          </el-timeline-item>
          <el-timeline-item timestamp="至今" placement="top" color="#43e97b">
            <div class="timeline-content">
              <h4><i class="el-icon-trophy"></i> 持续发展</h4>
              <p>不断优化专业结构，提升教学质量，为社会输送大批优秀人才</p>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>

    <!-- 院系设置 -->
    <el-card shadow="hover" class="department-card">
      <div slot="header" class="card-header">
        <i class="el-icon-office-building"></i>
        <span>院系设置</span>
      </div>
      <div class="card-content">
        <el-table :data="departments" border stripe>
          <el-table-column type="index" label="序号" width="80" align="center"></el-table-column>
          <el-table-column prop="name" label="系部名称" min-width="150"></el-table-column>
          <el-table-column prop="majors" label="主要专业" min-width="300"></el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 校园文化 -->
    <el-card shadow="hover" class="culture-card">
      <div slot="header" class="card-header">
        <i class="el-icon-star-on"></i>
        <span>校园文化</span>
      </div>
      <div class="card-content culture-grid">
        <div class="culture-item">
          <h4><i class="el-icon-medal"></i> 校训</h4>
          <p>诚以待人，毅以处事</p>
        </div>
        <div class="culture-item">
          <h4><i class="el-icon-trophy"></i> 校风</h4>
          <p>团结、勤奋、求实、创新</p>
        </div>
        <div class="culture-item">
          <h4><i class="el-icon-reading"></i> 学风</h4>
          <p>严谨、博学、笃行、致远</p>
        </div>
      </div>
    </el-card>

    <!-- 联系方式 -->
    <el-card shadow="hover" class="contact-card">
      <div slot="header" class="card-header">
        <i class="el-icon-phone"></i>
        <span>联系方式</span>
      </div>
      <div class="card-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="学校地址">福建省厦门市集美区集美学村</el-descriptions-item>
          <el-descriptions-item label="邮政编码">361021</el-descriptions-item>
          <el-descriptions-item label="联系电话">0592-6180000</el-descriptions-item>
          <el-descriptions-item label="电子邮箱">cyxy@jmu.edu.cn</el-descriptions-item>
          <el-descriptions-item label="学校官网" :span="2">
            <a href="https://chengyi.jmu.edu.cn" target="_blank">https://chengyi.jmu.edu.cn</a>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'SchoolIntro',
  data() {
    return {
      banners: [
        'https://chengyi.jmu.edu.cn/images/banner2.jpg',
        'https://chengyi.jmu.edu.cn/images/20251030.jpg',
        'https://chengyi.jmu.edu.cn/images/image_260302.jpg'
      ],
      currentBannerIndex: 0,
      bannerTimer: null,
      isBannerHover: false,
      departments: [
        { name: '经济系', majors: '经济学、国际经济与贸易、金融学' },
        { name: '管理系', majors: '工商管理、会计学、财务管理、行政管理' },
        { name: '信息工程系', majors: '计算机科学与技术、软件工程、网络工程' },
        { name: '中文系', majors: '汉语言文学、秘书学' },
        { name: '外语系', majors: '英语、日语' },
        { name: '艺术系', majors: '视觉传达设计、环境设计' }
      ]
    }
  },
  mounted() {
    this.startBannerAutoPlay()
  },
  beforeDestroy() {
    this.stopBannerAutoPlay()
  },
  methods: {
    nextBanner() {
      this.currentBannerIndex = (this.currentBannerIndex + 1) % this.banners.length
      this.resetBannerAutoPlay()
    },
    prevBanner() {
      this.currentBannerIndex = (this.currentBannerIndex - 1 + this.banners.length) % this.banners.length
      this.resetBannerAutoPlay()
    },
    goToBanner(index) {
      this.currentBannerIndex = index
      this.resetBannerAutoPlay()
    },
    startBannerAutoPlay() {
      this.bannerTimer = setInterval(() => {
        this.currentBannerIndex = (this.currentBannerIndex + 1) % this.banners.length
      }, 4000)
    },
    stopBannerAutoPlay() {
      if (this.bannerTimer) {
        clearInterval(this.bannerTimer)
      }
    },
    resetBannerAutoPlay() {
      this.stopBannerAutoPlay()
      this.startBannerAutoPlay()
    }
  }
}
</script>

<style scoped>
.school-intro {
  padding: 20px;
}

.banner-container {
  position: relative;
  width: 100%;
  margin-bottom: 25px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.banner-slides {
  position: relative;
  width: 100%;
  height: 500px;
}

.banner-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 1s ease-in-out;
}

.banner-slide.active {
  opacity: 1;
  z-index: 1;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.5s ease;
}

.banner-container:hover .banner-image {
  transform: scale(1.05);
}

.banner-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s ease;
  opacity: 0;
}

.banner-container:hover .banner-arrow {
  opacity: 1;
}

.banner-arrow:hover {
  background: rgba(0, 0, 0, 0.6);
}

.banner-arrow i {
  font-size: 24px;
  color: #fff;
}

.banner-arrow-left {
  left: 20px;
}

.banner-arrow-right {
  right: 20px;
}

.banner-indicators {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 10;
}

.indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator:hover {
  background: rgba(255, 255, 255, 0.8);
}

.indicator.active {
  background: #fff;
  transform: scale(1.2);
}

.banner-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 30px 30px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.4) 60%, transparent 100%);
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.banner-overlay.visible {
  opacity: 1;
}

.banner-title {
  font-size: 36px;
  font-weight: bold;
  color: #fff;
  margin: 0 0 10px 0;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  letter-spacing: 3px;
  animation: fadeInUp 0.8s ease;
}

.banner-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  letter-spacing: 5px;
  font-style: italic;
  animation: fadeInUp 0.8s ease 0.2s both;
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

.intro-card, .history-card, .department-card, .culture-card, .contact-card {
  margin-bottom: 25px;
  transition: all 0.3s ease;
  border-radius: 12px;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
  }
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: 1px;
}

.card-header i {
  margin-right: 12px;
  color: #667eea;
  font-size: 24px;
  filter: drop-shadow(0 2px 4px rgba(102, 126, 234, 0.3));
}

.card-content {
  line-height: 2;
  color: #4a4a4a;
  font-family: 'Microsoft YaHei', 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
  letter-spacing: 0.5px;
}

.card-content p {
  margin-bottom: 15px;
  font-size: 15px;
  text-align: justify;
  text-indent: 2em;
}

.card-content p:first-child {
  font-size: 16px;
  font-weight: 500;
  color: #2c3e50;
}

.culture-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.culture-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 25px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  min-height: 150px;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }
}

.culture-item h4 {
  margin-bottom: 12px;
  color: #2c3e50;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 1px;
  text-align: center;
}

.culture-item h4 i {
  margin-right: 8px;
  color: #e6a23c;
  font-size: 22px;
}

.culture-item .highlight {
  font-size: 32px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 12px 0;
  letter-spacing: 2px;
  text-align: center;
}

.culture-item p {
  text-align: center;
  font-size: 17px;
}

.culture-item .desc {
  color: #7a7a7a;
  font-size: 17px;
  font-style: italic;
  letter-spacing: 1px;
  text-align: center;
}

/* 发展历程时间轴样式 */
.custom-timeline {
  padding: 20px 0;

  ::v-deep .el-timeline-item__timestamp {
    font-size: 16px;
    font-weight: 600;
    color: #667eea;
    letter-spacing: 1px;
  }

  .timeline-content {
    padding: 15px 20px;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 10px;
    transition: all 0.3s ease;
    border-left: 4px solid #667eea;

    &:hover {
      transform: translateX(8px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }

    h4 {
      margin: 0 0 8px 0;
      font-size: 17px;
      font-weight: 600;
      color: #2c3e50;
      display: flex;
      align-items: center;

      i {
        margin-right: 8px;
        color: #667eea;
        font-size: 18px;
      }
    }

    p {
      margin: 0;
      font-size: 15px;
      color: #4a4a4a;
      line-height: 1.8;
      text-indent: 0;
    }
  }
}

/* 院系设置表格样式 */
.department-card {
  ::v-deep .el-table {
    font-size: 15px;
    border-radius: 8px;
    overflow: hidden;

    th {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: #fff;
      font-weight: 600;
      font-size: 16px;
      letter-spacing: 1px;
    }

    td {
      font-size: 15px;
      color: #4a4a4a;
    }

    .el-table__row:hover > td {
      background: #f5f7fa;
    }
  }
}

/* 联系方式样式 */
.contact-card {
  ::v-deep .el-descriptions {
    font-size: 15px;

    .el-descriptions-item__label {
      font-weight: 600;
      color: #2c3e50;
      font-size: 15px;
    }

    .el-descriptions-item__content {
      color: #4a4a4a;
      font-size: 15px;
    }

    a {
      color: #667eea;
      text-decoration: none;
      transition: all 0.3s ease;

      &:hover {
        color: #764ba2;
        text-decoration: underline;
      }
    }
  }
}
body.theme-dark .card-header {
  color: #e0e0e0 !important;
}

body.theme-dark .card-content {
  color: #c0c0c0 !important;
}

body.theme-dark .culture-item {
  background: #0f3460 !important;
}

body.theme-dark .culture-item h4 {
  color: #e0e0e0 !important;
}

body.theme-dark .culture-item .desc {
  color: #808080 !important;
}
</style>

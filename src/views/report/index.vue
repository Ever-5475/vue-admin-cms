<template>
  <div class="app-container">
    <div class="report-header">
      <h2 class="report-title">综合数据报表</h2>
      <span class="report-subtitle">全站核心指标一览</span>
    </div>

    <el-row :gutter="20" v-loading="loading" class="stat-cards">
      <el-col :span="6" v-for="card in overviewCards" :key="card.label">
        <div class="stat-card" :class="card.type" @click="handleCardClick(card)">
          <div class="stat-icon">
            <i :class="card.icon"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatNumber(card.value) }}</div>
            <div class="stat-label">{{ card.label }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 可视化图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title">
            <i class="el-icon-document"></i> 文章状态分布
          </div>
          <div class="chart-body">
            <div ref="articleStatusChart" class="echart-container"></div>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title">
            <i class="el-icon-chat-line-round"></i> 评论状态分布
          </div>
          <div class="chart-body">
            <div ref="commentStatusChart" class="echart-container"></div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title">
            <i class="el-icon-view"></i> 热门文章 TOP 10（按浏览量）
          </div>
          <div class="chart-body">
            <div ref="topArticlesChart" class="echart-container"></div>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title">
            <i class="el-icon-user-solid"></i> 作者文章数排行 TOP 10
          </div>
          <div class="chart-body">
            <div ref="authorRankingChart" class="echart-container"></div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 传统表格备用 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title">
            <i class="el-icon-document"></i> 文章状态分布（表格）
          </div>
          <div class="chart-body">
            <table class="dist-table">
              <thead><tr><th>状态</th><th>数量</th><th>占比</th></tr></thead>
              <tbody>
                <tr v-for="item in articleStatusList" :key="item.status">
                  <td><el-tag :type="getTagType(item.status)" size="small">{{ getStatusLabel(item.status) }}</el-tag></td>
                  <td>{{ item.count }}</td>
                  <td>
                    <el-progress :percentage="getPercent(item.count, totalArticles)" :show-text="false" :stroke-width="8" />
                    <span class="percent-text">{{ getPercent(item.count, totalArticles) }}%</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title">
            <i class="el-icon-chat-line-round"></i> 评论状态分布（表格）
          </div>
          <div class="chart-body">
            <table class="dist-table">
              <thead><tr><th>状态</th><th>数量</th><th>占比</th></tr></thead>
              <tbody>
                <tr v-for="item in commentStatusList" :key="item.status">
                  <td><el-tag :type="getCommentTagType(item.status)" size="small">{{ getCommentStatusLabel(item.status) }}</el-tag></td>
                  <td>{{ item.count }}</td>
                  <td>
                    <el-progress :percentage="getPercent(item.count, totalComments)" :show-text="false" :stroke-width="8" />
                    <span class="percent-text">{{ getPercent(item.count, totalComments) }}%</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getReportOverview } from '@/api/report'
import * as echarts from 'echarts'

export default {
  name: 'ReportIndex',
  data() {
    return {
      loading: false,
      reportData: {},
      overviewCards: [],
      articleStatusList: [],
      commentStatusList: [],
      topArticles: [],
      authorRanking: [],
      articleStatusChart: null,
      commentStatusChart: null,
      topArticlesChart: null,
      authorRankingChart: null
    }
  },
  computed: {
    totalArticles() { return this.articleStatusList.reduce((s, i) => s + i.count, 0) || 1 },
    totalComments() { return this.commentStatusList.reduce((s, i) => s + i.count, 0) || 1 }
  },
  created() { this.fetchData() },
  mounted() {
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    this.disposeCharts()
  },
  methods: {
    fetchData: function () {
      var self = this
      self.loading = true
      getReportOverview().then(function (res) {
        if (res && res.code === 20000) {
          self.reportData = res.data || {}
          self.overviewCards = [
            { label: '用户总数', value: res.data.users_count, icon: 'el-icon-user-solid', type: 'primary', path: '/user/list' },
            { label: '文章总数', value: res.data.articles_count, icon: 'el-icon-document', type: 'success', path: '/article/list' },
            { label: '已发布', value: res.data.published_count, icon: 'el-icon-document-checked', type: 'success', path: '/report/article' },
            { label: '草稿数', value: res.data.draft_count, icon: 'el-icon-edit-outline', type: 'warning', path: '/report/article' },
            { label: '评论总数', value: res.data.comments_count, icon: 'el-icon-chat-line-round', type: 'info', path: '/report/comment' },
            { label: '待审核', value: res.data.comments_pending, icon: 'el-icon-warning-outline', type: 'danger', path: '/report/comment' },
            { label: '已通过', value: res.data.comments_approved, icon: 'el-icon-circle-check', type: 'success', path: '/report/comment' },
            { label: '总浏览量', value: res.data.pageviews_total, icon: 'el-icon-view', type: 'primary', path: '/report/article' }
          ]
          self.articleStatusList = res.data.status_dist || []
          self.commentStatusList = res.data.comment_status_dist || []
          self.topArticles = res.data.top_articles || []
          self.authorRanking = res.data.author_ranking || []
          
          // 数据加载完成后渲染图表
          self.$nextTick(function() {
            self.initCharts()
          })
        }
      }).catch(function () {
        self.$message.error('获取报表数据失败')
      }).then(function () {
        self.loading = false
      })
    },
    handleCardClick: function (card) {
      if (card.path) this.$router.push(card.path)
    },
    formatNumber: function (n) {
      if (n === null || n === undefined || n === '') return 0
      return Number(n).toLocaleString()
    },
    getPercent: function (val, total) {
      if (!total || total === 0) return '0'
      return ((val / total) * 100).toFixed(1)
    },
    getStatusLabel: function (status) {
      var map = { published: '已发布', draft: '草稿', deleted: '已删除' }
      return map[status] || status
    },
    getTagType: function (status) {
      var map = { published: 'success', draft: 'warning', deleted: 'danger' }
      return map[status] || 'info'
    },
    getCommentStatusLabel: function (status) {
      var map = { approved: '已通过', pending: '待审核', rejected: '已拒绝' }
      return map[status] || status
    },
    getCommentTagType: function (status) {
      var map = { approved: 'success', pending: 'warning', rejected: 'danger' }
      return map[status] || 'info'
    },
    handleResize() {
      this.articleStatusChart && this.articleStatusChart.resize()
      this.commentStatusChart && this.commentStatusChart.resize()
      this.topArticlesChart && this.topArticlesChart.resize()
      this.authorRankingChart && this.authorRankingChart.resize()
    },
    disposeCharts() {
      this.articleStatusChart && this.articleStatusChart.dispose()
      this.commentStatusChart && this.commentStatusChart.dispose()
      this.topArticlesChart && this.topArticlesChart.dispose()
      this.authorRankingChart && this.authorRankingChart.dispose()
    },
    initCharts() {
      this.initArticleStatusChart()
      this.initCommentStatusChart()
      this.initTopArticlesChart()
      this.initAuthorRankingChart()
    },
    initArticleStatusChart() {
      if (!this.$refs.articleStatusChart) return
      this.articleStatusChart = echarts.init(this.$refs.articleStatusChart)
      
      const data = this.articleStatusList.map(item => ({
        name: this.getStatusLabel(item.status),
        value: item.count
      }))
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'middle'
        },
        series: [
          {
            name: '文章状态',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 20,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: data,
            color: ['#67c23a', '#e6a23c', '#f56c6c']
          }
        ]
      }
      
      this.articleStatusChart.setOption(option)
    },
    initCommentStatusChart() {
      if (!this.$refs.commentStatusChart) return
      this.commentStatusChart = echarts.init(this.$refs.commentStatusChart)
      
      const data = this.commentStatusList.map(item => ({
        name: this.getCommentStatusLabel(item.status),
        value: item.count
      }))
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'middle'
        },
        series: [
          {
            name: '评论状态',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 20,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: data,
            color: ['#67c23a', '#e6a23c', '#f56c6c']
          }
        ]
      }
      
      this.commentStatusChart.setOption(option)
    },
    initTopArticlesChart() {
      if (!this.$refs.topArticlesChart) return
      this.topArticlesChart = echarts.init(this.$refs.topArticlesChart)
      
      const titles = this.topArticles.map(item => {
        const title = item.title || '无标题'
        return title.length > 15 ? title.substring(0, 15) + '...' : title
      }).reverse()
      const views = this.topArticles.map(item => item.pageviews).reverse()
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            return params[0].name + '<br/>浏览量: ' + params[0].value.toLocaleString()
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '浏览量'
        },
        yAxis: {
          type: 'category',
          data: titles,
          axisLabel: {
            interval: 0,
            fontSize: 12
          }
        },
        series: [
          {
            name: '浏览量',
            type: 'bar',
            data: views,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#83bff6' },
                { offset: 0.5, color: '#188df0' },
                { offset: 1, color: '#188df0' }
              ])
            },
            emphasis: {
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#2378f7' },
                  { offset: 0.7, color: '#2378f7' },
                  { offset: 1, color: '#83bff6' }
                ])
              }
            },
            barWidth: '60%'
          }
        ]
      }
      
      this.topArticlesChart.setOption(option)
    },
    initAuthorRankingChart() {
      if (!this.$refs.authorRankingChart) return
      this.authorRankingChart = echarts.init(this.$refs.authorRankingChart)
      
      const names = this.authorRanking.map(item => item.name).reverse()
      const counts = this.authorRanking.map(item => item.count).reverse()
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '文章数'
        },
        yAxis: {
          type: 'category',
          data: names,
          axisLabel: {
            interval: 0,
            fontSize: 12
          }
        },
        series: [
          {
            name: '文章数',
            type: 'bar',
            data: counts,
            itemStyle: {
              color: function(params) {
                const colorList = ['#f56c6c', '#e6a23c', '#67c23a', '#409eff', '#909399']
                const index = counts.length - 1 - params.dataIndex
                if (index === 0) return '#f56c6c'
                if (index === 1) return '#e6a23c'
                if (index === 2) return '#67c23a'
                return '#409eff'
              }
            },
            barWidth: '60%'
          }
        ]
      }
      
      this.authorRankingChart.setOption(option)
    }
  }
}
</script>

<style scoped>
.report-header { padding: 20px 0; text-align: center; margin-bottom: 10px; }
.report-title { margin: 0; font-size: 24px; color: #303133; }
.report-subtitle { color: #909399; font-size: 14px; margin-left: 10px; }
.stat-cards { margin-bottom: 20px; }
.stat-card {
  background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px;
  display: flex; align-items: center; cursor: pointer; transition: all 0.2s;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.12); }
.stat-card .stat-icon {
  width: 56px; height: 56px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px; margin-right: 16px; color: white;
}
.stat-card.primary .stat-icon { background: #409eff; }
.stat-card.success .stat-icon { background: #67c23a; }
.stat-card.warning .stat-icon { background: #e6a23c; }
.stat-card.danger .stat-icon { background: #f56c6c; }
.stat-card.info .stat-icon { background: #909399; }
.stat-value { font-size: 28px; font-weight: bold; color: #303133; line-height: 1.2; }
.stat-label { color: #909399; font-size: 14px; margin-top: 4px; }
.chart-row { margin-bottom: 20px; }
.chart-card { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08); height: 100%; }
.chart-title { font-size: 16px; font-weight: bold; color: #303133; padding-bottom: 15px; border-bottom: 1px solid #ebeef5; margin-bottom: 15px; }
.chart-body { min-height: 260px; }
.echart-container { width: 100%; height: 300px; }
.dist-table { width: 100%; border-collapse: collapse; }
.dist-table th { background: #f5f7fa; padding: 10px; text-align: left; font-weight: 600; color: #606266; }
.dist-table td { padding: 12px 10px; border-bottom: 1px solid #ebeef5; color: #303133; }
.dist-table tr:last-child td { border-bottom: none; }
.percent-text { display: inline-block; margin-left: 8px; font-size: 12px; color: #909399; }
</style>

<style lang="scss">
/* 深色模式适配（非scoped，确保全局生效） */
body.theme-dark .report-title { color: #e0e0e0 !important; }
body.theme-dark .report-subtitle { color: #808080 !important; }
body.theme-dark .stat-card { background: #16213e !important; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.3) !important; }
body.theme-dark .stat-card:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important; }
body.theme-dark .stat-value { color: #e0e0e0 !important; }
body.theme-dark .stat-label { color: #808080 !important; }
body.theme-dark .chart-card { background: #16213e !important; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.3) !important; }
body.theme-dark .chart-title { color: #e0e0e0 !important; border-bottom: 1px solid #0f3460 !important; }
body.theme-dark .dist-table th { background: #0f3460 !important; color: #e0e0e0 !important; }
body.theme-dark .dist-table td { border-bottom: 1px solid #0f3460 !important; color: #c0c0c0 !important; }
body.theme-dark .percent-text { color: #808080 !important; }
</style>

<template>
  <div class="app-container">
    <div class="report-header">
      <h2 class="report-title">评论数据报表</h2>
      <div class="filter-bar">
        <span>最近</span>
        <el-select v-model="days" size="small" style="width:100px; margin:0 10px;">
          <el-option :value="7" label="7 天"></el-option>
          <el-option :value="30" label="30 天"></el-option>
          <el-option :value="90" label="90 天"></el-option>
        </el-select>
        <el-button size="small" type="primary" @click="fetchData">刷新</el-button>
      </div>
    </div>

    <el-row :gutter="20" v-loading="loading" class="stat-cards">
      <el-col :span="6">
        <div class="stat-card primary">
          <div class="stat-icon"><i class="el-icon-chat-line-round"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ formatNumber(reportData.comments_count || 0) }}</div>
            <div class="stat-label">评论总数</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card success">
          <div class="stat-icon"><i class="el-icon-circle-check"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ formatNumber(reportData.comments_approved || 0) }}</div>
            <div class="stat-label">已通过</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card warning">
          <div class="stat-icon"><i class="el-icon-warning-outline"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ formatNumber(reportData.comments_pending || 0) }}</div>
            <div class="stat-label">待审核</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card info">
          <div class="stat-icon"><i class="el-icon-circle-close"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ formatNumber(reportData.comments_rejected || 0) }}</div>
            <div class="stat-label">已拒绝</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title"><i class="el-icon-data-line"></i> 评论发布趋势（最近 {{ days }} 天）</div>
          <div class="chart-body">
            <table class="trend-table">
              <thead><tr><th>日期</th><th>新增评论</th></tr></thead>
              <tbody>
                <tr v-for="(item, idx) in commentTrend" :key="idx">
                  <td>{{ formatDate(item.date) }}</td>
                  <td>
                    <el-progress :percentage="getTrendPercent(item.count)" :show-text="false" :stroke-width="8" />
                    <span class="percent-text">{{ item.count }} 条</span>
                  </td>
                </tr>
                <tr v-if="!commentTrend.length"><td colspan="2" style="text-align:center; color:#909399;">暂无数据</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title"><i class="el-icon-s-data"></i> 评论状态分布</div>
          <div class="chart-body">
            <table class="dist-table">
              <thead><tr><th>状态</th><th>数量</th><th>占比</th></tr></thead>
              <tbody>
                <tr v-for="item in statusDist" :key="item.status">
                  <td><el-tag :type="getTagType(item.status)" size="small">{{ getStatusLabel(item.status) }}</el-tag></td>
                  <td>{{ item.count }}</td>
                  <td>
                    <el-progress :percentage="getPercent(item.count, totalComments)" :show-text="false" :stroke-width="8" />
                    <span class="percent-text">{{ getPercent(item.count, totalComments) }}%</span>
                  </td>
                </tr>
                <tr v-if="!statusDist.length"><td colspan="3" style="text-align:center; color:#909399;">暂无数据</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title"><i class="el-icon-s-order"></i> 评论最多的文章 TOP 10</div>
          <div class="chart-body">
            <el-table :data="topCommented" size="small" border stripe>
              <el-table-column type="index" label="排名" width="60" align="center"></el-table-column>
              <el-table-column prop="title" label="文章标题" show-overflow-tooltip min-width="160"></el-table-column>
              <el-table-column prop="author" label="作者" width="90" align="center"></el-table-column>
              <el-table-column prop="comment_count" label="评论数" width="100" align="center" sortable>
                <template slot-scope="scope"><el-tag size="mini" :type="scope.$index < 3 ? 'success' : 'info'">{{ scope.row.comment_count }}</el-tag></template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-title"><i class="el-icon-time"></i> 最近 50 条评论</div>
          <div class="chart-body">
            <el-table :data="recentComments" size="small" border stripe max-height="350">
              <el-table-column prop="username" label="用户" width="100"></el-table-column>
              <el-table-column prop="content" label="内容" show-overflow-tooltip min-width="140"></el-table-column>
              <el-table-column prop="status" label="状态" width="80" align="center">
                <template slot-scope="scope"><el-tag :type="getTagType(scope.row.status)" size="mini">{{ getStatusLabel(scope.row.status) }}</el-tag></template>
              </el-table-column>
              <el-table-column prop="article_title" label="所属文章" show-overflow-tooltip min-width="130"></el-table-column>
              <el-table-column prop="created_at" label="时间" width="150" align="center">
                <template slot-scope="scope">{{ formatDate(scope.row.created_at) }}</template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getReportComment } from '@/api/report'

export default {
  name: 'ReportComment',
  data() {
    return {
      loading: false,
      days: 30,
      reportData: {},
      commentTrend: [],
      statusDist: [],
      topCommented: [],
      recentComments: []
    }
  },
  computed: { totalComments() { return this.statusDist.reduce((s, i) => s + i.count, 0) || 1 } },
  created() { this.fetchData() },
  methods: {
    fetchData: function () {
      var self = this
      self.loading = true
      getReportComment(self.days).then(function (res) {
        if (res && res.code === 20000) {
          self.reportData = res.data || {}
          self.commentTrend = res.data.comment_trend || []
          self.statusDist = res.data.status_dist || []
          self.topCommented = res.data.top_commented || []
          self.recentComments = res.data.recent_comments || []
          var pendingItem = self.statusDist.filter(function (s) { return s.status === 'pending' })[0]
          var approvedItem = self.statusDist.filter(function (s) { return s.status === 'approved' })[0]
          var pending = pendingItem ? pendingItem.count : 0
          var approved = approvedItem ? approvedItem.count : 0
          self.$set(self.reportData, 'comments_rejected', self.reportData.comments_count - pending - approved)
        }
      }).catch(function () {
        self.$message.error('获取评论报表失败')
      }).then(function () {
        self.loading = false
      })
    },
    formatNumber: function (n) {
      if (n === null || n === undefined || n === '') return 0
      return Number(n).toLocaleString()
    },
    getPercent: function (val, total) {
      if (!total || total === 0) return '0'
      return ((val / total) * 100).toFixed(1)
    },
    getTrendPercent: function (count) {
      var values = this.commentTrend.map(function (i) { return i.count })
      values.push(1)
      var max = Math.max.apply(null, values)
      return Math.round((count / max) * 100)
    },
    getStatusLabel: function (status) {
      var map = { approved: '已通过', pending: '待审核', rejected: '已拒绝' }
      return map[status] || status
    },
    getTagType: function (status) {
      var map = { approved: 'success', pending: 'warning', rejected: 'danger' }
      return map[status] || 'info'
    },
    formatDate: function (dateStr) {
      if (!dateStr) return ''
      var s = String(dateStr)
      // 如果是 YYYY-MM-DD 格式（只有日期没有时间）
      if (/^\d{4}-\d{2}-\d{2}$/.test(s)) {
        var parts = s.split('-')
        return parseInt(parts[0]) + '年' + parseInt(parts[1]) + '月' + parseInt(parts[2]) + '日'
      }
      var d = new Date(s.replace(/-/g, '/'))
      if (isNaN(d.getTime())) return s
      var pad = function(n) { return String(n).padStart(2, '0') }
      return d.getFullYear() + '年' + pad(d.getMonth()+1) + '月' + pad(d.getDate()) + '日 ' + pad(d.getHours()) + ':' + pad(d.getMinutes())
    }
  }
}
</script>

<style scoped>
.report-header { padding: 15px 0; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.report-title { margin: 0; font-size: 20px; color: #303133; }
.filter-bar { display: flex; align-items: center; color: #606266; font-size: 13px; }
.stat-cards { margin-bottom: 20px; }
.stat-card { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; display: flex; align-items: center; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08); min-height: 100px; }
.stat-icon { width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 26px; margin-right: 16px; color: white; }
.stat-card.primary .stat-icon { background: #409eff; }
.stat-card.success .stat-icon { background: #67c23a; }
.stat-card.warning .stat-icon { background: #e6a23c; }
.stat-card.info .stat-icon { background: #909399; }
.stat-value { font-size: 26px; font-weight: bold; color: #303133; line-height: 1.2; }
.stat-label { color: #909399; font-size: 13px; margin-top: 4px; }
.chart-row { margin-bottom: 20px; }
.chart-card { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08); height: 100%; min-height: 450px; display: flex; flex-direction: column; }
.chart-title { font-size: 15px; font-weight: bold; color: #303133; padding-bottom: 15px; border-bottom: 1px solid #ebeef5; margin-bottom: 15px; flex-shrink: 0; }
.chart-body { flex: 1; min-height: 260px; max-height: 400px; overflow-y: auto; }
.trend-table, .dist-table { width: 100%; border-collapse: collapse; }
.trend-table th, .dist-table th { background: #f5f7fa; padding: 10px; text-align: left; font-weight: 600; color: #606266; }
.trend-table td, .dist-table td { padding: 12px 10px; border-bottom: 1px solid #ebeef5; }
.trend-table tr:last-child td, .dist-table tr:last-child td { border-bottom: none; }
.percent-text { display: inline-block; margin-left: 8px; font-size: 12px; color: #909399; }

/* 深色模式适配 */
body.theme-dark .report-title { color: #e0e0e0 !important; }
body.theme-dark .filter-bar { color: #c0c0c0 !important; }
body.theme-dark .stat-card { background: #16213e !important; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.3) !important; }
body.theme-dark .stat-value { color: #e0e0e0 !important; }
body.theme-dark .stat-label { color: #808080 !important; }
body.theme-dark .chart-card { background: #16213e !important; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.3) !important; }
body.theme-dark .chart-title { color: #e0e0e0 !important; border-bottom: 1px solid #0f3460 !important; }
body.theme-dark .trend-table th, body.theme-dark .dist-table th { background: #0f3460 !important; color: #e0e0e0 !important; }
body.theme-dark .trend-table td, body.theme-dark .dist-table td { border-bottom: 1px solid #0f3460 !important; color: #c0c0c0 !important; }
body.theme-dark .percent-text { color: #808080 !important; }

</style>

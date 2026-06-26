<template>
  <div class="article-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1><i class="el-icon-document"></i> 文章管理</h1>
        <p>管理和维护您的所有文章内容</p>
      </div>
      <el-button type="primary" icon="el-icon-plus" round @click="$router.push('/article/create')">
        发布新文章
      </el-button>
    </div>

    <!-- 筛选区域 -->
    <el-card shadow="hover" class="filter-card">
      <div class="filter-wrapper">
        <div class="filter-left">
          <el-input
            v-model="listQuery.title"
            placeholder="🔍 搜索文章标题..."
            prefix-icon="el-icon-search"
            clearable
            class="search-input"
            @keyup.enter.native="handleFilter"
            @clear="handleFilter">
          </el-input>

          <el-select v-model="listQuery.status" placeholder="文章状态" clearable class="status-select">
            <el-option label="✨ 已发布" value="published">
              <span style="display: flex; align-items: center; gap: 8px;">
                <el-tag type="success" size="mini">已发布</el-tag>
              </span>
            </el-option>
            <el-option label="📝 草稿" value="draft">
              <span style="display: flex; align-items: center; gap: 8px;">
                <el-tag type="warning" size="mini">草稿</el-tag>
              </span>
            </el-option>
            <el-option label="🗑️ 已删除" value="deleted">
              <span style="display: flex; align-items: center; gap: 8px;">
                <el-tag type="danger" size="mini">已删除</el-tag>
              </span>
            </el-option>
          </el-select>
        </div>

        <div class="filter-right">
          <el-button icon="el-icon-refresh" @click="handleFilter" circle></el-button>
          <el-button type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
          <el-dropdown @command="handleExport" trigger="click">
            <el-button type="success" icon="el-icon-download">
              导出<i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="csv"><i class="el-icon-document"></i> 导出 CSV</el-dropdown-item>
              <el-dropdown-item command="excel"><i class="el-icon-tickets"></i> 导出 Excel</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <el-button type="success" icon="el-icon-plus" @click="$router.push('/article/create')">发布文章</el-button>
        </div>
      </div>
    </el-card>

    <!-- 文章列表 -->
    <el-card shadow="hover" class="table-card">
      <el-table
        v-loading="listLoading"
        :data="list"
        border
        stripe
        highlight-current-row
        style="width: 100%"
        :header-cell-style="headerCellStyle"
        :row-class-name="tableRowClassName">

        <el-table-column align="center" label="ID" width="70">
          <template slot-scope="scope">
            <el-tag type="info" effect="plain" round>{{ scope.row.id }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="文章标题" min-width="220" show-overflow-tooltip>
          <template slot-scope="scope">
            <div class="title-cell">
              <i class="el-icon-document" title-color="#409eff"></i>
              <span class="title-text">{{ scope.row.title }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column align="center" label="作者" width="120">
          <template slot-scope="scope">
            <div class="author-cell">
              <el-avatar :size="28" :src="scope.row.avatar || ''" style="background: linear-gradient(135deg, #667eea, #764ba2); font-size: 12px;">{{ (scope.row.author || '').charAt(0) }}</el-avatar>
              <span>{{ scope.row.author }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column align="center" label="浏览量" width="100" sortable prop="pageviews">
          <template slot-scope="scope">
            <div class="stat-cell">
              <i class="el-icon-view"></i>
              <span>{{ formatNumber(scope.row.pageviews) }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column align="center" label="状态" width="110">
          <template slot-scope="scope">
            <el-tag :type="statusType(scope.row.status)" effect="dark" round>
              <i :class="statusIcon(scope.row.status)" style="margin-right: 4px;"></i>
              {{ statusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column align="center" label="发布时间" width="170" sortable>
          <template slot-scope="scope">
            <div class="time-cell">
              <i class="el-icon-time" style="color: #909399; margin-right: 6px;"></i>
              <span>{{ scope.row.display_time | formatDate }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column align="center" label="操作" width="240" fixed="right">
          <template slot-scope="scope">
            <div class="action-buttons">
              <el-tooltip content="阅读全文" placement="top">
                <el-button type="primary" size="mini" icon="el-icon-document" circle @click="$router.push(`/article/detail/${scope.row.id}`)"></el-button>
              </el-tooltip>
              <el-tooltip v-if="canEdit(scope.row)" content="编辑文章" placement="top">
                <el-button type="warning" size="mini" icon="el-icon-edit" circle @click="$router.push(`/article/edit/${scope.row.id}`)"></el-button>
              </el-tooltip>
              <el-tooltip v-if="canEdit(scope.row)" content="删除文章" placement="top">
                <el-button type="danger" size="mini" icon="el-icon-delete" circle @click="handleDelete(scope.row.id)"></el-button>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList"
        layout="total, sizes, prev, pager, next, jumper">
      </pagination>
    </el-card>
  </div>
</template>

<script>
import { getArticleList, deleteArticle } from '@/api/article'
import Pagination from '@/components/Pagination'
import { mapGetters } from 'vuex'
import * as XLSX from 'xlsx'

export default {
  name: 'ArticleList',
  components: { Pagination },
  computed: {
    ...mapGetters(['name', 'isAdmin']),
    headerCellStyle() {
      const isDark = document.body.classList.contains('theme-dark')
      return {
        background: isDark ? '#0f3460' : '#fafafa',
        color: isDark ? '#e0e0e0' : '#606266',
        fontWeight: '600'
      }
    }
  },
  filters: {
    formatDate(time) {
      if (!time) return ''
      const date = new Date(time)
      return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')} ${String(date.getHours()).padStart(2,'0')}:${String(date.getMinutes()).padStart(2,'0')}`
    }
  },
  data() {
    return {
      list: [],
      total: 0,
      listLoading: true,
      listQuery: { page: 1, limit: 10, title: '', status: '' }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getArticleList(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    canEdit(row) {
      // 管理员或文章作者可以编辑/删除
      if (this.isAdmin) return true
      if (!row || !row.author) return false
      return this.name && String(this.name) === String(row.author)
    },
    handleView(row) {
      this.$router.push(`/article/detail/${row.id}`)
    },
    handleDelete(id) {
      this.$confirm('确认删除该文章？此操作不可恢复！', '⚠️ 危险操作', {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        deleteArticle(id).then(() => {
          this.$message.success('🗑️ 删除成功')
          this.getList()
        })
      }).catch(() => {})
    },
    tableRowClassName({ row, rowIndex }) {
      if (rowIndex % 2 === 1) {
        return 'success-row'
      }
      return ''
    },
    statusType(status) {
      const map = { published: 'success', draft: 'warning', deleted: 'danger' }
      return map[status] || 'info'
    },
    statusIcon(status) {
      const map = { published: 'el-icon-check', draft: 'el-icon-edit-outline', deleted: 'el-icon-delete' }
      return map[status] || 'el-icon-info'
    },
    statusText(status) {
      const map = { published: '已发布', draft: '草稿', deleted: '已删除' }
      return map[status] || status
    },
    formatNumber(num) {
      if (!num) return '0'
      if (num >= 10000) {
        return (num / 10000).toFixed(1) + 'w'
      }
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k'
      }
      return num.toString()
    },
    handleExport(format) {
      var self = this
      var loading = self.$loading({ lock: true, text: '正在导出...', spinner: 'el-icon-loading' })
      // 获取当前筛选条件下的所有文章
      var params = Object.assign({}, self.listQuery, { page: 1, limit: 10000 })
      getArticleList(params).then(function(response) {
        var items = response.data.items || []
        if (!items.length) {
          loading.close()
          self.$message.warning('暂无数据可导出')
          return
        }
        if (format === 'csv') {
          self.exportToCSV(items, loading)
        } else if (format === 'excel') {
          self.exportToExcel(items, loading)
        }
      }).catch(function() {
        loading.close()
      })
    },
    exportToCSV(items, loading) {
      // 构建 CSV 内容
      var BOM = '\uFEFF'
      var headers = ['ID', '标题', '作者', '状态', '浏览量', '发布时间']
      var rows = [headers.join(',')]
      items.forEach(function(item) {
        var statusMap = { published: '已发布', draft: '草稿', deleted: '已删除' }
        var row = [
          item.id || '',
          '"' + String(item.title || '').replace(/"/g, '""') + '"',
          item.author || '',
          statusMap[item.status] || item.status || '',
          item.pageviews || 0,
          item.display_time || ''
        ]
        rows.push(row.join(','))
      })
      var csvContent = BOM + rows.join('\n')
      var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      var link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = '文章列表_' + new Date().getTime() + '.csv'
      link.click()
      URL.revokeObjectURL(link.href)
      loading.close()
      this.$message.success('导出 CSV 成功，共 ' + items.length + ' 条数据')
    },
    exportToExcel(items, loading) {
      // 准备数据
      var statusMap = { published: '已发布', draft: '草稿', deleted: '已删除' }
      var data = items.map(function(item) {
        return {
          'ID': item.id || '',
          '标题': item.title || '',
          '作者': item.author || '',
          '状态': statusMap[item.status] || item.status || '',
          '浏览量': item.pageviews || 0,
          '发布时间': item.display_time || ''
        }
      })
      // 创建工作簿
      var ws = XLSX.utils.json_to_sheet(data)
      var wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, '文章列表')
      // 导出文件
      XLSX.writeFile(wb, '文章列表_' + new Date().getTime() + '.xlsx')
      loading.close()
      this.$message.success('导出 Excel 成功，共 ' + items.length + ' 条数据')
    }
  }
}
</script>

<style lang="scss" scoped>
.article-container {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: calc(100vh - 84px);

  // 深色模式适配
  body.theme-dark & {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  }

  // 页面头部
  .page-header {
    background: white;
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    animation: slideInDown 0.6s ease-out;

    body.theme-dark & {
      background: #16213e;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .header-content {
      h1 {
        margin: 0 0 8px 0;
        font-size: 26px;
        color: #303133;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;

        body.theme-dark & {
          color: #e0e0e0;
        }

        i {
          color: #409eff;
          font-size: 28px;
        }
      }

      p {
        margin: 0;
        color: #909399;
        font-size: 14px;

        body.theme-dark & {
          color: #808080;
        }
      }
    }

    .el-button {
      border-radius: 25px;
      padding: 12px 30px;
      font-weight: 600;
      box-shadow: 0 4px 15px rgba(64, 158, 255, 0.3);
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(64, 158, 255, 0.4);
      }
    }
  }

  // 筛选卡片
  .filter-card {
    border-radius: 16px;
    border: none;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    animation: fadeInUp 0.6s ease-out 0.1s both;

    body.theme-dark & {
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    ::v-deep .el-card__body {
      padding: 20px;
    }

    .filter-wrapper {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 15px;
      flex-wrap: wrap;

      .filter-left {
        display: flex;
        gap: 12px;
        flex: 1;
        min-width: 300px;

        .search-input {
          width: 320px;

          ::v-deep .el-input__inner {
            border-radius: 25px;
            height: 40px;
            line-height: 40px;
            border: 2px solid #dcdfe6;
            transition: all 0.3s ease;

            body.theme-dark & {
              border: 2px solid #1a1a2e;
            }

            &:focus {
              border-color: #409eff;
              box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.1);
            }
          }
        }

        .status-select {
          width: 160px;

          ::v-deep .el-input__inner {
            border-radius: 25px;
            height: 40px;
          }
        }
      }

      .filter-right {
        display: flex;
        gap: 10px;

        .el-button {
          border-radius: 25px;
          padding: 10px 20px;
          transition: all 0.3s ease;

          &:hover {
            transform: translateY(-2px);
          }

          &.is-circle {
            width: 40px;
            height: 40px;
            padding: 0;
          }
        }
      }
    }
  }

  // 表格卡片
  .table-card {
    border-radius: 16px;
    border: none;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    animation: fadeInUp 0.6s ease-out 0.2s both;

    body.theme-dark & {
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    ::v-deep .el-card__body {
      padding: 24px;
    }

    // 表格样式优化
    .el-table {
      border-radius: 12px;
      overflow: hidden;

      &::before {
        display: none;
      }

      th {
        background: #fafafa !important;
        color: #606266 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;

        body.theme-dark & {
          background: #0f3460 !important;
          color: #e0e0e0 !important;
        }
      }

      td {
        padding: 16px 0 !important;
      }

      tr {
        transition: all 0.3s ease;

        &:hover {
          background-color: #ecf5ff !important;
          transform: scale(1.01);
          box-shadow: 0 2px 12px rgba(64, 158, 255, 0.1);

          body.theme-dark & {
            background-color: #1a1a3e !important;
            box-shadow: 0 2px 12px rgba(64, 158, 255, 0.2);
          }
        }

        &.success-row {
          background-color: #fafafa;

          body.theme-dark & {
            background-color: #16213e;
          }
        }
      }
    }

    // 单元格内容样式
    .title-cell {
      display: flex;
      align-items: center;
      gap: 10px;

      i {
        color: #409eff;
        font-size: 18px;
      }

      .title-text {
        font-weight: 500;
        color: #303133;
        cursor: pointer;
        transition: color 0.3s ease;

        body.theme-dark & {
          color: #e0e0e0;
        }

        &:hover {
          color: #409eff;
        }
      }
    }

    .author-cell {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;

      span {
        font-weight: 500;
        color: #606266;

        body.theme-dark & {
          color: #c0c0c0;
        }
      }
    }

    .stat-cell {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: #909399;
      font-weight: 500;

      body.theme-dark & {
        color: #808080;
      }

      i {
        font-size: 14px;
      }

      span {
        color: #303133;

        body.theme-dark & {
          color: #e0e0e0;
        }
      }
    }

    .time-cell {
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      color: #606266;

      body.theme-dark & {
        color: #c0c0c0;
      }
    }

    // 操作按钮组
    .action-buttons {
      display: flex;
      justify-content: center;
      gap: 8px;

      .el-button {
        margin: 0 !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);

        &:hover {
          transform: scale(1.15) rotate(5deg);
        }
      }
    }

    // 分页样式
    .pagination-container {
      margin-top: 24px;
      padding-top: 20px;
      border-top: 1px solid #ebeef5;

      body.theme-dark & {
        border-top: 1px solid #0f3460;
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

// 响应式设计
@media screen and (max-width: 992px) {
  .article-container {
    .page-header {
      flex-direction: column;
      text-align: center;
      gap: 20px;
    }

    .filter-wrapper {
      flex-direction: column;

      .filter-left,
      .filter-right {
        width: 100%;
        justify-content: center;
      }
    }
  }
}
</style>

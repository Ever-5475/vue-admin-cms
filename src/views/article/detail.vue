<template>
  <div class="detail-container">
    <!-- 返回 & 操作栏 -->
    <div class="detail-toolbar">
      <el-button icon="el-icon-arrow-left" round @click="$router.push('/article/list')">返回列表</el-button>
      <div class="right-actions">
        <el-tag v-if="article.status === 'published'" type="success" effect="dark">已发布</el-tag>
        <el-tag v-else-if="article.status === 'draft'" type="warning">草稿</el-tag>
        <el-tag v-else type="danger">{{ article.status }}</el-tag>
        <el-button type="primary" icon="el-icon-edit" round @click="$router.push(`/article/edit/${routeId}`)">编辑文章</el-button>
      </div>
    </div>

    <!-- 文章正文卡片 -->
    <el-card shadow="hover" v-loading="loading" class="article-card">
      <template v-if="!loading && article.title">
        <div class="article-header">
          <h1 class="article-title">{{ article.title }}</h1>
          <div class="article-meta">
            <el-avatar :size="36" :src="''" style="background:linear-gradient(135deg,#667eea,#764ba2);font-size:14px;">{{ (article.author || '').charAt(0) }}</el-avatar>
            <div class="meta-text">
              <div class="author-name">{{ article.author }}</div>
              <div class="meta-sub">
                <span><i class="el-icon-time"></i> {{ formatDate(article.display_time) || formatDate(article.created_at) }}</span>
                <span><i class="el-icon-view"></i> {{ article.pageviews || 0 }} 阅读</span>
                <span><i class="el-icon-chat-dot-round"></i> {{ commentCount.total }} 评论</span>
              </div>
            </div>
          </div>
        </div>

        <div class="article-body" v-html="article.content || '<p style=\'color:#909399;\'>（暂无正文内容）</p>'"></div>
      </template>

      <el-empty v-else-if="!loading" description="文章不存在或已被删除"></el-empty>
    </el-card>

    <!-- 评论区 -->
    <el-card shadow="hover" class="comments-card" v-loading="commentLoading">
      <div slot="header" class="comments-header">
        <div class="comments-title">
          <i class="el-icon-chat-dot-round" style="color:#409eff;margin-right:8px;"></i>
          <span>评论区</span>
          <el-tag size="mini" type="info">{{ commentCount.total }} 条</el-tag>
          <el-tag size="mini" type="warning" v-if="commentCount.pending > 0">{{ commentCount.pending }} 条待审核</el-tag>
        </div>
      </div>

      <!-- 发表评论 -->
      <div class="comment-input-box">
        <el-input
          type="textarea"
          v-model="newComment"
          :rows="3"
          placeholder="写下你的评论..."
          maxlength="2000"
          show-word-limit>
        </el-input>
        <div class="comment-input-actions">
          <span class="hint">管理员发表的评论直接通过；普通用户发表的评论需等待管理员或作者审核。</span>
          <el-button type="primary" icon="el-icon-edit" :disabled="!newComment.trim()" :loading="submitting" @click="submitComment">发表评论</el-button>
        </div>
      </div>

      <el-divider></el-divider>

      <!-- 评论列表 -->
      <div v-if="comments.length === 0" class="empty-comments">
        <el-empty description="暂无评论，快来抢沙发吧 👆"></el-empty>
      </div>

      <div v-else class="comment-list">
        <div v-for="(item, index) in comments" :key="item.id || index" class="comment-item" :class="{pending: item.status === 'pending', rejected: item.status === 'rejected'}">
          <div class="comment-avatar">
            <el-avatar :size="42" style="background:linear-gradient(135deg,#4facfe,#00f2fe);font-size:16px;">{{ (item.username || '?').charAt(0) }}</el-avatar>
          </div>
          <div class="comment-body">
            <div class="comment-head">
              <strong class="comment-user">{{ item.username }}</strong>
              <span class="comment-time">{{ formatDate(item.created_at) }}</span>
              <el-tag v-if="item.status === 'pending'" size="mini" type="warning">待审核</el-tag>
              <el-tag v-if="item.status === 'rejected'" size="mini" type="danger">已驳回</el-tag>
              <el-tag v-if="item.status === 'approved'" size="mini" type="success" effect="plain">已通过</el-tag>
            </div>
            <div class="comment-content">{{ item.content }}</div>
            <div class="comment-actions" v-if="canManage(item)">
              <el-button type="success" size="mini" icon="el-icon-check" v-if="item.status !== 'approved'" @click="changeStatus(item.id, 'approved')">通过</el-button>
              <el-button type="danger" size="mini" icon="el-icon-close" v-if="item.status !== 'rejected'" @click="changeStatus(item.id, 'rejected')">驳回</el-button>
              <el-button type="text" size="mini" icon="el-icon-delete" @click="handleDeleteComment(item)">删除</el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getArticleDetail } from '@/api/article'
import { getCommentsByArticle, createComment, approveComment, deleteComment, countComment } from '@/api/article'
import { mapGetters } from 'vuex'

export default {
  name: 'ArticleDetail',
  computed: {
    ...mapGetters(['name', 'isAdmin']),
    routeId() {
      return this.$route.params.id
    }
  },
  data() {
    return {
      loading: false,
      commentLoading: false,
      submitting: false,
      article: {},
      comments: [],
      commentCount: { total: 0, approved: 0, pending: 0 },
      newComment: ''
    }
  },
  created() {
    this.fetchArticle()
    this.fetchComments()
  },
  methods: {
    async fetchArticle() {
      this.loading = true
      try {
        const res = await getArticleDetail(this.routeId)
        if (res && res.code === 20000) {
          this.article = res.data || {}
        }
      } catch (e) {
      } finally {
        this.loading = false
      }
    },
    async fetchComments() {
      this.commentLoading = true
      try {
        // 管理员/作者可以看到所有评论（含 pending），普通用户只看 approved
        const approvedOnly = !this.isAdmin && !this.isAuthor() ? 'true' : 'false'
        const res = await getCommentsByArticle({ article_id: this.routeId, page: 1, limit: 200, approved_only: approvedOnly })
        if (res && res.code === 20000) {
          this.comments = (res.data && res.data.items) || []
        }
        const countRes = await countComment({ article_id: this.routeId })
        if (countRes && countRes.code === 20000) {
          this.commentCount = countRes.data || { total: 0, approved: 0, pending: 0 }
        }
      } catch (e) {
      } finally {
        this.commentLoading = false
      }
    },
    isAuthor() {
      return this.name && this.article.author && String(this.name) === String(this.article.author)
    },
    canManage(item) {
      // 管理员或文章作者可以审核/删除评论
      return this.isAdmin || this.isAuthor()
    },
    async submitComment() {
      if (!this.newComment.trim()) return
      this.submitting = true
      try {
        const res = await createComment({
          article_id: this.routeId,
          content: this.newComment.trim()
        })
        if (res && res.code === 20000) {
          this.$message.success(res.data.status === 'pending' ? '评论已提交，等待审核！' : '评论发表成功！')
          this.newComment = ''
          this.fetchComments()
        }
      } catch (e) {
      } finally {
        this.submitting = false
      }
    },
    async changeStatus(id, status) {
      try {
        const res = await approveComment({ id, status })
        if (res && res.code === 20000) {
          this.$message.success(status === 'approved' ? '已通过审核' : '已驳回')
          this.fetchComments()
        }
      } catch (e) {
      }
    },
    async handleDeleteComment(item) {
      this.$confirm(`确认删除 ${item.username} 的这条评论？`, '提示', {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const res = await deleteComment(item.id)
        if (res && res.code === 20000) {
          this.$message.success('删除成功')
          this.fetchComments()
        }
      }).catch(() => {})
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const d = new Date(String(dateStr).replace(/-/g, '/'))
      if (isNaN(d.getTime())) return String(dateStr)
      const pad = (n) => String(n).padStart(2, '0')
      return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
    }
  }
}
</script>

<style lang="scss" scoped>
.detail-container {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: calc(100vh - 84px);

  body.theme-dark & {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  }

  .detail-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .right-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }

  .article-card {
    border-radius: 16px;
    border: none;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);

    body.theme-dark & {
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    ::v-deep .el-card__body {
      padding: 40px 50px;
    }

    .article-header {
      margin-bottom: 30px;
      padding-bottom: 25px;
      border-bottom: 2px solid #f0f2f5;

      body.theme-dark & {
        border-bottom: 2px solid #0f3460;
      }

      .article-title {
        font-size: 32px;
        font-weight: 700;
        color: #303133;
        margin: 0 0 20px 0;
        line-height: 1.4;

        body.theme-dark & {
          color: #e0e0e0;
        }
      }

      .article-meta {
        display: flex;
        align-items: center;
        gap: 14px;

        .meta-text {
          .author-name {
            font-weight: 600;
            font-size: 15px;
            color: #303133;
            margin-bottom: 4px;

            body.theme-dark & {
              color: #e0e0e0;
            }
          }
          .meta-sub {
            color: #909399;
            font-size: 13px;
            display: flex;
            gap: 16px;

            body.theme-dark & {
              color: #808080;
            }

            i { margin-right: 4px; }
          }
        }
      }
    }

    .article-body {
      font-size: 16px;
      line-height: 1.85;
      color: #4c4d4f;
      word-break: break-word;

      body.theme-dark & {
        color: #c0c0c0;
      }

      :deep(h1), :deep(h2), :deep(h3), :deep(h4) {
        color: #303133;
        margin: 28px 0 14px 0;
        font-weight: 700;

        body.theme-dark & {
          color: #e0e0e0;
        }
      }
      :deep(h2) { font-size: 22px; }
      :deep(h3) { font-size: 18px; }
      :deep(p) { margin: 14px 0; }
      :deep(ul), :deep(ol) { padding-left: 24px; margin: 14px 0; }
      :deep(li) { margin: 6px 0; }
      :deep(strong) { color: #303133; }
      :deep(pre) {
        background: #2d2d2d;
        color: #e8e8e8;
        padding: 16px 20px;
        border-radius: 8px;
        overflow-x: auto;
        font-size: 13px;
        line-height: 1.6;
      }
      :deep(code) {
        background: #f5f5f5;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: Consolas, Monaco, monospace;
        font-size: 13px;
        color: #e96900;

        body.theme-dark & {
          background: #0f3460;
          color: #e6a23c;
        }
      }
      :deep(pre code) {
        background: transparent;
        color: inherit;
        padding: 0;
      }
      :deep(a) {
        color: #409eff;
        text-decoration: none;
        &:hover { text-decoration: underline; }
      }
    }
  }

  .comments-card {
    border-radius: 16px;
    border: none;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);

    body.theme-dark & {
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    ::v-deep .el-card__header {
      border-bottom: 2px solid #f0f2f5;
      padding: 18px 24px;

      body.theme-dark & {
        border-bottom: 2px solid #0f3460;
      }
    }

    .comments-header {
      .comments-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        font-weight: 600;
        color: #303133;

        body.theme-dark & {
          color: #e0e0e0;
        }
      }
    }

    .comment-input-box {
      padding: 8px 0 0 0;

      .comment-input-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 12px;

        .hint {
          font-size: 12px;
          color: #909399;

          body.theme-dark & {
            color: #808080;
          }
        }
      }
    }

    .empty-comments {
      padding: 20px 0;
    }

    .comment-list {
      .comment-item {
        display: flex;
        gap: 14px;
        padding: 18px 0;
        border-bottom: 1px solid #f0f2f5;
        transition: all 0.3s ease;

        body.theme-dark & {
          border-bottom: 1px solid #0f3460;
        }

        &:last-child { border-bottom: none; }

        &:hover {
          background: #fafbfc;
          padding-left: 10px;
          margin-left: -10px;
          border-radius: 8px;

          body.theme-dark & {
            background: #1a2a4a;
          }
        }

        &.pending {
          background: #fdf6ec;
          border-radius: 8px;
          padding-left: 14px;
          margin-left: -10px;

          body.theme-dark & {
            background: #3a2a0a;
          }
        }
        &.rejected {
          opacity: 0.55;
        }

        .comment-avatar {
          flex-shrink: 0;
        }

        .comment-body {
          flex: 1;
          min-width: 0;

          .comment-head {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
            flex-wrap: wrap;

            .comment-user {
              color: #303133;
              font-size: 14px;

              body.theme-dark & {
                color: #e0e0e0;
              }
            }
            .comment-time {
              color: #909399;
              font-size: 12px;

              body.theme-dark & {
                color: #808080;
              }
            }
          }

          .comment-content {
            font-size: 14px;
            color: #4c4d4f;
            line-height: 1.7;
            word-break: break-word;
            white-space: pre-wrap;

            body.theme-dark & {
              color: #c0c0c0;
            }
          }

          .comment-actions {
            margin-top: 10px;
            display: flex;
            gap: 6px;
          }
        }
      }
    }
  }
}
</style>

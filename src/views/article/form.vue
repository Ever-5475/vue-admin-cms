<template>
  <div class="form-container">
    <el-card shadow="hover">
      <div slot="header"><span>{{ isEdit ? '编辑文章' : '发布文章' }}</span></div>
      <el-form ref="articleForm" :model="articleForm" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title"><el-input v-model="articleForm.title" placeholder="请输入文章标题"></el-input></el-form-item>
        <el-form-item label="作者" prop="author"><el-input v-model="articleForm.author" placeholder="请输入作者名称"></el-input></el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="articleForm.status" placeholder="请选择状态">
            <el-option label="草稿" value="draft"></el-option>
            <el-option label="发布" value="published"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="浏览量" prop="pageviews"><el-input-number v-model="articleForm.pageviews" :min="0"></el-input-number></el-form-item>
        <el-form-item label="发布时间" prop="display_time"><el-date-picker v-model="articleForm.display_time" type="datetime" placeholder="选择日期时间"></el-date-picker></el-form-item>
        <el-form-item label="文章正文" prop="content">
          <el-input
            type="textarea"
            v-model="articleForm.content"
            :rows="14"
            placeholder="请输入文章正文内容，支持 HTML 格式，例如：<h2>小标题</h2>、<p>段落内容</p>、<ul><li>列表项</li></ul>"
            maxlength="50000"
            show-word-limit></el-input>
          <div style="color:#909399;font-size:12px;margin-top:6px;">提示：详情页会按 HTML 渲染正文内容。</div>
        </el-form-item>
        <el-form-item><el-button type="primary" @click="handleSubmit">提交</el-button><el-button @click="$router.back()">取消</el-button></el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { getArticleDetail, createArticle, updateArticle } from '@/api/article'
export default {
  name: 'ArticleForm',
  data() {
    return {
      isEdit: false, articleId: null,
      articleForm: { title: '', author: '', status: 'draft', pageviews: 0, content: '', display_time: '' },
      rules: { title: [{ required: true, message: '请输入标题', trigger: 'blur' }], author: [{ required: true, message: '请输入作者', trigger: 'blur' }], status: [{ required: true, message: '请选择状态', trigger: 'change' }] }
    }
  },
  created() { if (this.$route.params.id) { this.isEdit = true; this.articleId = this.$route.params.id; this.getArticleData() } },
  methods: {
    getArticleData() { getArticleDetail(this.articleId).then(response => { if (response && response.code === 20000) { this.articleForm = Object.assign({}, this.articleForm, response.data) } }) },
    handleSubmit() {
      this.$refs.articleForm.validate(valid => {
        if (valid) {
          if (this.isEdit) { updateArticle(this.articleId, this.articleForm).then(() => { this.$message.success('更新成功'); this.$router.push('/article/list') }) }
          else { createArticle(this.articleForm).then(() => { this.$message.success('创建成功'); this.$router.push('/article/list') }) }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.form-container { max-width: 800px; margin: 20px auto; }
</style>

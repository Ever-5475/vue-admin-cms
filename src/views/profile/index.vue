<template>
  <div class="profile-container">
    <el-card shadow="hover" class="profile-card">
      <div slot="header" class="card-header">
        <span><i class="el-icon-setting"></i> 个人中心</span>
        <el-tag :type="roleTagType" size="small" effect="plain">{{ isAdmin ? '管理员' : '普通用户' }}</el-tag>
      </div>

      <!-- 用户信息展示 -->
      <div class="user-info-section">
        <el-avatar :size="100" :src="avatarSrc" class="user-avatar"></el-avatar>
        <div class="user-basic">
          <h2 class="user-name">{{ name }}</h2>
          <p class="user-sub">角色: {{ role === 'admin' ? '管理员' : '普通用户' }}</p>
        </div>
      </div>

      <el-divider></el-divider>

      <el-divider></el-divider>

      <!-- 修改个人信息表单 -->
      <el-form ref="profileForm" :model="profileForm" :rules="rules" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="profileForm.name" placeholder="请输入姓名"></el-input>
        </el-form-item>

        <el-form-item label="头像URL">
          <el-input v-model="profileForm.avatar" placeholder="请输入头像URL（留空使用默认头像）" clearable></el-input>
        </el-form-item>

        <el-form-item label="新密码" prop="password">
          <el-input v-model="profileForm.password" type="password" show-password placeholder="留空则不修改"></el-input>
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="profileForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSave" :loading="loading">保存修改</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-divider></el-divider>

      <!-- 权限区别表 -->
      <div class="permission-section">
        <h3 class="section-title"><i class="el-icon-key"></i> 权限说明</h3>
        <el-table :data="permissionTable" border stripe class="permission-table">
          <el-table-column prop="feature" label="功能模块" min-width="200" align="center" header-align="center"></el-table-column>
          <el-table-column label="普通用户" min-width="120" align="center" header-align="center">
            <template slot-scope="scope">
              <i v-if="scope.row.user" class="el-icon-success permission-icon success"></i>
              <i v-else class="el-icon-error permission-icon error"></i>
            </template>
          </el-table-column>
          <el-table-column label="管理员" min-width="120" align="center" header-align="center">
            <template slot-scope="scope">
              <i v-if="scope.row.admin" class="el-icon-success permission-icon success"></i>
              <i v-else class="el-icon-error permission-icon error"></i>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import request from '@/utils/request'

export default {
  name: 'Profile',
  data() {
    return {
      loading: false,
      profileForm: {
        name: '',
        avatar: '',
        password: '',
        confirmPassword: ''
      },
      rules: {
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
        password: [{ min: 6, message: '密码不能少于6位', trigger: 'blur' }]
      },
      permissionTable: [
        { feature: '文章管理', user: false, admin: true, description: '普通用户只能查看/编辑/删除自己的文章，管理员可以管理所有文章' },
        { feature: '用户管理', user: false, admin: true, description: '普通用户无法访问用户管理，管理员可以查看/创建/编辑/删除用户' },
        { feature: '评论管理', user: false, admin: true, description: '普通用户只能管理自己的评论，管理员可以管理所有评论' },
        { feature: '数据报表', user: true, admin: true, description: '普通用户可以查看基础统计，管理员可以查看完整数据报表和趋势分析' },
        { feature: '系统设置', user: false, admin: true, description: '普通用户无法访问系统设置，管理员可以配置系统参数' },
        { feature: '操作日志', user: true, admin: true, description: '普通用户可以查看自己的操作日志，管理员可以查看所有用户的操作日志' }
      ]
    }
  },
  computed: {
    ...mapGetters(['name', 'avatar', 'role', 'isAdmin']),
    roleTagType() {
      return this.isAdmin ? 'danger' : 'success'
    },
    avatarSrc() {
      if (this.profileForm.avatar && this.profileForm.avatar.trim() !== '') {
        return this.profileForm.avatar
      }
      if (this.avatar && this.avatar.trim() !== '' && !String(this.avatar).includes('[object')) {
        return this.avatar
      }
      return null
    }
  },
  created() {
    this.profileForm.name = this.name || ''
    this.profileForm.avatar = (this.avatar && !String(this.avatar).includes('[object')) ? this.avatar : ''
  },
  methods: {
    handleSave() {
      const validateConfirm = (rule, value, callback) => {
        if (this.profileForm.password && value !== this.profileForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      }
      const mergedRules = {
        ...this.rules,
        confirmPassword: [{ validator: validateConfirm, trigger: 'blur' }]
      }

      this.$refs.profileForm.validateField ? null : null
      const valid = this.profileForm.password ? this.profileForm.password === this.profileForm.confirmPassword : true
      if (this.profileForm.password && !valid) {
        this.$message.error('两次输入的密码不一致')
        return
      }
      if (!this.profileForm.name || !this.profileForm.name.trim()) {
        this.$message.error('姓名不能为空')
        return
      }
      if (this.profileForm.password && this.profileForm.password.length < 6) {
        this.$message.error('密码不能少于6位')
        return
      }

      this.loading = true
      const data = {
        name: this.profileForm.name.trim(),
        avatar: this.profileForm.avatar.trim()
      }
      if (this.profileForm.password) {
        data.password = this.profileForm.password
      }

      request({
        url: '/vue-admin-template/user/self-update',
        method: 'post',
        data
      }).then(response => {
        if (response.code === 20000) {
          this.$message.success('个人信息修改成功')
          // 更新 Vuex 中的用户信息
          if (response.data) {
            this.$store.commit('user/SET_NAME', response.data.name)
            this.$store.commit('user/SET_AVATAR', response.data.avatar)
          }
          this.profileForm.password = ''
          this.profileForm.confirmPassword = ''
        } else {
          this.$message.error(response.message || '保存失败')
        }
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    handleReset() {
      this.profileForm.name = this.name || ''
      this.profileForm.avatar = (this.avatar && !String(this.avatar).includes('[object')) ? this.avatar : ''
      this.profileForm.password = ''
      this.profileForm.confirmPassword = ''
      this.$refs.profileForm && this.$refs.profileForm.clearValidate && this.$refs.profileForm.clearValidate()
    }
  }
}
</script>

<style lang="scss" scoped>
.profile-container {
  padding: 20px;
  min-height: calc(100vh - 84px);
}

.profile-card {
  max-width: 700px;
  margin: 0 auto;
  border-radius: 12px;

  ::v-deep .el-card__body {
    padding: 30px 40px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 18px;
    font-weight: 600;
    color: #303133;

    body.theme-dark & {
      color: #e0e0e0;
    }
  }

  .user-info-section {
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 10px 0;

    .user-avatar {
      border: 4px solid #409eff;
      box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
    }

    .user-basic {
      flex: 1;

      .user-name {
        margin: 0 0 8px 0;
        font-size: 24px;
        color: #303133;
        font-weight: 600;

        body.theme-dark & {
          color: #e0e0e0;
        }
      }

      .user-sub {
        margin: 0;
        color: #909399;
        font-size: 14px;

        body.theme-dark & {
          color: #808080;
        }
      }
    }
  }

  .permission-section {
    margin: 20px 0;

    .section-title {
      font-size: 18px;
      color: #303133;
      margin: 0 0 16px 0;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;

      body.theme-dark & {
        color: #e0e0e0;
      }

      i {
        color: #409eff;
      }
    }

    .permission-table {
      border-radius: 8px;
      overflow: hidden;

      ::v-deep .permission-icon {
        font-size: 22px;
        font-weight: bold;
        width: 30px;
        height: 30px;
        line-height: 30px;
        border-radius: 50%;
        text-align: center;
        display: inline-block;

        &.success {
          color: #fff !important;
          background-color: #67c23a !important;
        }

        &.error {
          color: #fff !important;
          background-color: #f56c6c !important;
        }
      }
    }
  }
}
</style>

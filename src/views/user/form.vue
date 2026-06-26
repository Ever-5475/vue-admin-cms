<template>
  <div class="form-container">
    <el-card shadow="hover">
      <div slot="header"><span>{{ isEdit ? '编辑用户' : '新增用户' }}</span></div>
      <el-form ref="userForm" :model="userForm" :rules="rules" label-width="100px">
        <el-form-item label="用户名" prop="username"><el-input v-model="userForm.username" placeholder="请输入用户名" :disabled="isEdit"></el-input></el-form-item>
        <el-form-item label="密码" prop="password"><el-input v-model="userForm.password" type="password" placeholder="请输入密码（至少6位）" show-password></el-input></el-form-item>
        <el-form-item label="姓名" prop="name"><el-input v-model="userForm.name" placeholder="请输入姓名"></el-input></el-form-item>
        <el-form-item label="角色" prop="role"><el-select v-model="userForm.role" placeholder="请选择角色" :disabled="isEdit && userForm.username === 'admin'"><el-option label="管理员" value="admin"></el-option><el-option label="普通用户" value="user"></el-option></el-select></el-form-item>
        <el-form-item label="头像URL" prop="avatar"><el-input v-model="userForm.avatar" placeholder="请输入头像URL（留空将使用默认头像）" clearable></el-input></el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">{{ isEdit ? '更新' : '创建' }}</el-button>
          <el-button @click="$router.back()">取消</el-button>
          <el-button v-if="!isEdit" type="success" @click="handleSubmitAndLogin" :loading="loading">创建并登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { getUserDetail, createUser, updateUser, login } from '@/api/user'

export default {
  name: 'UserForm',
  data() {
    return {
      isEdit: false,
      userId: null,
      loading: false,
      userForm: {
        username: '',
        password: '',
        name: '',
        role: 'user',
        avatar: ''
      },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码不能少于6位', trigger: 'blur' }],
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
        role: [{ required: true, message: '请选择角色', trigger: 'change' }]
      }
    }
  },
  created() {
    if (this.$route.params.id) {
      this.isEdit = true
      this.userId = this.$route.params.id
      this.getUserData()
    }
  },
  methods: {
    getUserData() {
      getUserDetail(this.userId).then(response => {
        this.userForm = response.data
      })
    },
    handleSubmit() {
      this.$refs.userForm.validate(valid => {
        if (valid) {
          this.loading = true
          if (this.isEdit) {
            updateUser(this.userId, this.userForm).then(() => {
              this.$message.success('更新成功')
              this.loading = false
              this.$router.push('/user/list')
            }).catch(() => {
              this.loading = false
            })
          } else {
            createUser(this.userForm).then(() => {
              this.$message.success('创建成功！请使用新账号登录')
              this.loading = false
              this.$confirm('用户创建成功！是否立即使用新账号登录？', '提示', {
                confirmButtonText: '立即登录',
                cancelButtonText: '稍后再说',
                type: 'success'
              }).then(() => {
                this.handleAutoLogin()
              }).catch(() => {
                this.$router.push('/user/list')
              })
            }).catch(error => {
              this.loading = false
              this.$message.error('创建失败: ' + (error.message || '未知错误'))
            })
          }
        }
      })
    },
    handleSubmitAndLogin() {
      this.$refs.userForm.validate(valid => {
        if (valid) {
          this.loading = true
          createUser(this.userForm).then(() => {
            this.$message.success('创建成功，正在自动登录...')
            this.handleAutoLogin()
          }).catch(error => {
            this.loading = false
            this.$message.error('创建失败: ' + (error.message || '未知错误'))
          })
        }
      })
    },
    handleAutoLogin() {
      const { username, password } = this.userForm
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        this.$store.commit('user/SET_TOKEN', data.token)
        this.setToken(data.token)
        this.$message.success(`欢迎 ${username}！登录成功`)
        this.loading = false
        this.$router.push('/')
      }).catch(error => {
        this.loading = false
        this.$message.error('自动登录失败，请手动登录: ' + (error.message || ''))
        this.$router.push('/login')
      })
    },
    setToken(token) {
        if (typeof window !== 'undefined') {
          localStorage.setItem('vue_admin_token', token)
        }
    }
  }
}
</script>

<style lang="scss" scoped>
.form-container { max-width: 800px; margin: 20px auto; }
</style>

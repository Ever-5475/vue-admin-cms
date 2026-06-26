<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.username" placeholder="搜索用户名" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter"></el-input>
      <el-select v-model="listQuery.role" placeholder="角色筛选" clearable style="width: 150px" class="filter-item">
        <el-option label="管理员" value="admin"></el-option>
        <el-option label="普通用户" value="user"></el-option>
      </el-select>
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
      <el-button class="filter-item" type="success" icon="el-icon-plus" @click="$router.push('/user/create')">新增用户</el-button>
    </div>

    <el-table v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%">
      <el-table-column align="center" label="ID" width="80"><template slot-scope="scope">{{ scope.row.id }}</template></el-table-column>
      <el-table-column align="center" label="头像" width="80"><template slot-scope="scope"><el-avatar :size="40" :src="scope.row.avatar || require('@/views/login/5.gif')"></el-avatar></template></el-table-column>
      <el-table-column align="center" label="用户名"><template slot-scope="scope">{{ scope.row.username }}</template></el-table-column>
      <el-table-column align="center" label="姓名" width="120"><template slot-scope="scope">{{ scope.row.name }}</template></el-table-column>
      <el-table-column align="center" label="角色" width="120"><template slot-scope="scope"><el-tag :type="scope.row.role === 'admin' ? 'danger' : 'primary'">{{ scope.row.role === 'admin' ? '管理员' : '用户' }}</el-tag></template></el-table-column>
      <el-table-column align="center" label="注册时间" width="180"><template slot-scope="scope"><i class="el-icon-time" /><span>{{ scope.row.created_at | formatDate }}</span></template></el-table-column>
      <el-table-column align="center" label="操作" width="200" fixed="right"><template slot-scope="scope"><el-button type="primary" size="mini" icon="el-icon-edit" @click="$router.push(`/user/edit/${scope.row.id}`)">编辑</el-button><el-button v-if="scope.row.username !== 'admin'" type="danger" size="mini" icon="el-icon-delete" @click="handleDelete(scope.row.id)">删除</el-button></template></el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList"></pagination>
  </div>
</template>

<script>
import { getUserList, deleteUser } from '@/api/user'
import Pagination from '@/components/Pagination'

export default {
  name: 'UserList',
  components: { Pagination },
  filters: {
    formatDate(time) {
      if (!time) return ''
      const date = new Date(time)
      return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`
    }
  },
  data() {
    return {
      list: [], total: 0, listLoading: true,
      listQuery: { page: 1, limit: 10, username: '', role: '' }
    }
  },
  created() { this.getList() },
  methods: {
    getList() {
      this.listLoading = true
      getUserList(this.listQuery).then(response => {
        this.list = response.data.items; this.total = response.data.total; this.listLoading = false
      })
    },
    handleFilter() { this.listQuery.page = 1; this.getList() },
    handleDelete(id) {
      this.$confirm('确认删除该用户？', '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }).then(() => {
        deleteUser(id).then(() => { this.$message.success('删除成功'); this.getList() })
      })
    }
  }
}
</script>

<style scoped>.filter-container { padding-bottom: 20px; }.filter-item { margin-right: 10px; }</style>

<template>
    <div class="user-list-container">
      <div>
        <el-col :span="8" style="margin-bottom: 20px">
           <el-input placeholder="搜索" v-model="keywords" @keyup.enter.native="searchClick">
                <el-button slot="append" icon="el-icon-search" @click="searchClick"></el-button>
            </el-input>
        </el-col>
        <div class="addUser-btn">
          <el-button type="primary" @click="addClick">添加用户</el-button>
        </div>
      </div>
      <el-table
              class="table"
              style="margin-bottom: 20px;"
              v-loading="loading"
              element-loading-text="拼命加载中"
              :data="userList"
              border
              >
          <el-table-column
                  prop="username"
                  label="用户名"
                  align="center">
          </el-table-column>
          <el-table-column
                  prop="name"
                  label="姓名"
                  width="90"
                  align="center">
          </el-table-column>
          <el-table-column
                  prop="phone"
                  label="手机号"
                  width="110"
                  align="center">
          </el-table-column>
          <el-table-column
                  prop="email"
                  label="email"
                  align="center">
          </el-table-column>
          <el-table-column
            prop="department"
            label="department"
            align="center">
          </el-table-column>
          <el-table-column
                  prop="is_active"
                  label="登录状态"
                  align="center"
                  width="78">
              <template slot-scope="scope">
                  <el-switch
                          v-model="scope.row.is_active"
                          @change="statusChange(scope.row)">
                  </el-switch>
              </template>
          </el-table-column>
          <el-table-column
                  prop="last_login"
                  label="上次登陆时间"
                  align="center"
                  width="155">
          </el-table-column>
          <el-table-column
                  prop=""
                  label="操作"
                  width="215"
                  align="center">
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="checkRoleClick(scope.row)">查看角色</el-button>
                <el-button type="text" size="small" @click="chooceRoleClick(scope.row)">指定角色</el-button>
                <el-button type="text" size="small" @click="changeMobileClick(scope.row)">修改</el-button>
                <el-button type="text" size="small" @click="deleteClick(scope.row)">删除</el-button>
              </template>
          </el-table-column>
      </el-table>
      <div class="text-center" v-show="total_num>=10">
          <el-pagination
                  style="text-align: center"
                  background
                  @current-change="paginationChange"
                  layout="total, prev, pager, next, jumper"
                  :current-page.sync="page"
                  :total="total_num">
          </el-pagination>
      </div>
      <!-- 增加用户 -->
      <el-dialog title="增加用户" :visible.sync="addUserFormVisible">
          <el-form ref="addUserForm" :model="addUserForm" label-width="70px" :rules="addUserRule">
              <el-form-item label="登陆名" prop="username">
                  <el-input v-model="addUserForm.username" placeholder="请输入登陆名"></el-input>
              </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="addUserForm.password" type="password" placeholder="请输入密码"></el-input>
            </el-form-item>
              <el-form-item label="姓名" prop="name">
                  <el-input v-model="addUserForm.name" placeholder="请输入姓名"></el-input>
              </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="addUserForm.email" placeholder="请输入姓名"></el-input>
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="addUserForm.phone" placeholder="请输入手机号"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
              <el-button @click="addUserFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="submitAddClick">确 定</el-button>
          </div>
      </el-dialog>
      <el-dialog title="查看角色" :visible.sync="checkRoleVisible">
          <div class="text-center">
            <el-tag type="info" v-for="(item, index) in roleTags" :key="index" style="margin:0 10px;">{{ item.name }}</el-tag>
          </div>
          <div slot="footer" class="dialog-footer">
              <el-button @click="checkRoleVisible = false">取 消</el-button>
              <el-button type="primary" @click="checkRoleVisible = false">确 定</el-button>
          </div>
      </el-dialog>
      <el-dialog title="指定角色" :visible.sync="chooseRoleVisible">
          <el-form :model="chooseRole" label-width="70px">
              <el-form-item label="用户名">
                  <el-input v-model="chooseRole.username" disabled></el-input>
              </el-form-item>
              <el-form-item label="角色">
                  <el-select v-model="roles" multiple placeholder="请选择角色" style="width:100%">
                    <el-option
                      v-for="(item, index) in rolesList"
                      :key="index"
                      :label="item.name"
                      :value="item.id">
                    </el-option>
                  </el-select>
              </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
              <el-button @click="chooseRoleVisible = false">取 消</el-button>
              <el-button type="primary" @click="submitChooseRoleClick">确 定</el-button>
          </div>
      </el-dialog>
      <el-dialog title="修改用户信息" :visible.sync="changeMobileFormVisible">
          <el-form ref="changeMobileForm" :model="changeMobileForm" label-width="70px" :rules="addUserRule">
              <el-form-item label="登陆名">
                  <el-input v-model="changeMobileForm.username" placeholder="请输入登陆名" disabled></el-input>
              </el-form-item>
              <el-form-item label="email" prop="email">
                  <el-input v-model="changeMobileForm.email" placeholder="请输入邮箱"></el-input>
              </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="changeMobileForm.phone" placeholder="请输入手机号"></el-input>
            </el-form-item>
            <el-form-item label="姓名" prop="name">
              <el-input v-model="changeMobileForm.name" placeholder="请输入姓名"></el-input>
            </el-form-item>
            <el-form-item label="部门(选填)" prop="department">
              <el-input v-model="changeMobileForm.department" placeholder="请输入部门"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
              <el-button @click="changeMobileFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="submitChangeMobileClick">确 定</el-button>
          </div>
      </el-dialog>
    </div>
</template>

<script>
import { getUserList, deleteUser, addUser, updateUser, getGroupsList, getUserGroupsList, updateUserGroupsList } from '@/api/account'

export default {
  data() {
    const checkYNMobile = (rule, value, callback) => {
      if (!value || value.length === 11) {
        callback()
      } else {
        callback(new Error('请确保这个字段至少包含 11 个字符'))
      }
    }
    const validatePass = (rule, value, callback) => {
      if (value.length < 5) {
        callback(new Error('密码不能小于5位'))
      } else {
        callback()
      }
    }
    return {
      name: '',
      userList: [],
      total_num: 0,
      page: 1,
      listLoading: true,
      loading: true,
      keywords: '',
      userGroupList: [],
      addUserForm: {
        username: '',
        name: '',
        password: '',
        phone: '',
        email: ''
      },
      addUserRule: {
        username: [
          { required: true, message: '请输入登陆名', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        password: [
          { required: true, trigger: 'blur', validator: validatePass }
        ],
        phone: [
          { required: false, validator: checkYNMobile, trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur', type: 'email' }
        ]
      },
      rolesList: [], // 角色列表
      addUserFormVisible: false, // 增加用户弹框
      chooseRoleVisible: false, // 指定角色弹框
      chooseRole: {},
      roles: [],
      changeMobileFormVisible: false,
      changeMobileForm: {},
      checkRoleVisible: false,
      roleTags: []
    }
  },
  created() {
    this.fetchData()
    // 获取所有角色列表
    getGroupsList({ page_size: 0 }).then(res => {
      this.rolesList = res
    })
  },
  methods: {
    fetchData() {
      this.loading = true
      getUserList({ page: this.page, keywords: this.keywords }).then(res => {
        this.userList = res.results
        this.total_num = res.count
        this.loading = false
      })
    },
    searchClick() {
      this.page = 1
      this.fetchData()
    },
    paginationChange(val) {
      this.page = val
      this.fetchData()
    },
    deleteClick(row) {
      this.$confirm('此操作将删除用户 “' + row.name + '” , 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteUser(row.id).then(response => {
          this.$message({
            message: '删除用户 “' + row.name + '” 成功',
            type: 'success'
          })
          this.fetchData()
        })
      }).catch(() => {
        this.$message({
          message: '操作失败',
          type: 'error'
        })
      })
    },
    addClick() {
      this.addUserFormVisible = true
      if (this.$refs['addUserForm'] !== undefined) {
        this.$refs['addUserForm'].resetFields()
      }
    },
    submitAddClick() {
      this.$refs['addUserForm'].validate((valid) => {
        if (!valid) {
          return
        }
        const params = Object.assign({}, this.addUserForm)
        addUser(params).then(res => {
          this.addUserFormVisible = false
          this.fetchData()
          this.$message({
            message: '操作成功',
            type: 'success'
          })
        }, err => {
          console.log(err.message)
        }
        )
      })
    },
    statusChange(row) {
      updateUser(row.id, { is_active: row.is_active }).then(() => {
        this.fetchData()
        this.$message({
          message: '操作成功',
          type: 'success'
        })
      })
    },
    chooceRoleClick(row) {
      this.roles = []
      this.chooseRoleVisible = true
      this.chooseRole = Object.assign({}, row)
      // 获取指定用户角色列表
      getUserGroupsList(row.id, { page_size: 0 }).then(res => {
        this.roles = res.map(item => {
          return item.id
        })
      })
    },
    submitChooseRoleClick() {
      if (!this.roles.length) {
        this.$message.error('请选择角色')
        return
      }
      updateUserGroupsList(this.chooseRole.id, { gid: this.roles }).then(res => {
        this.chooseRoleVisible = false
        this.$message({
          message: '操作成功',
          type: 'success'
        })
      })
    },
    changeMobileClick(row) {
      this.changeMobileFormVisible = true
      this.changeMobileForm = row
    },
    submitChangeMobileClick() {
      this.$refs['changeMobileForm'].validate((valid) => {
        if (!valid) {
          return
        }
        const data = { phone: this.changeMobileForm.phone, email: this.changeMobileForm.email, name: this.changeMobileForm.name, department: this.changeMobileForm.department }
        updateUser(this.changeMobileForm.id, data).then(() => {
          this.changeMobileFormVisible = false
          this.fetchData()
          this.$message({
            message: '操作成功',
            type: 'success'
          })
        })
      })
    },
    checkRoleClick(row) {
      this.roleTags = []
      getUserGroupsList(row.id, { page_size: 0 }).then(res => {
        this.roleTags = res
        if (this.roleTags.length > 0) {
          this.checkRoleVisible = true
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .user-list-container {
    position: relative;
    display: block;
    .addUser-btn{
      text-align: right;
    }
  }
</style>


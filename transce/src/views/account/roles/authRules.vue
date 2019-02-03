<template>
  <div style="padding: 10px">
    <el-card shadow="always">
      <el-row :gutter="20">
        <el-col :span="14">
          <div style="margin-bottom: 20px">
            <el-alert title="" type="success" :closable="false" icon="el-icon-warning"><i class="el-icon-warning"><span>&nbsp;&nbsp;平台权限表</span></i></el-alert>
          </div>
          <div>
            <el-tabs value="prod" type="border-card" @tab-click="handleChangeTab">
              <el-tab-pane name="prod" label="生产环境">
                <el-table size="small" :data="authRules">
                  <el-table-column label="工单流程">
                    <template slot-scope="scope">
                      <div v-if="scope.row.is_manual_review">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="角色" prop="role" :formatter="formatterRole"></el-table-column>
                  <el-table-column label="执行">
                    <template slot-scope="scope">
                      <div v-if="scope.row.execute">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="放弃">
                    <template slot-scope="scope">
                      <div v-if="scope.row.reject">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="回滚">
                    <template slot-scope="scope">
                      <div v-if="scope.row.rollback">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="审批">
                    <template slot-scope="scope">
                      <div v-if="scope.row.approve">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button size="mini" type="text" @click="handleUpdateBtn(scope.row)">修改</el-button>
                      <el-button size="mini" type="text" @click="handleDeleteRole(scope.row)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
              <el-tab-pane name="ppe" label="预发布环境">
                <el-table size="small" :data="authRules">
                  <el-table-column label="工单流程">
                    <template slot-scope="scope">
                      <div v-if="scope.row.is_manual_review">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="角色" prop="role" :formatter="formatterRole"></el-table-column>
                  <el-table-column label="执行">
                    <template slot-scope="scope">
                      <div v-if="scope.row.execute">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="放弃">
                    <template slot-scope="scope">
                      <div v-if="scope.row.reject">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="回滚">
                    <template slot-scope="scope">
                      <div v-if="scope.row.rollback">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="审批">
                    <template slot-scope="scope">
                      <div v-if="scope.row.approve">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button size="mini" type="text" @click="handleUpdateBtn(scope.row)">修改</el-button>
                      <el-button size="mini" type="text" @click="handleDeleteRole(scope.row)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
              <el-tab-pane name="test" label="测试环境">
                <el-table :data="authRules" size="small">
                  <el-table-column label="工单流程">
                    <template slot-scope="scope">
                      <div v-if="scope.row.is_manual_review">
                        <b><i class="el-icon-success"></i></b>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="角色" prop="role" :formatter="formatterRole"></el-table-column>
                  <el-table-column label="执行">
                    <template slot-scope="scope">
                      <div v-if="scope.row.execute">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="放弃">
                    <template slot-scope="scope">
                      <div v-if="scope.row.reject">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="回滚">
                    <template slot-scope="scope">
                      <div v-if="scope.row.rollback">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="审批">
                    <template slot-scope="scope">
                      <div v-if="scope.row.approve">
                        <i class="el-icon-success"></i>
                      </div>
                      <div v-else>
                        <i class="el-icon-error"></i>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button size="mini" type="text" @click="handleUpdateBtn(scope.row)">修改</el-button>
                      <el-button size="mini" type="text" @click="handleDeleteRole(scope.row)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-col>
        <el-col :span="10">
          <div class='left20'>
            <el-alert title="" type="warning" show-icon :closable="false">
              <b>SQL平台使用步骤</b>
                <p class='left20'>
                  <b>1</b>. 创建组/用户
                </p>
                <p class='left20'>
                  <b>2</b>. 平台流程设置
                </p>
                <p class='left20'>
                  <b>3</b>. 创建目标数据库/集群
                </p>
                <p class='left20'>
                  <b>4</b>. SQL工单设置
                </p>
                <p class='left20'>
                  <b>5</b>. 提交SQL工单及后续处理
                </p>
            </el-alert>
          </div>

          <div class='left20'>
            <el-alert title="" type="warning" show-icon :closable="false">
              <b>流程说明</b>
                <p class='left20'>
                  <b>1</b>. 测试环境
                </p>
                <p class="left40">
                  <b>1.1</b>. 提交人发起 --- 提交人执行
                </p>
                <p class='left20'>
                  <b>2</b>. 生产环境
                </p>
                <p class='left40'>
                  <b>2.1</b>. 无流程
                </p>
                <p class='left60'>
                  研发： 研发发起 --- 经理执行
                </p>
                <p class='left60'>
                  其它角色： 本用户发起 --- 本用户执行
                </p>
                <p class='left40'>
                  <b>2.2</b>. 有流程
                </p>
                <p class='left60'>
                  研发： 研发发起 --- 经理核准 --- 管理员执行
                </p>
                <p class='left60'>
                  经理： 经理发起 --- 经理核准 --- 管理员执行
                </p>
                <p class='left60'>
                  总监： 总监发起 --- 总监核准 --- 管理员执行
                </p>
                <p class='left60'>
                  管理员：管理员发起 --- 管理员本人核准 --- 其它管理员执行
                </p>
            </el-alert>
          </div>
        </el-col>

        <el-dialog
          title="修改"
          :visible.sync="dialogVisible"
          width="30%">
          <el-form ref="authRule" :model="authRule" label-width="100px">
            <el-form-item label="SQL平台权限">
              <el-checkbox v-model="authRule.is_manual_review">工单流程</el-checkbox>
              <el-checkbox v-model="authRule.execute">执行</el-checkbox>
              <el-checkbox v-model="authRule.reject">放弃</el-checkbox>
              <el-checkbox v-model="authRule.rollback">回滚</el-checkbox>
              <el-checkbox v-model="authRule.approve">审核</el-checkbox>
            </el-form-item>
            <el-form-item>
              <div style="margin-left: 60%">
            <el-button size="small" @click="handleCloseBtn">取 消</el-button>
            <el-button size="small" type="primary" @click="handleSetRolePermissionActions">确 定</el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-dialog>
      </el-row>
    </el-card>
  </div>
</template>

<script>
  import { getRolePerm, updateRolePerm, deleteRolePerm } from '@/api/account'
  export default {
    data() {
      return {
        checkAll: false,
        dialogVisible: false,
        indeterminate: true,
        getParams: {
          page: 1,
          pagesize: 1000,
          search: 'prod'
        },
        iconMap: {
          true: 'checkmark',
          false: 'close'
        },
        role_perm: {
          is_manual_review: '工单流程',
          execute: '执行',
          reject: '放弃',
          rollback: '回滚',
          approve: '审批',
          '工单流程': 'is_manual_review',
          '执行': 'execute',
          '放弃': 'reject',
          '回滚': 'rollback',
          '审批': 'approve'
        },
        roleMap: {
          developer: '研发',
          developer_manager: '研发经理',
          developer_supremo: '研发总监',
          admin: '管理员',
          test: '测试'
        },
        permiss: [],
        actions_checked: [],
        actions: [],
        authRule: {},
        authRules: []
      }
    },
    created() {
      this.handleGetAuthRules()
    },
    methods: {
      formatterRole(row) {
        const role = row.role
        const role_name = this.roleMap[role]
        return role_name
      },
      handleUpdateBtn(authRule) {
        if (this.$refs['authRule'] !== undefined) {
          this.$refs['authRule'].resetFields()
        }
        this.authRule = { ... authRule }
        this.dialogVisible = true
      },
      handleSetRolePermissionActions() {
        const id = this.authRule.id
        updateRolePerm(id, this.authRule).then(response => {
          console.log(response)
          this.$message.success('更新成功')
          this.handleGetAuthRules()
        })
        this.dialogVisible = false
      },
      handleDeleteRole(value) {
        const id = value.id
        const name = value.role_name
        this.$confirm(`删除该角色: ${name}, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteRolePerm(id).then(res => {
            this.$notify.success('删除成功')
            this.handleGetAuthRules()
          })
        }).catch(() => {
          this.$message.info('取消删除')
        })
      },
      handleChangeTab(data) {
        this.getParams.search = data.name
        this.handleGetAuthRules()
      },
      handleGetAuthRules() {
        getRolePerm(this.getParams)
          .then(
            response => {
              this.authRules = response.results
            }
          )
      },
      handleCloseBtn() {
        // this.authRule = {}
        this.$refs.authRule.resetFields()
        this.dialogVisible = false
      }
    }
  }
</script>

<style scoped>
  .left20 {
    margin-left: 20px;
  }
  .left40 {
    margin-left: 40px;
  }
  .left60 {
    margin-left: 60px;
  }
</style>

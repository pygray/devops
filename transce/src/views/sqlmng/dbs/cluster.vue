<template>
  <div class="cluster" style="padding: 10px;">
    <el-card shadow="always">
    <!--搜索-->
    <el-col :span="8" style="margin-bottom: 20px">
      <el-input placeholder="搜索" v-model="getClusterParams.search"  size="small"  @keyup.enter.native="searchClick">
        <el-button slot="append" icon="el-icon-search" size="small" @click="searchClick"></el-button>
      </el-input>
    </el-col>

    <!--添加按钮-->
    <el-col :span="16" style="text-align: right">
      <el-button type="primary" @click="handleAddModal" size="small">创建</el-button>
    </el-col>

    <!--table-->
    <el-table
    :data="clusterList"
    style="width: 100%"
    size="small">
      <el-table-column
        label="#"
        type="index">
      </el-table-column>
      <el-table-column
        label="集群名"
        prop="name">
      </el-table-column>
      <el-table-column
        label="数据库"
        prop="dbs">
        <template slot-scope="scope">
          <el-button type="text" size="mini" @click="handleDbListBtn(scope.row)">列表</el-button>
        </template>

      </el-table-column>
      <el-table-column
        label="备注"
        prop="remark">
      </el-table-column>
      <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button
          size="mini"
          type="primary"
          @click="handleUpdateModal(scope.row)">修改</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDeleteCluster(scope.row)">删除</el-button>
      </template>
      </el-table-column>
    </el-table>

    <!--分页-->
    <div class="text-center" v-show="getClusterParams.totalNum>=10">
      <el-pagination
        background
        layout="total, prev, pager, next, jumper"
        :page-size="getClusterParams.pagesize"
        :total="getClusterParams.totalNum"
        @current-change="handleCurrentChange">
      </el-pagination>
    </div>
    <!-- 创建集群 -->
    <el-dialog
      title="创建集群"
      :visible.sync="createModal"
      width="20%">
      <el-form ref="createClusterForm" :model="createClusterForm" :rules="rules" label-width="80px" size="small">
        <el-form-item label="集群名" prop="name">
          <el-input v-model="createClusterForm.name" placeholder="请输入集群名称"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="createClusterForm.remark" placeholder="请输入备注"></el-input>
        </el-form-item>
        <el-form-item>
          <div class="btn-wrapper">
            <el-button size="small" @click="handleCancelAdd">取消</el-button>
            <el-button size="small" type="primary" @click="handleCreateCluster">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- 修改集群 -->
    <el-dialog
      title="修改集群"
      :visible.sync="updateModal"
      width="30%">
      <el-form ref="updateClusterForm" :model="updateClusterForm" :rules="rules" :label-position="labelPosition" label-width="100px" size="small">
        <el-form-item label="集群名" prop="name" size="small">
          <el-input v-model="updateClusterForm.name" placeholder="请输入集群名称"></el-input>
        </el-form-item>
        <el-form-item label="目标数据库" prop="dbs" label-width="100px">
          <el-select v-model="updateClusterForm.dbs" multiple placeholder="请选择" style="width: 100%">
            <el-option
              v-for="item in dbList"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="updateClusterForm.remark" placeholder="请输入备注"></el-input>
        </el-form-item>
        <el-form-item>
          <div class="btn-wrapper">
            <el-button size="small" @click="handleCancelupdate">取消</el-button>
            <el-button size="small" type="primary" @click="handleUpdateCluster">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- 数据库列表 -->
    <el-dialog
      title="数据库"
      :visible.sync="dbListModal"
      width="40%">
      <el-table
      :data="clusterDbList"
      style="width: 100%"
      size="small">
        <el-table-column
          label="数据库名"
          prop="name">
        </el-table-column>
        <el-table-column
          label="数据库地址"
          prop="host">
        </el-table-column>
        <el-table-column
          label="端口"
          prop="port">
        </el-table-column>
        <el-table-column
          label="用户名"
          prop="user">
        </el-table-column>
        <el-table-column
          label="环境"
          prop="env">
          <template slot-scope="scope">
            <el-tag type="warning" v-if="scope.row.env === 'test'">测试</el-tag>
            <el-tag type="warning" v-if="scope.row.env === 'ppe'">预发布</el-tag>
            <el-tag type="warning" v-if="scope.row.env === 'prod'">生产</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    </el-card>
  </div>
</template>

<script>
  import { GetDbList } from '@/api/sql/dbs'
  import { ContainsIdList } from '@/utils/base/contains'
  import { GetClusterList, UpdateCluster, CreateCluster, DeleteCluster } from '@/api/sql/cluster'
  export default {
    name: 'cluster',
    data() {
      return {
        spinShow: false,
        labelPosition: 'right',
        dbListModal: false,
        createModal: false,
        updateModal: false,
        // 显示数据库
        showContent: {
          modal: false,
          title: '',
          data: []
        },
        search: '',
        clusterList: [],
        clusterDbList: [],
        dbList: [],
        createClusterForm: {
          name: '',
          remark: ''
        },
        rules: {
          name: [
            { required: true, message: '项目名不能为空', trigger: 'blur' }
          ]
        },
        updateClusterForm: {
          id: '',
          name: '',
          dbs: [],
          dbList: [],
          remark: ''
        },
        deleteParams: {
          id: '',
          name: ''
        },
        getDbParams: {
          page: 1,
          // pagesize: 1000,
          search: ''
        },
        getClusterParams: {
          page: 1,
          totalNum: 0,
          pagesize: 10,
          search: ''
        }
      }
    },
    created() {
      this.initData()
    },
    methods: {
      initData() {
        this.handleGetClusterList()
        this.handleGetDbList()
      },
      handleGetDbList() {
        this.spinShow = true
        GetDbList(this.getDbParams)
          .then(
            res => {
              this.spinShow = false
              this.dbList = res.results
            }
          )
      },
      handleDbListBtn(value) {
        this.clusterDbList = []
        const db_ids = value.dbs
        this.dbList.map((item) => {
          if (ContainsIdList(db_ids, item.id) === true) {
            this.clusterDbList.push(item)
          }
        })

        this.dbListModal = true
      },
      handleAddModal() {
        this.createModal = true
      },
      handleCreateCluster() {
        this.$refs.createClusterForm.validate((valid) => {
          if (!valid) {
            return
          }
          CreateCluster(this.createClusterForm)
            .then(
              res => {
                this.$message({
                  type: 'success',
                  message: '创建集群成功'
                })
                this.createModal = false
                this.initData()
              },
            )
        })
      },
      handleUpdateModal(value) {
        this.updateClusterForm = { ...value }
        this.updateModal = true
      },
      handleUpdateCluster() {
        this.$refs.updateClusterForm.validate((valid) => {
          if (!valid) {
            return
          }
          const id = this.updateClusterForm.id
          const data = this.updateClusterForm
          UpdateCluster(id, data)
            .then(
              res => {
                this.$message.success('修改集群成功')
                this.initData()
                this.updateModal = false
              },
            )
        })
      },
      handleDeleteCluster(value) {
        const id = value.id
        const name = value.name
        this.$confirm(`此操作将删除: ${name}, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          DeleteCluster(id).then(res => {
            this.$message({
              message: '删除集群成功',
              type: 'success'
            })
            this.initData()
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除'
            })
          })
        })
      },
      handleGetClusterList() {
        this.spinShow = true
        GetClusterList(this.getClusterParams)
          .then(
            res => {
              this.spinShow = false
              this.clusterList = res.results
              this.total = res.count
            }
          )
      },
      handleCurrentChange(val) {
        this.getClusterParams.page = val
        this.initData()
      },
      searchClick() {
        this.initData()
      },
      handleCancelAdd() {
        this.createModal = false
        this.$refs.createClusterForm.resetFields()
      },
      handleCancelupdate() {
        this.updateModal = false
        this.$refs.updateClusterForm.resetFields()
      }
    }
  }
</script>

<style scoped>
  .text-center {
    text-align: center;
    margin-top:10px;
  }
</style>

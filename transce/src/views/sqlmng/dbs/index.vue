<template>
  <div class="db">
    <!--搜索-->
    <el-col :span="8" style="margin-bottom: 20px">
      <el-input placeholder="搜索" v-model="params.keywords" @keyup.enter.native="searchClick">
        <el-button slot="append" icon="el-icon-search" @click="searchClick"></el-button>
      </el-input>
    </el-col>

    <!--添加按钮-->
    <el-col :span="16" style="text-align: right">
      <el-button type="primary" @click="handleAddBtn">创建</el-button>
    </el-col>

  <!-- DB table -->
  <db-list :value="db_list" @edit="handleEdit" @delete="handleDelete"></db-list>
  <!-- 添加表单 -->
    <el-dialog
      title="创建数据库配置"
      :visible.sync="dialogVisibleForAdd"
      width="50%">
      <db-form
        ref="DbForm"
        @submit="handleSubmitAdd"
        @cancel="handleCancelAdd">
      </db-form>
    </el-dialog>
  <!-- 修改 -->
    <el-dialog
      title="修改数据库配置"
      :visible.sync="dialogVisibleForEdit"
      width="50%">
      <db-form
        ref="DbForm"
        :form="currentValue"
        @submit="handleSubmitEdit"
        @cancel="handleCancelEdit">
      </db-form>
    </el-dialog>
  <!--分页-->
  <div class="text-center" v-show="totalNum>=10">
    <el-pagination
      background
      layout="total, prev, pager, next, jumper"
      :page-size="pagesize"
      :total="totalNum"
      @current-change="handleCurrentChange">
    </el-pagination>
  </div>
  </div>
</template>

<script>
  import { GetDbList, UpdateDb, CreateDb, DeleteDb } from '@/api/sql/dbs'
  import DbList from './list'
  import DbForm from './form'
  export default {
    name: 'db',
    components: {
      DbForm,
      DbList
    },
    data() {
      return {
        db_list: [],
        currentValue: {},
        params: {
          keywords: '',
          page: 1
        },
        dialogVisibleForAdd: false,
        dialogVisibleForEdit: false,
        totalNum: 0,
        pagesize: 2
      }
    },
    created() {
      this.fetchData()
    },
    methods: {
      fetchData() {
        GetDbList(this.params).then(res => {
          this.db_list = res.results
          this.totalNum = res.count
        })
      },
      handleCurrentChange(val) {
        this.params.page = val
        this.fetchData()
        // console.log(this.params.page)
      },
      searchClick() {
        this.fetchData()
      },
      /* 添加 */
      handleAddBtn() {
        this.dialogVisibleForAdd = true
      },
      handleSubmitAdd(value) {
        console.log(value)
        CreateDb(value).then(res => {
          this.$message({
            message: '创建成功',
            type: 'success'
          })
          this.handleCancelAdd()
          this.fetchData()
        })
      },
      handleCancelAdd() {
        this.dialogVisibleForAdd = false
        this.$refs.CreateFormDb.$refs.form.resetFields() // 清除掉子组件表单的数据
      },
      /* 修改 */
      handleEdit(value) {
        this.currentValue = { ...value }
        this.dialogVisibleForEdit = true
      },
      handleSubmitEdit(value) {
        const data = value
        const id = data.id
        console.log(data)
        if (data.cluster === {}) {
          console.log(data.cluster)
          data.cluster = data.cluster.id
        } else {
          data.cluster = null
        }
        UpdateDb(id, data).then(res => {
          this.$message({
            message: '更新成功',
            type: 'success'
          })
          this.handleCancelEdit()
          this.fetchData()
        })
      },
      handleCancelEdit() {
        this.dialogVisibleForEdit = false
        this.$refs.DbForm.$refs.form.resetFields()
      },
      /* 删除 */
      handleDelete(id) {
        DeleteDb(id).then(res => {
          this.$message({
            message: '删除成功',
            type: 'success'
          })
          this.params.page = 1
          this.fetchData()
        }, err => {
          console.log(err.message)
        })
      }
    }
  }
</script>

<style scoped>
  .db {
    padding: 10px;
  }
  .text-center {
    text-align: center;
    margin-top:10px;
  }
</style>

<template>
  <div class="task">
    <el-card shadow="always">
    <div>
      <!--搜索-->
      <el-col :span="8" style="margin-bottom: 20px">
        <el-input size="small" placeholder="搜索" v-model="params.keywords" @keyup.enter.native="searchClick">
          <el-button size="small" slot="append" icon="el-icon-search" @click="searchClick"></el-button>
        </el-input>
      </el-col>
    </div>

    <!--表格-->
    <task-list :value="tasks" @edit="handleEdit" @detail="handleDetail"></task-list>

    <!--模态窗-->
    <el-dialog
      title="任务详情"
      :visible.sync="dialogVisibleForTask"
      width="70%">
      <div><pre>{{ exce_result }}</pre></div>
    </el-dialog>



    <!--分页-->
    <center>
      <el-pagination
        background
        layout="total, prev, pager, next, jumper"
        :page-size="pagesize"
        :total="totalNum"
        @current-change="handleCurrentChange">
      </el-pagination>
    </center>
    </el-card>
  </div>
</template>

<script>
  import { getBatchTaskList, updateBatchTask, detailBatchTask } from '@/api/task'
  import TaskList from './table'

  export default {
    name: 'task',
    components: {
      TaskList
    },

    data() {
      return {
        dialogVisibleForTask: false,
        tasks: [],
        exce_result: '',
        totalNum: 0,
        pagesize: 10,
        params: {
          page: 1,
          keywords: ''
        }
      }
    },

    created() {
      this.fetchData()
    },

    methods: {
      fetchData() {
        getBatchTaskList(this.params).then(
          res => {
            this.tasks = res.results
            this.totalNum = res.count
          })
      },

      handleCurrentChange(val) {
        this.params.page = val
        this.fetchData()
      },

      searchClick() {
        this.fetchData()
      },

      handleEdit(value) {
        const { id, ...params } = value
        const data = { 'status': 'Y' }
        console.log(params)
        updateBatchTask(id, data).then(res => {
          this.$message({
            message: '执行成功',
            type: 'success'
          })
          this.fetchData()
        })
      },

      /* 详情 */
      handleDetail(id) {
        this.dialogVisibleForTask = true
        detailBatchTask(id).then(
          res => {
            this.exce_result = res.detail_result
            console.log(this.exce_result)
          })
      }
    }

  }

</script>

<style lang='scss' scoped>
  .task {
    padding: 10px;
  }
  pre {
    font-weight: bold;
    color: white;
    font-size: 16px;
    background-color: black;
  }
</style>



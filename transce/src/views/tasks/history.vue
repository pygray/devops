<template>
  <div class="task-result-list">
    <div>
      <el-col :span="8" style="margin-bottom: 20px">
        <el-input placeholder="搜索" v-model="params.keywords" @keyup.enter.native="searchClick">
          <el-button slot="append" icon="el-icon-search" @click="searchClick"></el-button>
        </el-input>
      </el-col>
    </div>
    <el-table
      ref="multipleTable"
      v-loading="loading"
      element-loading-text="拼命加载中"
      :data="resultList"
      tooltip-effect="dark"
      style="margin-bottom: 20px"
      :default-sort = "{prop: 'date_done', order: 'descending'}"
      @selection-change="handleSelectionChange"
      border>
      <el-table-column
        type="selection"
        width="55">
      </el-table-column>
      <el-table-column
        prop="task_id"
        label="任务ID"
        align="center">
      </el-table-column>
      <el-table-column
        prop="status"
        label="状态"
        align="center">
      </el-table-column>
      <el-table-column
        prop="result"
        label="结果"
        align="center">
      </el-table-column>
      <el-table-column
        prop="date_done"
        label="完成时间"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop=""
        label="操作"
        align="center">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleDeleteClick(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="text-align: center">
      <div style="float: left">
      <el-button @click="toggleSelection()">取消选择</el-button>
      <el-button @click="toggleSelectionDelete">批量删除</el-button>
      </div>
      <el-pagination
        background
        @current-change="paginationChange"
        layout="total, prev, pager, next, jumper"
        :current-page.sync="params.page"
        :total="task_result_total_num">
      </el-pagination>
    </div>

  </div>
</template>

<script>
    import { taskResultList, deleteTaskResult } from '@/api/task'
    export default {
      name: 'history',
      data() {
        return {
          resultList: [],
          multipleSelection: [],
          multipleSelectionIdList: [],
          task_result_total_num: 0,
          params: {
            page: 1,
            keywords: ''
          },
          loading: false

        }
      },
      created() {
        this.fetchData()
      },
      methods: {
        fetchData() {
          taskResultList(this.params).then(res => {
            this.resultList = res.results
            this.task_result_total_num = res.count
            this.loading = false
          })
        },
        searchClick() {
          this.params.page = 1
          this.fetchData()
        },
        paginationChange(val) {
          this.params.page = val
          this.fetchData()
        },
        handleSelectionChange(val) {
          this.multipleSelection = val
        },
        toggleSelection(rows) {
          if (rows) {
            rows.forEach(row => {
              this.$refs.multipleTable.toggleRowSelection(row)
            })
          } else {
            console.log(this.$refs)
            this.$refs.multipleTable.clearSelection()
          }
        },
        toggleSelectionDelete() {
          this.$confirm('此操作将删除选择的任务 , 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            const ids = this.multipleSelection.map(item => item.id).join()
            deleteTaskResult(ids).then(response => {
              this.$message({
                message: '删除任务结果成功',
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
        handleDeleteClick(row) {
          this.$confirm('此操作将删除此任务结果 “' + row.task_id + '” , 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            deleteTaskResult(row.id).then(response => {
              this.$message({
                message: '删除任务结果 “' + row.task_id + '” 成功',
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
        }
      }
    }
</script>

<style scoped>

</style>

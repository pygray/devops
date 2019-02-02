<template>
  <div class="task-list">
    <el-card shadow="always">
    <div>
      <el-col :span="8" style="margin-bottom: 20px">
        <el-input size="small" placeholder="搜索" v-model="params.keywords" @keyup.enter.native="searchClick">
          <el-button size="small" slot="append" icon="el-icon-search" @click="searchClick"></el-button>
        </el-input>
      </el-col>
      <div style="float: right">
        <el-button type="primary" @click="addClick" size="small">添加任务</el-button>
      </div>
    </div>
    <el-table
      v-loading="loading"
      element-loading-text="拼命加载中"
      :data="taskList"
      style="margin-bottom: 20px"
      border>
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="table-form-expand">
            <el-form-item label="参数(args): ">
              <span>{{ props.row.args }}</span>
            </el-form-item>
            <el-form-item label="参数(kwargs): ">
              <span>{{ props.row.kwargs }}</span>
            </el-form-item>
            <el-form-item label="过期时间: ">
              <span>{{ props.row.expires }}</span>
            </el-form-item>
            <el-form-item label="备 注: ">
              <span>{{ props.row.description }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="任务名称"
        prop="name"
        align="center">
      </el-table-column>
      <el-table-column
        label="任务模板"
        prop="task"
        align="center">
      </el-table-column>
      <el-table-column
        label="crontab表达式"
        prop="crontabs">
      </el-table-column>
      <el-table-column
        label="详情"
        icon="chart"
        align="center">
        <template slot-scope="scope">
          <i class="el-icon-picture-outline" @click="detailHandleClick(scope.row)"></i>
          <!--<el-button @click="detailHandleClick(scope.row)" icon="chart" ></el-button>-->
        </template>
      </el-table-column>
      <el-table-column
        label="创建用户"
        prop="user"
        align="center">
      </el-table-column>
      <el-table-column
        label="最后一次执行时间"
        prop="last_run_at"
        align="center">
      </el-table-column>
      <el-table-column
        label="执行任务次数"
        prop="total_run_count"
        align="center">
      </el-table-column>
      <el-table-column
        prop="enabled"
        label="任务状态"
        align="center"
        width="78">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.enabled"
            @change="statusChange(scope.row)">
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column
        prop=""
        label="操作"
        align="center">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleEdit(scope.row)">修改</el-button>
          <el-button type="text" size="small" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="text-align: center">
      <el-pagination
        background
        @current-change="paginationChange"
        layout="total, prev, pager, next, jumper"
        :current-page.sync="params.page"
        :total="task_total_num">
      </el-pagination>
    </div>

    <!-- 添加定时task -->
    <el-dialog title="增加定时任务" :visible.sync="addTaskFormVisible">
      <el-form ref="addTaskForm" :model="addTaskForm" label-width="70px" :rules="addTaskRule">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="addTaskForm.name" placeholder="请输入任务名称"></el-input>
        </el-form-item>
        <el-form-item label="任务模板" prop="task">
          <el-select v-model="addTaskForm.task" placeholder="请选择任务模板" style="width:100%" @focus="handleTaskMb">
            <el-option
              v-for="(item, index) in taskRegList"
              :key="index"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="是否启用" prop="enabled">
          <el-checkbox v-model="addTaskForm.enabled"></el-checkbox>
        </el-form-item>
        <el-form-item label="crontab表达式" prop="crontab">
          <el-select v-model="addTaskForm.crontab" placeholder="请选择crontab表达式" style="width:100%" @focus="handleCrontab">
            <el-option
              v-for="(item, index) in crontabsList"
              :key="index"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="参数args" prop="args">
          <el-input type="textarea" v-model="addTaskForm.args" placeholder="[{}]"></el-input>
        </el-form-item>
        <el-form-item label="参数kwargs" prop="kwargs">
          <el-input type="textarea" v-model="addTaskForm.kwargs" placeholder="{}"></el-input>
        </el-form-item>
        <el-form-item label="过期时间" prop="expires">
          <div class="block">
            <el-date-picker
              v-model="addTaskForm.expires"
              type="datetime"
              placeholder="选择日期时间">
            </el-date-picker>
          </div>
        </el-form-item>
        <el-form-item label="备注" prop="description">
          <el-input type="textarea" v-model="addTaskForm.description" placeholder="请输入备注"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addTaskFormVisible = false" size="small">取 消</el-button>
        <el-button type="primary" @click="submitAddClick" size="small">保 存</el-button>
      </div>
    </el-dialog>

    <!-- 修改定时任务 -->
    <el-dialog title="增加定时任务" :visible.sync="editTaskFormVisible">
      <el-form ref="editTaskForm" :model="editTaskForm" label-width="70px" :rules="addTaskRule">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="editTaskForm.name" placeholder="请输入任务名称"></el-input>
        </el-form-item>
        <el-form-item label="任务模板" prop="task">
          <el-select v-model="editTaskForm.task" placeholder="请选择任务模板" style="width:100%" @focus="handleTaskMb">
            <el-option
              v-for="(item, index) in taskRegList"
              :key="index"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="是否启用" prop="enabled">
          <el-checkbox v-model="editTaskForm.enabled"></el-checkbox>
        </el-form-item>
        <el-form-item label="crontab表达式" prop="crontab">
          <el-select v-model="editTaskForm.crontab" placeholder="请选择crontab表达式" style="width:100%" @focus="handleCrontab">
            <el-option
              v-for="(item, index) in testCrontabList"
              :key="index"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="参数args" prop="args">
          <el-input type="textarea" v-model="editTaskForm.args" placeholder="[{}]"></el-input>
        </el-form-item>
        <el-form-item label="参数kwargs" prop="kwargs">
          <el-input type="textarea" v-model="editTaskForm.kwargs" placeholder="{}"></el-input>
        </el-form-item>
        <el-form-item label="过期时间" prop="expires">
          <div class="block">
            <el-date-picker
              v-model="editTaskForm.expires"
              type="datetime"
              placeholder="选择日期时间">
            </el-date-picker>
          </div>
        </el-form-item>
        <el-form-item label="备注" prop="description">
          <el-input type="textarea" v-model="editTaskForm.description" placeholder="请输入备注"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editTaskFormVisible = false" size="small">取 消</el-button>
        <el-button type="primary" @click="submitEditClick" size="small">保 存</el-button>
      </div>
    </el-dialog>
    </el-card>
  </div>
</template>

<script>
  import { getTaskList, updateTask, taskMbList, crontabList, createTask, deleteTask } from '@/api/task'
  export default {
    name: 'task-list',
    data() {
      return {
        taskList: [],
        taskRegList: [],
        crontabsList: [],
        editTaskForm: {},
        task_total_num: 0,
        params: {
          page: 1,
          keywords: ''
        },
        addTaskForm: {
          name: '',
          task: '',
          enabled: false,
          crontab: '',
          args: '',
          kwargs: '',
          expires: null,
          description: ''
        },
        addTaskRule: {
          name: [
            { required: true, message: '请输入任务名称', trigger: 'blur' }
          ],
          task: [
            { required: true, message: '请选择任务模板', trigger: 'blur' }
          ],
          crontab: [
            { required: true, message: '请选择crontab表达式', trigger: 'blur' }
          ]
        },
        loading: false,
        addTaskFormVisible: false,
        editTaskFormVisible: false
      }
    },
    computed: {
      testCrontabList() {
        return [].concat(this.crontabsList)
      }
    },
    created() {
      this.fetchData()
    },
    methods: {
      fetchData() {
        this.loading = true
        getTaskList(this.params).then(res => {
          this.taskList = res.results
          this.task_total_num = res.count
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
      statusChange(row) {
        updateTask(row.id, { name: row.name, task: row.task, enabled: row.enabled }).then(() => {
          this.fetchData()
          this.$message({
            message: '操作成功',
            type: 'success'
          })
        }, err => {
          this.$message({
            message: err.$message,
            type: 'error'
          })
        })
      },
      detailHandleClick(row) {
        console.log(row.id)
      },
      addClick() {
        if (this.$refs['addTaskForm'] !== undefined) {
          this.$refs['addTaskForm'].resetFields()
        }
        this.addTaskFormVisible = true
      },
      handleTaskMb() {
        taskMbList().then(res => {
          this.taskRegList = res
        })
      },
      handleCrontab() {
        crontabList().then(res => {
          this.crontabsList = res.results
        })
      },
      submitAddClick() {
        this.$refs.addTaskForm.validate(valid => {
          if (!valid) {
            return
          }
          createTask(this.addTaskForm).then(res => {
            this.addTaskFormVisible = false
            this.fetchData()
            this.$message({
              message: '操作成功',
              type: 'success'
            })
          })
        })
      },
      handleEdit(row) {
        this.editTaskForm = { ...row }
        this.editTaskFormVisible = true
      },
      submitEditClick() {
        this.$refs['editTaskForm'].validate(valid => {
          if (!valid) {
            return
          }
          console.log(this.editTaskForm)
          updateTask(this.editTaskForm.id, this.editTaskForm).then(response => {
            this.editTaskFormVisible = false
            this.fetchData()
            this.$message({
              message: '操作成功',
              type: 'success'
            })
          })
          this.conrtabID = ''
        })
      },
      handleDelete(row) {
        this.$confirm('此操作将删除此任务 “' + row.name + '” , 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteTask(row.id).then(response => {
            this.$message({
              message: '删除任务 “' + row.name + '” 成功',
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

<style lang="scss" scoped>
  .table-form-expand {
    font-size: 0;
  }
  .table-form-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .table-form-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
  .task-list {
    padding: 10px;
  }
</style>

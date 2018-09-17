<template>
    <div class="crontabs">
      <div>
        <div style="float: right;margin-bottom: 20px">
          <el-button type="primary" @click="addClick">添加表达式</el-button>
        </div>
      </div>
      <el-table
        v-loading="loading"
        element-loading-text="拼命加载中"
        :data="crontabsList"
        style="margin-bottom: 20px"
        border>
        <el-table-column
          type="index"
          width="50">
        </el-table-column>
        <el-table-column
          prop="name"
          label="表达式"
          align="center">
        </el-table-column>
        <el-table-column
          prop=""
          label="操作"
          align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleEditClick(scope.row)">修改</el-button>
            <el-button type="text" size="small" @click="handleDeleteClick(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="text-align: center">
        <el-pagination
          background
          @current-change="paginationChange"
          layout="total, prev, pager, next, jumper"
          :current-page.sync="params.page"
          :total="crontab_total_num">
        </el-pagination>
      </div>

      <!-- 添加crontab表达式 -->
      <el-dialog title="增加crontab表达式" :visible.sync="addCrontabFormVisible">
        <el-form ref="addCrontabForm" :model="addCrontabForm" label-width="120px" :rules="addCrontabRule">
          <el-form-item label="minute: " prop="minute">
            <el-input v-model="addCrontabForm.minute" placeholder="*"></el-input>
          </el-form-item>
          <el-form-item label="hour: " prop="hour">
            <el-input v-model="addCrontabForm.hour" placeholder="*"></el-input>
          </el-form-item>
          <el-form-item label="day_of_week: " prop="day_of_week">
            <el-input v-model="addCrontabForm.day_of_week" placeholder="*"></el-input>
          </el-form-item>
          <el-form-item label="day_of_month: " prop="day_of_month">
            <el-input v-model="addCrontabForm.day_of_month" placeholder="*"></el-input>
          </el-form-item>
          <el-form-item label="month_of_year: " prop="month_of_year">
            <el-input v-model="addCrontabForm.month_of_year" placeholder="*"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="addCrontabFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitAddClick">保 存</el-button>
        </div>
      </el-dialog>

      <!-- 修改crontab表达式 -->
      <el-dialog title="修改crontab表达式" :visible.sync="editCrontabFormVisible">
        <el-form ref="editCrontabForm" :model="editCrontabForm" label-width="120px" :rules="addCrontabRule">
          <el-form-item label="minute: " prop="minute">
            <el-input v-model="editCrontabForm.minute" placeholder="*"></el-input>
          </el-form-item>
          <el-form-item label="hour: " prop="hour">
            <el-input v-model="editCrontabForm.hour" placeholder="*"></el-input>
          </el-form-item>
          <el-form-item label="day_of_week: " prop="day_of_week">
            <el-input v-model="editCrontabForm.day_of_week" placeholder="*"></el-input>
          </el-form-item>
          <el-form-item label="day_of_month: " prop="day_of_month">
            <el-input v-model="editCrontabForm.day_of_month" placeholder="*"></el-input>
          </el-form-item>
          <el-form-item label="month_of_year: " prop="month_of_year">
            <el-input v-model="editCrontabForm.month_of_year" placeholder="*"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="editCrontabFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitEditClick">保 存</el-button>
        </div>
      </el-dialog>

    </div>
</template>

<script>
  import { crontabList, deleteCrontabs, createCrontabs, updateCrontabs } from '@/api/task'
  export default {
    name: 'crontabs',
    data() {
      return {
        crontabsList: [],
        editCrontabForm: {},
        crontab_total_num: 0,
        loading: false,
        addCrontabFormVisible: false,
        editCrontabFormVisible: false,
        params: {
          page: 1,
          keywords: ''
        },
        addCrontabForm: {
          minute: '',
          hour: '',
          day_of_week: '',
          day_of_month: '',
          month_of_year: ''
        },
        addCrontabRule: {
          minute: [
            { required: true, message: '请输入minute', trigger: 'blur' }
          ],
          hour: [
            { required: true, message: '请输入hour', trigger: 'blur' }
          ],
          day_of_week: [
            { required: true, message: '请输入day_of_week', trigger: 'blur' }
          ],
          day_of_month: [
            { required: true, message: '请输入day_of_month', trigger: 'blur' }
          ],
          month_of_year: [
            { required: true, message: '请输入month_of_year', trigger: 'blur' }
          ]
        }
      }
    },
    created() {
      this.fetchData()
    },
    methods: {
      fetchData() {
        this.loading = true
        crontabList(this.params).then(res => {
          this.crontabsList = res.results
          this.crontab_total_num = res.count
          this.loading = false
        })
      },
      paginationChange(val) {
        this.params.page = val
        this.fetchData()
      },
      addClick() {
        this.addCrontabFormVisible = true
        if (this.$refs['addCrontabForm'] !== undefined) {
          this.$refs['addCrontabForm'].resetFields()
        }
      },
      submitAddClick() {
        this.$refs.addCrontabForm.validate(valid => {
          if (!valid) {
            return
          }
          createCrontabs(this.addCrontabForm).then(res => {
            this.addCrontabFormVisible = false
            this.fetchData()
            this.$message({
              message: '操作成功',
              type: 'success'
            })
          })
        })
      },
      handleEditClick(row) {
        this.editCrontabForm = { ...row }
        this.editCrontabFormVisible = true
      },
      submitEditClick() {
        this.$refs['editCrontabForm'].validate(valid => {
          if (!valid) {
            return
          }
          updateCrontabs(this.editCrontabForm.id, this.editCrontabForm).then(response => {
            this.editCrontabFormVisible = false
            this.fetchData()
            this.$message({
              message: '操作成功',
              type: 'success'
            })
          })
        })
      },
      handleDeleteClick(row) {
        this.$confirm('此操作将删除此表达式 “' + row.name + '” , 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteCrontabs(row.id).then(response => {
            this.$message({
              message: '删除任务结果 “' + row.name + '” 成功',
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

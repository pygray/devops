<template>
  <div>
    <div>
      <el-row :gutter="20">
        <el-col :span="16">
        <div style="height:400px;">
          <el-scrollbar class="el-scrollbar-class">
            <div>
              <el-table
                :data="results"
                style="width: 100%"
                >
                <el-table-column
                label="时间"
                >
                <template slot-scope="scope">
                  <div>{{ scope.row.createtime.split('.')[0].replace('T',' ') }}</div>
                </template>
                </el-table-column>
                <el-table-column
                  label="用户"
                  prop="username">
                </el-table-column>
              <el-table-column
                label="意见"
                prop="remark"
              ></el-table-column>
              </el-table>
            </div>
              <!-- 分页 -->
              <div class="text-center">
                <el-pagination
                  background
                  layout="total, prev, pager, next, jumper"
                  :page-size="pagesize"
                  :total="count"
                  @current-change="handleCurrentChange">
                </el-pagination>
              </div>
          </el-scrollbar>
        </div>
        </el-col>
        <el-col :span="8">
          <el-form class="step-form" ref="checkSuggestion" :model="suggestionData" :rules="ruleSuggestionData" label-width="100">
            <el-form-item label="审批意见" prop="remark">
              <el-input v-model="suggestionData.remark" type="textarea" :rows="6" placeholder="请输入审批意见..."></el-input>
            </el-form-item>
            <el-form-item label="操作">
              <el-button type="primary" @click="handleCommit" size="small">发表意见</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  import ElPager from 'element-ui/packages/pagination/src/pager'
  import { GetSuggestionList, CreateSuggestion } from '@/api/sql/suggestion'
  export default {
    props: ['id'],
    components: { ElPager },
    data() {
      return {
        state: 0,
        showHeader: false,
        page: 1,
        count: 1,
        pagesize: 10,
        results: [],
        suggestionData: {
          remark: ''
        },
        res: {},
        ruleSuggestionData: {
          remark: [{ required: true, message: '请输入审批意见', trigger: 'blur' }]
        }
      }
    },
    watch: {
      state() {
        this.handleGetList(this.page)
      }
    },
    created() {
      this.state = 1
    },
    methods: {
      refreshList(page) {
        this.$emit('refreshList', page)
        this.handleGetList(this.page)
      },
      handleCurrentChange(val) {
        this.page = val
        this.handleGetList(this.page)
      },
      // getData() {
      //   if (JSON.stringify(this.res) !== '{}') {
      //     this.count = this.res.count
      //     this.results = this.res.results
      //     console.log(this.res)
      //   }
      // },
      handleGetList() {
        const params = { page: this.page, pagesize: 10, work_order_id: this.$route.params.id }
        GetSuggestionList(params)
          .then(
            response => {
              this.results = response.results
              this.count = response.count
            }
          )
      },
      handleCommit() {
        this.$refs.checkSuggestion.validate((valid) => {
          if (!valid) {
            return
          }
          const data = this.suggestionData
          data.work_order = this.id
          CreateSuggestion(data)
            .then(response => {
              this.refreshList()
            })
        })
      }
    }
  }
</script>

<style scoped>
  .inner {
    margin-bottom:10px
  }
  .el-scrollbar-class {
    height: 100%;
    overflow: scroll;
    overflow-x: hidden;
  }
</style>

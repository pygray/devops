<template>
  <div class="inception-list" style="padding: 10px;color: white">
    <!--搜索-->
    <el-col :span="8" style="margin-bottom: 20px">
      <el-input placeholder="搜索" v-model="getParams.search" size="small" @keyup.enter.native="handleGetSqlList">
        <el-button slot="append" icon="el-icon-search" size="small" @click="handleGetSqlList"></el-button>
      </el-input>
    </el-col>
    <!-- 日期搜索 -->
    <el-col :span="4" :offset="1">
      <div class="block" >
        <el-date-picker
          v-model="getParams.daterange"
          type="datetimerange"
          :picker-options="dateOption"
          @change="dateChange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          align="right"
          size="small">
        </el-date-picker>
      </div>
    </el-col>
    <!--table-->
    <el-table
      :data="sqlList"
      style="width: 100%">
      <el-table-column
        label="ID">
        <template slot-scope="scope">
          <router-link :to="'/inceptionsql/' + scope.row.id + '/'"><el-button type="text">{{ scope.row.id }}</el-button></router-link>
        </template>
      </el-table-column>
      <el-table-column
        prop="createtime"
        label="提交时间"
        :formatter="formatterDate">
      </el-table-column>
      <el-table-column
        prop="commiter"
        label="发起人">
      </el-table-column>
      <el-table-column
        label="环境">
        <template slot-scope="scope">
          <el-tag type="info" v-if="scope.row.env === 'test'">测试</el-tag>
          <el-tag v-if="scope.row.env === 'ppe'">预发布</el-tag>
          <el-tag type="warning" v-if="scope.row.env === 'prod'">生产</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="db_name"
        label="目标库">
      </el-table-column>
      <el-table-column
        label="SQL语句">
        <template slot-scope="scope">
          <span>{{ scope.row.sql_content.slice(0,6) }} ... <el-button ty size="mini" style="float: right"
                                                                      @click="handleGetSqlContent(scope.row)">语句</el-button></span>
        </template>
      </el-table-column>
      <el-table-column
        prop="steps"
        label="流程">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleGetSteps(scope.row)">流程</el-button>
          <el-badge :value="handleGetStepsNum(scope.row.steps).count"
                    :type="statusMap[handleGetStepsNum(scope.row.steps).badgeStatus]"></el-badge>
        </template>
      </el-table-column>
      <el-table-column
        prop="remark"
        label="备注">
      </el-table-column>
      <el-table-column
        label="工单状态">
        <template slot-scope="scope">
          <el-tag color="red" size="small" v-if="scope.row.status === -4"><font color="white">回滚失败</font></el-tag>
          <el-tag size="small" color="mediumorchid" v-if="scope.row.status === -3"><font color="white">已回滚</font></el-tag>
          <el-tag size="small" v-if="scope.row.status === -2"><font color="white">已暂停</font></el-tag>
          <el-tag color="#3a8ee6" type="info" size="small" v-if="scope.row.status === -1" style=""><font color="white">待执行</font>
          </el-tag>
          <el-tag color="green" size="small" v-if="scope.row.status === 0"><font color="white">成功</font></el-tag>
          <el-tag color="sandybrown" size="small" v-if="scope.row.status === 1"><font color="white">已放弃</font></el-tag>
          <el-tag color="red" size="small" v-if="scope.row.status === 2"><font color="white">任务失败</font></el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="treater"
        label="核准人">
      </el-table-column>
      <el-table-column
        label="操作">
        <template slot-scope="scope">
          <div
            v-show="scope.row.status !== -4 || scope.row.status !== -3 || scope.row.status !== 1 || (scope.row.status !== 0 && scope.row.type !== 'select') || (scope.row.status !== 0 && scope.row.rollbackable !== 0)">
            <el-dropdown trigger="click">
              <el-button type="primary" size="mini">
                操作<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <div v-if="scope.row.status === -1">
                  <el-dropdown-item  @click.native="handleAction('execute', scope.row)">
                    执行
                  </el-dropdown-item>
                  <el-dropdown-item  @click.native="handleAction('reject', scope.row)">
                    放弃
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="scope.row.is_manual_review === false || scope.row.handleable || scope.row.status === -2"
                    @click.native="handleAction('approve', scope.row)">审核通过
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="scope.row.is_manual_review === false || scope.row.handleable || scope.row.status === -2"
                    @click.native="handleAction('disapprove', scope.row)">审核驳回
                  </el-dropdown-item>
                </div>
                <div v-if="scope.row.status === 0 && scope.row.type !== 'select'">
                  <el-dropdown-item @click.native="handleAction('rollback', scope.row)">回滚</el-dropdown-item>
                </div>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <div class="text-center">
      <el-pagination
        background
        layout="total, prev, pager, next, jumper"
        :page-size="getParams.pagesize"
        :total="total"
        @current-change="handleCurrentChange">
      </el-pagination>
    </div>

    <!-- SQL语句内容 -->
    <el-dialog
      :title="sqlContentTitle"
      :visible.sync="sqlContentModal"
      width="30%">
      <div style="height:400px;">
        <el-scrollbar class="el-scrollbar-class">
          <div v-for="(item, index) in sqlContent" :value="item.value" :key="index">{{ item.value }}</div>
        </el-scrollbar>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="sqlContentModal = false" size="small">取 消</el-button>
        <el-button type="primary" @click="sqlContentModal = false" size="small">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 流程 -->
    <el-dialog
      :title="stepsModalTitle"
      :visible.sync="stepsModal"
      width="40%">
      <div style="height:400px;">
        <el-scrollbar class="el-scrollbar-class">
          <el-steps direction="vertical" :active="1" space="100px">
            <el-step v-for="(item, index) in steps" :value="item.value" :title="item.username" :key="index">
              <template slot="description">
                <div v-for="(item, index) in steps">
                  <p>
                    <font color="black">{{ item.updatetime.split('.')[0].replace('T', ' ') }}</font>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <el-tag size="mini" :color="getColor(item.status)">
                      <font color="white">{{ stepStatusMap[item.status].desc }}</font>
                    </el-tag>
                  </p>
                </div>
              </template>
            </el-step>
          </el-steps>
        </el-scrollbar>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="stepsModal = false" size="small">取 消</el-button>
        <el-button type="primary" @click="stepsModal = false" size="small">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import { GetSqlList, SqlAction } from '@/api/sql/inception'
  import { getSqlContent } from '@/utils/sql/inception'
  import { addDate } from '@/utils/base/date'
  import { handleBadgeData } from '@/utils/sql/inception'
  import baseData from '@/utils/sql/data'

  export default {
    filters: {
      formatTime: function(value) {
        if (value !== '') {
          return value.slice(0, 19).replace('T', ' ')
        }
      }
    },
    computed: {},
    data() {
      return {
        spinShow: false,
        steps: [],
        stepsModal: false,
        stepsModalTitle: '',
        stepStatusMap: {
          '-1': { color: 'gray', desc: '终止', stepStatus: 'wait' },
          0: { color: 'gray', desc: '待处理' },
          1: { color: 'limegreen', desc: '通过' },
          2: { color: 'red', desc: '驳回' },
          3: { color: 'red', desc: '放弃' }
        },
        statusMap: {
          1: 'success',
          2: 'warning'
        },
        total: 1,
        getParams: {
          page: 1,
          pagesize: 10,
          search: '',
          daterange: ''
        },
        sqlContentTitle: '',
        sqlContent: [],
        sqlContentModal: false,
        sqlList: [],
        dateOption: baseData.dateOption
      }
    },
    created() {
      this.handleGetSqlList(this.getParams)
    },
    methods: {
      handleGetStepsNum(steps) {
        const badgeData = handleBadgeData(steps)
        return badgeData
      },
      handleGetSteps(value) {
        const data = value
        const steps = data.steps
        this.steps = steps
        this.stepsModalTitle = `工单流程 (工单ID: ${data.id})`
        this.stepsModal = true
      },
      handleGetSqlContent(value) {
        const data = value
        this.sqlContentTitle = `SQL语句 (工单ID: ${data.id})`
        this.sqlContent = getSqlContent(data.sql_content)
        this.sqlContentModal = true
      },
      formatterDate(row, column) {
        return row.createtime.split('.')[0].replace('T', ' ')
      },
      getColor(status) {
        return this.stepStatusMap[status]['color']
      },
      alertSuccess(title, paramId, execute_time, affected_rows) {
        const h = this.$createElement
        const id = h('p', {}, 'ID：' + paramId)
        const time = execute_time ? h('p', {}, '耗时（秒）：' + execute_time) : ''
        const rows = affected_rows ? h('p', {}, '影响的行数：' + affected_rows) : ''
        const subtags = [id, time, rows]
        const msg = h('div', subtags)
        this.$notify.success({
          title: title,
          dangerouslyUseHTMLString: true,
          message: msg
        })
      },
      alertWarning(title, paramId) {
        const h = this.$createElement
        const id = h('p', {}, 'ID：' + paramId)
        const desc = h('p', {}, '具体查看工单详情[inception结果]')
        const subTags = [id, desc]
        const msg = h('div', subTags)
        this.$notify.error({
          title: title,
          duration: 0,
          dangerouslyUseHTMLString: true,
          message: msg
        })
      },
      getDatetime() {
        const date = this.userInfo.date_joined || ''
        return date.slice(0, 19).replace('T', ' ')
      },
      handleGetSqlList() {
        this.spinShow = true
        GetSqlList(this.getParams)
          .then(response => {
            this.spinShow = false
            this.sqlList = response.results
            this.total = response.count
          })
      },
      handleAction(command, params) {
        const id = params.id
        SqlAction(id, command)
          .then(response => {
            const status = response.status
            const data = response.data
            if (status === 0) {
              if (command === 'execute') {
                this.alertSuccess('执行成功', id, data.execute_time, data.affected_rows)
              } else if (command === 'rollback') {
                this.alertSuccess('回滚成功', id, '', data.affected_rows)
              } else if (command === 'approve') {
                this.alertSuccess('审批通过', id, '')
              } else if (command === 'disapprove') {
                this.alertSuccess('审批驳回', id, '')
              }
            } else {
              this.alertWarning('任务失败', id)
            }
            this.handleGetSqlList()
          })
      },
      cancel() {},
      handleCurrentChange(val) {
        this.getParams.page = val
        this.handleGetSqlList()
      },
      // pageChange(page) {
      //   this.getParams.page = page
      //   this.handleGetSqlList()
      // },
      // sizeChange(size) {
      //   this.getParams.pagesize = size
      //   this.handleGetSqlList()
      // },
      dateChange(data) {
        console.log(data)
        if (data[0]) {
          this.getParams.daterange = addDate(data[0], 1) + ',' + addDate(data[1], 1)
          this.handleGetSqlList()
        }
      }
      // dateClear(data) {
      //   console.log(data)
      // }
    }
  }
</script>

<style scoped>
  .text-center {
    text-align: center;
    margin-top:10px;
    color: white;
  }
  .el-scrollbar-class {
    height: 100%;
    overflow: scroll;
    overflow-x: hidden;
  }
  .test {
    color: mediumorchid;
  }
</style>

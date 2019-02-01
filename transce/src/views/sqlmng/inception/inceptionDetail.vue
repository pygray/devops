<template>
  <div style="padding: 20px">
    <div style="margin-bottom: 20px">
    <el-tabs size="small">
      <el-tab-pane label="基本信息"><base-info v-if="flag" :row="row"></base-info></el-tab-pane>
      <el-tab-pane label="SQL语句"><sql-content-info v-if="flag" :sqlContent="sqlContent"></sql-content-info></el-tab-pane>
      <el-tab-pane :label="labelResult">
        <handle-result
          v-if="flag"
          :row="row"
          :handleResultCheck="handle_result_check"
          :handleResultExecute="handle_result_execute"
          :handleResultRollback="handle_result_rollback">
        </handle-result></el-tab-pane>
        <el-tab-pane label="审核意见" name="suggestion">
          <suggestion-info @refreshList="handleGetList" :id="this.$route.params.id" :res="res"></suggestion-info>
        </el-tab-pane>
    </el-tabs>
    </div>


    <div style="margin-bottom: 30px" v-if="is_has_flow(row)">
      <el-alert title="" show-icon>工单流</el-alert>
      <el-steps :current="stepCurrent" :status="stepCurrentStatus">
        <el-step v-for="(item, index) in stepList" :title="item.title" :content="item.content" :key="index"> </el-step>
      </el-steps>
    </div>


    <div class="inner">
      <el-alert title=""  show-icon :closable="false" size="small">操作</el-alert>
    </div>
      <el-row :gutter="20" class="inner">
        <el-col :span="24">
          <el-dropdown v-show="showBtn" @command="showAction" trigger="click">
            <el-button type="primary" size="small">
              操作 <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item v-show="row.status === -1" command='execute'>执行</el-dropdown-item>
              <el-dropdown-item v-show="row.status === -1" command='reject'>放弃</el-dropdown-item>
              <el-dropdown-item v-show="row.status === -1 && showItem" command='approve'>审批通过</el-dropdown-item>
              <el-dropdown-item v-show="row.status === -1 && showItem" command='disapprove'>审批驳回</el-dropdown-item>
              <el-dropdown-item v-show="row.status === 0" command='rollback'>回滚</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-col>
      </el-row>

    <el-dialog
      :visible.sync="modalAction.show"
      width="10%"
      title="SQL操作">
      <div>
        <center> {{ modalAction.content }} </center>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancel" size="small">取 消</el-button>
        <el-button type="primary" size="small" @click="handleAction">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :visible.sync="stepsModal"
      width="40%"
      title="流程">
      <div>
        <el-scrollbar height=450>
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
        </el-scrollbar>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import { GetSuggestionList } from '@/api/sql/suggestion'
  import { GetSqlDetail, SqlAction } from '@/api/sql/inception'
  import { getSqlContent, handleBadgeData } from '@/utils/sql/inception'
  import baseInfo from './components/baseInfo'
  import sqlContentInfo from './components/sqlContentInfo'
  import handleResult from './components/handleResult'
  import suggestionInfo from './components/suggestionInfo'
  export default {
    components: { suggestionInfo, sqlContentInfo, baseInfo, handleResult },
    filters: {
      formatTime: function(value) {
        if (value !== '') {
          return value.slice(0, 19).replace('T', ' ')
        }
      }
    },
    data() {
      return {
        flag: false,
        title_yj: '',
        stepList: [],
        stepCurrent: 0,
        stepCurrentStatus: 'finish',
        res: {},
        count: '',
        row: {},
        handle_result_check: [],
        handle_result_execute: [],
        handle_result_rollback: [],
        sqlContent: [],
        steps: [],
        stepsModal: false,
        stepStatusMap: {
          '-1': { color: 'gray', desc: '终止', stepStatus: 'wait' },
          0: { color: 'gray', desc: '待处理', stepStatus: 'wait' },
          1: { color: 'green', desc: '通过', stepStatus: 'finish' },
          2: { color: 'red', desc: '驳回', stepStatus: 'error' },
          3: { color: 'red', desc: '放弃', stepStatus: 'error' }
        },
        badgeData: { count: '', badgeStatus: '' },
        modalAction:
          {
            show: false,
            id: '',
            action: '',
            content: ''
          },
        descMap: {
          execute: { name: '执行' },
          reject: { name: '放弃' },
          rollback: { name: '回滚' },
          approve: { name: '审批通过' },
          disapprove: { name: '审批驳回' }
        }
      }
    },
    created() {
      this.handleGetSqlDetail()
    },
    computed: {
      showBtn: function() {
        if (this.row.status === -4 || this.row.status === -3 || this.row.status === 1 || (this.row.type === 'select' && this.row.status === 0) || this.row.rollback_able === 0) {
          return false
        } else {
          return true
        }
      },
      showItem: function() {
        const row = this.row
        if (row.is_manual_review === true && row.env === 'prod' && row.status !== -2 && row.handleable === false) {
          return true
        } else {
          return false
        }
      },
      env: function() {
        if (this.row.env === 'prod') {
          return '生产'
        } else if (this.row.env === 'ppe') {
          return '预发布'
        } else if (this.row.env === 'test') {
          return '测试'
        }
      },
      labelResult: function() {
        if (this.row.type === 'select') {
          return '查询结果'
        } else {
          return 'Inception结果'
        }
      }
    },
    methods: {
      cancel() {
        this.$message.info('Clicked cancel')
        this.modalAction.show = false
      },
      showStep() {
        this.stepsModal = true
      },
      getColor(status) {
        return this.stepStatusMap[status]['color']
      },
      is_has_flow(row) {
        const env = row.env
        const is_manual_review = row.is_manual_review
        if (env === 'prod' && is_manual_review === true) {
          return true
        } else if (env === 'ppe' && is_manual_review === true) {
          return true
        } else {
          return false
        }
      },
      handleGetList(page) {
        const params = { page: page, pagesize: 10, work_order_id: this.$route.params.id }
        GetSuggestionList(params)
          .then(
            response => {
              this.res = response
              this.count = response.count
            }
          )
      },
      alertSuccess(title, sqlid, execute_time, affected_rows) {
        const h = this.$createElement
        const id = h('p', {}, 'ID：' + sqlid)
        const time = execute_time ? h('p', {}, '耗时（秒）：' + execute_time) : ''
        const rows = affected_rows ? h('p', {}, '影响的行数：' + affected_rows) : ''
        const subtags = [id, time, rows]
        const msg = h('div', subtags)
        this.$notify.success({
          dangerouslyUseHTMLString: true,
          title: title,
          message: msg
        })
      },
      alertWarning(title, paramId) {
        const h = this.$createElement
        const id = h('p', {}, 'ID：' + paramId)
        const desc = h('p', {}, '具体查看工单详情[inception结果]')
        const subTags = [id, desc]
        const msg = h('div', subTags)
        this.$notify.warning({
          title: title,
          duration: 0,
          message: msg
        })
      },
      showAction(command) {
        this.modalAction.id = this.row.id
        this.modalAction.action = command
        this.modalAction.show = true
        this.modalAction.content = this.descMap[command].name + ' 工单?'
      },
      getStepData() {
        if (this.is_has_flow(this.row) === false) {
          return false
        }
        let current = -1
        this.stepList = []
        for (const i in this.steps) {
          const item = this.steps[i]
          const statusCode = item.status
          if (statusCode !== 0 && statusCode !== -1) {
            current += 1
          }
          const desc = ' [' + this.stepStatusMap[statusCode]['desc'] + '] '
          const dateTime = item.updatetime.split('.')[0].replace('T', ' ')
          this.stepList.push(
            {
              title: item.group,
              content: item.username + desc + dateTime
            }
          )
        }
        this.stepCurrent = current
        const currentStatus = this.steps[current].status
        this.stepCurrentStatus = this.stepStatusMap[currentStatus]['stepStatus'] // 数字转换成组件状态
      },
      parseHandleResult(handle_result) {
        if (handle_result === '') {
          return
        }
        const data = JSON.parse(handle_result)
        const ret = []
        for (const i in data) {
          ret.push(
            {
              value: JSON.stringify(data[i])
            }
          )
        }
        return ret
      },
      handleAction() {
        const id = this.modalAction.id
        const action = this.modalAction.action
        SqlAction(id, action)
          .then(response => {
            const status = response.status
            const data = response.data
            if (status === 0) {
              if (action === 'execute') {
                this.alertSuccess('执行成功', id, data.execute_time, data.affected_rows)
              } else if (action === 'rollback') {
                this.alertSuccess('回滚成功', id, '', data.affected_rows)
              } else if (action === 'approve') {
                this.alertSuccess('审批通过', id, '', '')
              } else if (action === 'disapprove') {
                this.alertSuccess('审批驳回', id, '', '')
              }
              this.modalAction.show = false
              this.handleGetSqlDetail()
            } else {
              // const msg = response.data.msg
              this.alertWarning('任务失败', id)
            }
          })
      },
      handleGetSqlDetail() {
        GetSqlDetail(this.$route.params.id)
          .then(response => {
            this.row = response
            this.steps = this.row.steps
            this.handle_result_check = this.parseHandleResult(this.row.handle_result_check)
            this.handle_result_execute = this.parseHandleResult(this.row.handle_result_execute)
            this.handle_result_rollback = this.parseHandleResult(this.row.handle_result_rollback)
            this.sqlContent = getSqlContent(this.row.sql_content)
            this.badgeData = handleBadgeData(this.steps)
            this.handleGetList(1)
            this.getStepData()
            this.flag = true
          })
      }
    }
  }
</script>

<style scoped>
  .inner {
    margin-bottom:20px
  }
</style>

<template>
  <div class="platformSettings">
    <el-card shadow="always">
    <el-row :gutter="30">
      <el-col :span="12">
        <el-form label-width="100px">
          <div class="mig">
        <el-alert title="SQL审核" :closable="false" show-icon></el-alert>
          </div>
        <el-form-item label="SQL条数限制" label-width="100px">
          <el-slider v-model="sqlsettings.sql_count_limit" :max="20000"></el-slider>
        </el-form-item>
          <el-form-item label="SQL禁用语" label-width="100px">
            <el-input v-model="sqlsettings.forbidden_words" :readonly="readonly" type="textarea" :rows="3" placeholder="SQL语句里不允许出现的词，多个以空格分隔"></el-input>
          </el-form-item>
          <el-form-item label-width="100px" label="操作">
            <el-button size="small" type="warning" v-show="readonly === true" @click="editHandle">编辑</el-button>
            <el-button size="small" type="primary" v-show="readonly === false" @click="saveHandle">保存</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="12">
        <div style="margin-left:20px">
          <el-alert title="" type="warning" show-icon :closable="false">
            <b>SQL审核设置</b>
              <p class="left20">
                <b>1</b>. 限制每个工单的SQL语句数量；默认1000，最大可设置10000。
              </p>
              <p class="left20">
                <b>2</b>. 可指定不允许语句中出现的词，对包含禁词的SQL语句，后端会做拦截处理。
              </p>
          </el-alert>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="mig">
          <el-alert title="工单流" show-icon :closable="false"></el-alert>
        </div>
        <el-form label-width="100px">
          <el-form-item label="工单流">
            <el-switch size="large" v-model="strategy.is_manual_review" @change="handleWriteStrategy">
              <span slot="open">开启</span>
              <span slot="close">关闭</span>
            </el-switch>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="12">
        <div style="margin-left:20px">
        <el-alert title="" type="warning" show-icon :closable="false">
          <b>工单流设置</b>
          <p style="margin-left:20px">
            <b>1</b>. 关闭，工单流: 提交人 --- 核准人 。
          </p>
          <p style="margin-left:20px">
            <b>2</b>. 开启，工单流: 提交人 --- 核准人 --- 管理员 。
          </p>
        </el-alert>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="mig">
        <el-alert title="邮件提醒" show-icon :closable="false">邮件提醒</el-alert>
        </div>
        <el-form label-width="100px">
          <el-form-item label="选择事件">
            <el-checkbox :indeterminate="indeterminate" v-model="checkAll" @change="handleCheckAll">全选</el-checkbox>
            <div style="margin: 15px 0;"></div>
            <el-checkbox-group v-model="actions_checked" @change="checkAllGroupChange">
              <el-checkbox  v-for="m in mail_events" :label="m" :key="m"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="操作">
            <el-button type="primary" size="small" @click="handleSetMailActions">提交</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="12">
        <div class="left20">
          <el-alert title="" type="warning" show-icon :closable="false">
            <b>邮件提醒设置</b>
            <p class="left20">
              &nbsp;&nbsp; 对于生产环境的数据库，发生选择的事件时，工单相关人员将收到邮件提醒。
            </p>
          </el-alert>
        </div>
      </el-col>
    </el-row>
    </el-card>
  </div>
</template>

<script>
  import { GetStrategyList, UpdateStrategy, CreateStrategy } from '@/api/sql/strategy'
  import { GetFWList, UpdateFW, CreateFW } from '@/api/sql/sqlsettings'
  import { GetMailActions, SetMailActions } from '@/api/sql/mailactions'
  import { getUserList } from '@/api/account'
  const mail_events = ['审核', '放弃', '执行', '回滚', '审批通过', '审批拒绝']
  export default {
    // name: 'platformSettings',
    data() {
      return {
        readonly: true,
        res: [],
        actions: [],
        indeterminate: true,
        checkAll: false,
        mail_events: mail_events,
        actions_checked: [],
        sqlsettings: {
          id: '',
          sql_count_limit: 0,
          forbidden_words: ''
        },
        userList: [],
        strategy: {
          id: '',
          is_manual_review: false
        },
        getParams: {
          page: 1,
          pagesize: 10
        }
      }
    },
    created() {
      this.handleGetUsers()
      this.handleGetFWList()
      this.handleGetStrategyList()
      this.handleGetMailActions()
    },
    methods: {
      handleCheckAll(val) {
        this.actions_checked = val ? mail_events : []
        this.indeterminate = false
        // if (this.indeterminate) {
        //   this.checkAll = false
        // } else {
        //   this.checkAll = !this.checkAll
        // }
        // this.indeterminate = false
        // if (this.checkAll) {
        //   this.actions_checked = this.actions
        // } else {
        //   this.actions_checked = []
        // }
      },
      checkAllGroupChange(data) {
        if (data.length === this.actions.length) {
          this.indeterminate = false
          this.checkAll = true
        } else if (data.length > 0) {
          this.indeterminate = true
          this.checkAll = false
        } else {
          this.indeterminate = false
          this.checkAll = false
        }
      },
      getActionName() {
        const actions_checked = []
        for (const i in this.actions_checked) {
          const item = this.actions_checked[i]
          for (const j in this.res) {
            const row = this.res[j]
            if (row.desc_cn === item) {
              actions_checked.push(row.name)
              break
            }
          }
        }
        return actions_checked
      },
      handleGetMailActions() {
        GetMailActions(this.getParams)
          .then(
            response => {
              this.res = response.results
              this.actions = []
              this.actions_checked = []
              for (const i in this.res) {
                const item = this.res[i]
                this.actions.push(item.desc_cn)
                if (item.value === true) {
                  this.actions_checked.push(item.desc_cn)
                }
              }
            }
          )
      },
      handleSetMailActions() {
        const data = this.getActionName()
        SetMailActions(data)
          .then(
            response => {
              this.handleNotice(response)
            })
      },
      notice(msg) {
        this.$message.success(msg)
      },
      handleNotice(response) {
        // const httpstatus = response.status
        // if (httpstatus === 200 || httpstatus === 201) {
        //   const msg = '设置 保存成功'
        //   this.notice(msg)
        // }
        const msg = '设置 保存成功'
        this.notice(msg)
      },
      editHandle() {
        this.readonly = false
      },

      saveHandle() {
        this.readonly = true
        this.handleWriteFW()
      },
      handleGetStrategyList() {
        GetStrategyList({})
          .then(
            response => {
              const results = response.results
              if (results.length > 0) {
                this.strategy = results[0]
              }
            }
          )
      },
      handleWriteStrategy() {
        const id = this.strategy.id
        const data = this.strategy
        if (id === '') {
          CreateStrategy(data)
            .then(
              response => {
                this.handleNotice(response)
                this.handleGetStrategyList()
              },
            )
        } else {
          UpdateStrategy(id, data).then(response => {
            this.handleNotice(response)
            this.handleGetStrategyList()
          })
        }
      },
      handleGetFWList() {
        GetFWList({}).then(response => {
          console.log(response)
          const results = response.results
          if (results.length > 0) {
            this.sqlsettings = results[0]
          }
        })
      },
      handleGetUsers() {
        getUserList({ pagesize: 1000 }).then(response => {
          console.log(response)
          this.userList = []
          const results = response.results
          for (const i in results) {
            const user = results[i]
            if (user.is_superuser === true) {
              this.userList.push(user)
            }
          }
        })
      },
      handleWriteFW() {
        const id = this.sqlsettings.id
        const data = this.sqlsettings
        if (id === '') {
          CreateFW(data)
            .then(
              response => {
                this.handleNotice(response)
                this.handleGetFWList()
              },
            )
        } else {
          UpdateFW(id, data)
            .then(
              response => {
                this.handleNotice(response)
                this.handleGetFWList()
              },
            )
        }
      }
    }
  }
</script>

<style scoped>
  .left20 {
    margin-left: 20px
  }
  .mig {
    /*margin-left: 20px;*/
    margin-bottom: 20px;
  }
  .platformSettings {
    padding: 10px;
    background-color: white;
  }
</style>

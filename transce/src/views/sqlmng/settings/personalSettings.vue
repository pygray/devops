<template>
  <div class="personalSettings">
    <el-row :gutter="20">
    <el-form :label-position="labelPosition" label-width="150px">
      <el-col :span="12">
      <el-alert title="订阅" type="warning" :closable="false" class="mig" show-icon></el-alert>
      <el-form-item label="集群" class="mig" size="small">
        <el-select v-model="queryParams.cluster" style="width: 100%" filterable @change="handleChange">
          <el-option
            v-for="item in clusterList"
            :key="item.id"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
    <el-form-item label="环境" size="small" class="mig">
      <el-radio-group v-model="queryParams.env" style="width: 100%" @change="handleChange">
        <el-radio label="prod">生产</el-radio>
        <el-radio label="ppe">预发布</el-radio>
        <el-radio label="test">测试</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="数据库" size="small" class="mig">
      <el-select v-model="personalSettings.dbs"  multiple filterable style="width: 100%">
        <el-option
          v-for="item in dbList"
          :key="item.id"
          :label="item.name"
          :value="item.id">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="工单核准人" size="small" class="mig" v-if="showLeader">
      <el-select v-model="personalSettings.leader" style="width: 100%" filterable>
        <el-option
          v-for="item in leaderList"
          :key="item.id"
          :label="item.username"
          :value="item.id">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="管理员组收件人" size="small" class="mig" v-if="showLeader">
      <el-select v-model="personalSettings.admin_mail" style="width: 100%" filterable>
        <el-option
          v-for="item in adminList"
          :key="item.id"
          :label="item.username"
          :value="item.id">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="操作" class="mig">
      <el-button type="primary" size="mini" @click="handleCreatePersonalSettings">保存</el-button>
      <el-button size="mini">取消</el-button>
    </el-form-item>
      </el-col>
    <el-col :span="10">
      <el-alert
        title=""
        type="warning"
        show-icon
        :closable="false">
        <b>订阅设置</b>
        <p class="left20">
          您可以在设置里指定常用的数据库及leader，提交工单时只显示这些数据供您选择。
        </p>
        <p>
          <b>1</b>.  关于工单核准人
        </p>
        <p class="left20">
          <b>1.1</b>. 研发角色：工单核准人是同组的经理（角色/组 在用户管理里设置）。
        </p>
        <p class="left20">
          <b>1.2</b>. 经理/总监/管理员角色：工单核准人是自己。
        </p>
        <p>
          <b>2</b>.  关于管理员组收件人
        </p>
        <p class="left20">
          <b>2.1</b>. 指定接收工单邮件的管理员。
        </p>
      </el-alert>
    </el-col>
    </el-form>
    </el-row>
  </div>

</template>

<script>
  import { GetSelectData, GetPersonalSettings, CreatePersonalSettings } from '@/api/sql/check'
  // import { GetMailActions, SetMailActions } from '@/api/sql/mailactions'
  import { GetClusterList } from '@/api/sql/cluster'
  export default {
    data() {
      return {
        showLeader: true,
        spinShow: true,
        env: '',
        labelPosition: 'right',
        clusterList: [],
        dbList: [],
        leaderList: [],
        adminList: [],
        personalSettings: {
          dbs: [], // id list
          leader: null, // id
          admin_mail: null
        },
        queryParams: {
          cluster: '',
          env: ''
        }
      }
    },
    created() {
      this.handleInitData()
    },
    methods: {
      notice(msg) {
        this.$message.success(msg)
      },
      getDbList(list, e) {
        const res = []
        for (const i in list) {
          if (list[i].env === e) {
            res.push(list[i].id)
          }
        }
        return res
      },
      getLeaderID(instance) {
        let leaderID = null
        if (instance != null) {
          leaderID = instance.id
        }
        return leaderID
      },
      handleInitData() {
        this.handleGetClusterList()
        this.handleGetPersonalSettings()
      },
      handleChange(e) {
        this.env = e
        if (e === 'prod' || e === 'ppe') {
          this.showLeader = true
        } else if (e === 'test') {
          this.showLeader = false
        }
        this.handleSelect()
        this.handleGetPersonalSettings()
      },
      handleGetMailActions() {},
      handleGetPersonalSettings() {
        GetPersonalSettings({ env: this.queryParams.env })
          .then(
            response => {
              const data = response.results[0]
              this.personalSettings.dbs = this.getDbList(data.db_list, this.queryParams.env)
              if (this.queryParams.env === 'prod' || this.queryParams.env === 'ppe') {
                this.personalSettings.leader = data.leader.username
                this.personalSettings.admin_mail = data.commiter.username
              }
            }
          )
      },
      handleSelect() {
        const data = this.queryParams
        GetSelectData(data)
          .then(response => {
            this.dbList = response.data.dbs
            this.leaderList = response.data.treaters
            this.adminList = response.data.admins
          })
      },
      handleGetClusterList() {
        this.spinShow = true
        GetClusterList(this.getClusterParams)
          .then(
            res => {
              this.spinShow = false
              this.clusterList = res.results
              this.setDefaultCluster()
            }
          )
      },
      setDefaultCluster() {
        if (this.clusterList.length !== 0) {
          this.queryParams.cluster = this.clusterList[0].id
        }
      },
      handleCreatePersonalSettings() {
        this.personalSettings.cluster = this.queryParams.cluster
        this.personalSettings.env = this.queryParams.env
        const data = this.personalSettings
        CreatePersonalSettings(data)
          .then(
            response => {
              const msg = '设置 保存成功'
              this.notice(msg)
              this.handleInitData()
            },
          )
      }
    }
  }
</script>

<style scoped>
  .mig {
    margin-bottom: 20px;
  }
  .personalSettings {
    padding: 10px;
    background-color: white;
  }
  .left20 {
    margin-left: 20px
  }
</style>

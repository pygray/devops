<template>
  <div style="padding: 10px;">
    <el-card shadow="always">
    <el-row>
      <el-col :span="8">
        <el-card>
          <el-alert title="" type="warning" show-icon :closable="false">inception连接</el-alert>
          <div style="height:520px">
            <el-tabs>
              <el-tab-pane label="inception服务" style="margin-bottom: 30px">

                <el-form ref="inceptionForm" :model="inceptionForm" :rules="ruleInceptionForm" label-width="100px">
                  <el-form-item label="地址：" prop="host" label-width="80px">
                    <el-input v-model="inceptionForm.host" :readonly="readonly" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="端口：" prop="port" label-width="80px">
                    <el-input v-model="inceptionForm.port" :readonly="readonly" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="操作: " label-width="80px">
                    <div>
                      <el-button type="warning" size="small" v-show="readonly === true" @click="editHandle">编辑</el-button>
                      <el-button type="primary" size="small" v-show="readonly === false" @click="saveHandle">保存</el-button>
                    </div>
                  </el-form-item>
                  <el-form-item label="连接测试: " label-width="80px">
                    <el-button type="success" size="small" @click="checkInceptionConn" round>连接</el-button>
                  </el-form-item>
                  <el-form-item>
                    <div style="color:#7B7B7B;">(上次变更时间：{{ time }})</div>
                  </el-form-item>
                </el-form>
              </el-tab-pane>
              <el-tab-pane label="inception备份库">
                <el-form ref="inceptionBackup" :model="inceptionBackup" label-width="100px">
                  <el-form-item label="地址：">
                    <div>{{ inceptionBackup.inception_remote_backup_host }}</div>
                  </el-form-item>
                  <el-form-item label="端口：">
                    <div>{{inceptionBackup.inception_remote_backup_port}}</div>
                  </el-form-item>
                  <el-form-item label="用户名：">
                    <div>{{inceptionBackup.inception_remote_system_user}}</div>
                  </el-form-item>
                  <el-form-item label="密码：">
                    <div>{{inceptionBackup.inception_remote_system_password}}</div>
                  </el-form-item>
                  <el-form-item label="连接测试: ">
                    <el-button type="success" size="small" @click="checkBackupConn" round>连接</el-button>
                  </el-form-item>
                </el-form>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card>
          <div class="inner">
            <el-alert title="" type="warning" show-icon :closable="false">inception变量</el-alert>
            <div style="height:510px;">
            <el-scrollbar class="el-scrollbar-class">
              <el-table :data="inceptionVariables">
                <el-table-column label="参数名字">
                  <template slot-scope="scope">
                    <el-tag>{{ scope.row.name }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="可选参数" prop="param">

                </el-table-column>
                <el-table-column label="默认值" prop="default">

                </el-table-column>
                <el-table-column label="功能说明">
                  <template slot-scope="scope">
                    <div>{{ handleInstructions(scope.row.instructions) }}</div>
                  </template>
                </el-table-column>
                <el-table-column label="设置">
                  <template slot-scope="scope">
                    <el-switch
                      active-value="ON"
                      inactive-value="OFF"
                      v-model="scope.row.value" @change="handleSwitchStatus(scope.row)">
                    </el-switch>
                  </template>
                </el-table-column>
              </el-table>
            </el-scrollbar>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    </el-card>
  </div>
</template>

<script>
  import { GetInceptionVariables, CheckConn, SetInceptionVariables, GetInceptionBackup, GetInceptionConnection, CreateInceptionConnection, UpdateInceptionConnection } from '@/api/sql/inceptionSettings'
  export default {
    data() {
      return {
        readonly: true,
        time: '',
        valueMap: {
          ON: true,
          OFF: false
        },
        bool_value: '',
        getDbParams: {
          page: 1,
          page_size: 1000,
          search: ''
        },
        inceptionForm: {
          id: '',
          host: '',
          port: '',
          updatetime: ''
        },
        inceptionBackup: {
          inception_remote_backup_host: '',
          inception_remote_backup_port: '',
          inception_remote_system_user: '',
          inception_remote_system_password: ''
        },
        ruleInceptionForm: {
          host: [{ required: true, message: 'Inception地址不能为空', trigger: 'blur' }],
          port: [{ required: true, message: 'Inception端口不能为空', trigger: 'blur' }]
        },
        inceptionVariables: []
      }
    },
    created() {
      this.handleGetInceptionBackup()
      this.handleGetInceptionVariables()
      this.handleGetInceptionConnection()
    },
    methods: {
      handleSwitchStatus(perams) {
        const status = perams.value
        const name = perams.name
        const data = {
          variable_name: name,
          variable_value: status
        }
        this.handleSetInceptionVariables(data)
      },
      handleInstructions(instructions) {
        const instruction = instructions
        if (instruction.length >= 20) {
          const instructions = instruction
        }
        return instructions
      },
      editHandle() {
        this.readonly = false
      },
      saveHandle() {
        this.readonly = true
        this.handleWriteConf()
      },
      getUpdatetime() {
        const time = this.inceptionForm.updatetime
        if (time !== '') {
          this.time = time.split('.')[0].replace('T', ' ')
        }
      },
      variablesNotice(title, name, value) {
        const h = this.$createElement
        const msg1 = h('p', {}, '的值设置为 ' + value)
        const msg2 = h('p', {}, '参数 ' + name)
        const msg3 = [msg2, msg1]
        const msg = h('div', msg3)
        this.$notify.success({
          title: title,
          dangerouslyUseHTMLString: true,
          message: msg
        })
      },
      notice(title, msg) {
        this.$notify.success({
          title: title,
          message: msg
        })
      },
      handleNotice(response) {
        // const httpstatus = response.status
        // console.log(response)
        if (response) {
          const title = '服务器提示'
          const msg = '设置 保存成功'
          this.notice(title, msg)
        }
      },
      checkInceptionConn() {
        const data = {
          check_type: 'inception_conn'
        }
        this.HandleCheckConn(data)
      },
      checkBackupConn() {
        const data = {
          check_type: 'inception_backup',
          host: this.inceptionBackup.inception_remote_backup_host,
          port: this.inceptionBackup.inception_remote_backup_port,
          user: this.inceptionBackup.inception_remote_system_user
        }
        this.HandleCheckConn(data)
      },
      handleWriteConf() {
        const id = this.inceptionForm.id
        const data = this.inceptionForm
        if (id === '') {
          CreateInceptionConnection(data)
            .then(
              response => {
                this.handleNotice(response)
                this.handleGetInceptionConnection()
              },
            )
        } else {
          UpdateInceptionConnection(id, data)
            .then(
              response => {
                this.handleNotice(response)
                this.handleGetInceptionConnection()
              },
            )
        }
      },
      handleGetInceptionVariables() {
        GetInceptionVariables(this.getDbParams)
          .then(res => {
            this.inceptionVariables = res.results
          })
      },
      handleSetInceptionVariables(data) {
        SetInceptionVariables(data)
          .then(res => {
            const status = res.status
            if (status === 0) {
              const title = '服务器提示'
              this.variablesNotice(title, data.variable_name, data.variable_value)
            }
          })
      },
      HandleCheckConn(data) {
        console.log(data)
        CheckConn(data)
          .then(res => {
            const status = res.status
            const data = res.data
            if (status === 0) {
              this.$message.success('连接成功')
            } else {
              this.$message.warning('连接失败 （' + data + '）')
            }
          })
      },
      handleGetInceptionConnection() {
        GetInceptionConnection()
          .then(res => {
            const results = res.results
            if (results.length > 0) {
              this.inceptionForm = results[0]
              this.getUpdatetime()
            }
          })
      },
      handleGetInceptionBackup() {
        GetInceptionBackup()
          .then(res => {
            this.inceptionBackup = res.data
          })
      }

    }
  }
</script>

<style scoped>
  .inner {
    margin-bottom: 10px;
    margin-left: 10px;
  }
  .el-scrollbar-class {
    height: 100%;
    overflow: scroll;
    overflow-x: hidden;
  }
</style>

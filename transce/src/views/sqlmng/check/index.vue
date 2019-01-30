<template>
  <div>
    <div style="padding: 10px;background-color: white">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-alert title="输入要上线的SQL语句" type="warning" :closable="false" show-icon class="mar"></el-alert>
          <br>
          <el-form :model="checkData" :rules="ruleCheckData" ref="checkContent" label-width="100px" show-icon class="demo-form">
            <el-form-item label="SQL" prop="sql_content">
              <editor v-model="checkData.sql_content" @init="editorInit" @setCompletions="setCompletions"></editor>
            </el-form-item>
            <el-form-item label="备注 ">
              <el-input type="textarea" v-model="checkData.remark"></el-input>
            </el-form-item>
            <el-form-item label="操作 ">
              <el-col :span="10">
                <el-button type="primary" size="mini" @click="handleCheckSql">审核</el-button>
              </el-col>
              <el-button size="mini" @click="handleClear">清空</el-button>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="12">
          <div>
          <el-alert title="选择执行条件" type="warning" :closable="false" show-icon class="mar"></el-alert>
          <el-form ref="checkConf" :model="checkData" :rules="ruleCheckData" :label-position="labelPosition" label-width="100px">
            <el-form-item label="目标数据库 ">
              <el-cascader
                size="small"
                expand-trigger="hover"
                :options="targetDbs"
                v-model="targetDb"
                @change="handleSelect"
                class="parm_check_element">
              </el-cascader>
            </el-form-item>
            <el-form-item label="工单核准人" prop="treater">
              <el-input v-model="checkData.treater_username" class="parm_check_element" :readonly="readonly" size="small"></el-input>
            </el-form-item>
          </el-form>
          </div>
          <div>
            <el-alert title="" type="warning" show-icon :closable="false">
              <p><b>Tips</b></p>
              <p>
                <b>1</b>.  您可以在<router-link to='/sqlmng/settings'><b>设置</b></router-link>里指定常用的数据库&工单核准人，之后只显示这些数据供您选择。
              </p>
              <p>
                <b>2</b>.  关于流程 (由管理员在 <router-link to='/settings/platform'><b>流程设置</b></router-link>里指定 )
              </p>
              <p class="left20">
                <b>2.1</b>. 关闭流程，工单流: 提交人 --- 核准人 。
              </p>
              <p class="left20">
                <b>2.2</b>. 开启流程，工单流: 提交人 --- 核准人 --- 管理员 。
              </p>
            </el-alert>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  import { CascaderData } from '@/utils/sql/formatData'
  import editor from '../my-components/sql/editor'
  import { GetPersonalSettings, CheckSql } from '@/api/sql/check'
  export default {
    components: { editor },
    data() {
      return {
        labelPosition: 'right',
        readonly: true,
        wordList: [],
        env_map: {
          prod: '生产',
          test: '测试',
          ppe: '预发布',
          '生产': 'prod',
          '测试': 'test',
          '预发布': 'ppe'
        },
        checkData: {
          sql_content: '',
          remark: '',
          env: '',
          db: '',
          treater_username: '',
          treater: '',
          commiter: '',
          users: []
        },
        commiter: {},
        ruleCheckData: {
          sql_content: [
            { required: true, message: '请输入SQL', trigger: 'blur' }
          ],
          treater: [
            { required: true, message: '请设置工单核准人', trigger: 'blur' }
          ],
          db: [
            { required: true, message: '请选择数据库', trigger: 'change', type: 'array', len: 3,
              fields: { 0: { type: 'number', required: true }, 1: { type: 'string', required: true }, 2: { type: 'number', required: true }}
            }
          ]
        },
        targetDb: [],
        targetDbs: []
      }
    },
    created() {
      this.getWordList()
      this.handleSelect()
    },
    methods: {
      getWordList() {
        for (const i of this.GLOBAL.highlight.split('|')) {
          this.wordList.push({ 'vl': i, 'meta': '关键字' })
        }
      },
      setCompletions(editor, session, pos, prefix, callback) {
        callback(null, this.wordList.map(function(word) {
          return {
            caption: word.vl,
            value: word.vl,
            meta: word.meta
          }
        }))
      },
      editorInit: function() {
        require('brace/mode/mysql') // language
        require('brace/theme/xcode')
      },
      renderFunc(treater, title) {
        this.$message({
          title: title,
          type: 'success',
          dangerouslyUseHTMLString: true,
          showClose: true,
          message: '<span>请等待<a>' + treater + '</a>处理'
        })
      },
      warning(title, msg) {
        this.$message({
          type: 'warning',
          title: title,
          duration: 0,
          message: msg
        })
      },
      handleClear() {
        this.checkData.sql_content = ''
      },
      setTreater(treater) {
        if (JSON.stringify(treater) !== '{}') {
          this.checkData.treater = treater.id
          this.checkData.treater_username = treater.username
        }
      },
      treaterClear() {
        this.checkData.treater_username = ''
        this.checkData.treater = ''
      },
      handleSelect(e) {
        this.treaterClear()
        if (e === undefined) {
          var env = 'test'
        } else {
          env = this.env_map[e[1]]
        }
        const data = {
          env: env
        }
        GetPersonalSettings(data)
          .then(response => {
            const data = response.results[0]
            const dbs = data.db_list
            const commiter = data.commiter
            const treater = data.leader
            this.setTreater(treater)
            this.checkData.commiter = commiter.username
            this.checkData.users = [commiter.id, treater.id]
            dbs.map((item) => {
              item.env = this.env_map[item.env]
            })
            this.targetDbs = CascaderData(dbs)
          })
      },
      handleCheckSql() {
        this.$refs.checkContent.validate((valid) => {
          if (!valid) {
            return
          }
          this.$refs.checkConf.validate((valid) => {
            if (!valid) {
              return
            }
            this.checkData.env = this.env_map[this.targetDb[1]]
            this.checkData.db = this.targetDb[2]
            CheckSql(this.checkData)
              .then(response => {
                const status = response.status
                // const data = response.data
                const msg = response.msg
                if (status === 0) {
                  this.renderFunc(this.checkData.treater_username, 'SQL工单 已提交')
                } else if (status === -1 || status === -2) {
                  this.warning('SQL审核不通过', msg)
                }
              })
          })
        })
      }
    }
  }
</script>

<style scoped>
  .mar {
    margin-bottom: 30px;
  }
  .parm_check_element {
    width: 400px;
    margin-left: 10px;
  }
  .left20 {
    margin-left: 20px
  }
  .test {
    background-color: #409EFF;
  }
</style>

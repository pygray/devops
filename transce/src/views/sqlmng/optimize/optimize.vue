<template>
  <div style="padding: 10px">
      <el-row :gutter="20">
        <el-card shadow="always">
        <el-col :span="10">
          <el-alert title="" type="warning" show-icon :closable="false">SQL语句优化</el-alert>
          <div style="margin-top: 40px">
            <el-form class="step-form" ref="checkData" :model="checkData" :rules="ruleCheckData" label-width="100px" size="small">
              <el-form-item label="数据库: " prop="db" style="margin-bottom: 30px">
                <el-cascader
                  :options="targetDbs"
                  expand-trigger="hover"
                  @change="handleGetTables"
                  placeholder="选择数据库"
                  style="width: 100%">
                </el-cascader>
              </el-form-item>
              <el-form-item label="表: " prop="table" style="margin-bottom: 30px">
                <el-select v-model="checkData.table" @change="handleGetTableInfo" filterable placeholder="选择表" style="width: 100%">
                  <el-option v-for="item in tableList" :value="item" :key="item">{{ item }}</el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="优化类型: " style="margin-bottom: 30px">
                <el-radio-group v-model="optimizeType">
                  <el-radio label="SOAR"></el-radio>
                  <el-radio label="SQLAdvisor"></el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="SQL语句: " prop="sql" style="margin-bottom: 30px">
                <editor v-model="checkData.sql" @init="editorInit" @setCompletions="setCompletions"></editor>
              </el-form-item>
              <el-form-item label="操作: ">
                <div v-if="optimizeType === 'SQLAdvisor'" style="margin-right: 10%">
                  <el-button type="primary" @click='handleSQLAdvisor' style="margin-right: 5%">查询</el-button>
                  <el-button @click="handleClear" style="margin-right: 10%">清空</el-button>
                </div>
                <div v-if="optimizeType==='SOAR'">
                  <el-button type="primary" @click="SOARAllowOnline" style="margin-right: 1%">SQL评分</el-button>
                  <el-button type="primary" @click="SOARBnlySyntax" style="margin-right: 1%">语法检查</el-button>
                  <el-button type="primary" @click="SOARFingerPrint" style="margin-right: 1%">SQL指纹</el-button>
                  <el-button type="primary" @click="SOARPretty" style="margin-right: 1%">SQL美化</el-button>
                </div>
              </el-form-item>
            </el-form>
          </div>
        </el-col>

        <el-col :span="12">
          <el-alert show-icon title="" style='margin-left:6%' :closable="false">
            <el-icon type="ios-lightbulb-outline" slot="icon"></el-icon>
            查询结果 {{ query_type }}
          </el-alert>
          <div class="scrollbar-div" style="color: black">
            <vue-markdown :source="query_result"> </vue-markdown>
          </div>
        </el-col>
        </el-card>
      </el-row>
  </div>
</template>

<script>
  import { GetDbList } from '@/api/sql/dbs'
  import { GetPersonalSettings } from '@/api/sql/check'
  import { CascaderData } from '@/utils/sql/formatData'
  import { GetTableList, GetTableInfo, GetSqlAdvisor, GetSqlSOAR } from '@/api/sql/sqlquery'
  import editor from '../my-components/sql/editor'
  import VueMarkdown from 'vue-markdown'
  export default {
    components: { editor, VueMarkdown },
    data() {
      return {
        spinShow: false,
        optimizeType: 'SOAR',
        targetDbs: [],
        wordList: [],
        dbList: [],
        tableList: [],
        database: '',
        query_type: '',
        query_result: '',
        checkData: {
          sql: '',
          table: ''
        },
        env_map: {
          prod: '生产',
          test: '测试',
          ppe: '预发布',
          '生产': 'prod',
          '测试': 'test',
          '预发布': 'ppe'
        },
        getParams: {
          page: 1,
          pagesize: 1000,
          search: ''
        },
        ruleCheckData: {
          sql: [{ required: true, message: '请输入SQL语句', trigger: 'blur' }],
          table: [{ required: true, message: '请选择表', trigger: 'change' }],
          db: [{ required: false, message: '请选择数据库', trigger: 'blur' }, { type: 'array', trigger: 'change' }]
        }
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
      warning(title, msg) {
        this.$notify.warning({
          title: title,
          duration: 0,
          message: msg
        })
      },
      handleClear() {
        this.checkData.sql = ''
      },
      clearDisplay() {
        this.query_result = ''
      },
      SOARAllowOnline() {
        this.query_type = ' / SOAR SQL评分'
        const soar_type = 'allow_online'
        this.handleSOAR(soar_type)
      },
      SOARBnlySyntax() {
        this.query_type = ' / SOAR 语法检查'
        const soar_type = 'only_syntax'
        this.handleSOAR(soar_type)
      },
      SOARFingerPrint() {
        this.query_type = ' / SOAR SQL指纹'
        const soar_type = 'fingerprint'
        this.handleSOAR(soar_type)
      },
      SOARPretty() {
        this.query_type = ' / SOAR SQL美化'
        const soar_type = 'pretty'
        this.handleSOAR(soar_type)
      },
      handleSelect() {
        GetPersonalSettings()
          .then(response => {
            const data = response.results[0]
            const dbs = data.db_list
            dbs.map((item) => {
              item.env = this.env_map[item.env]
            })
            this.targetDbs = CascaderData(dbs)
          })
      },
      handleGetTables(e) {
        this.database = e[2]
        this.spinShow = true
        GetTableList(this.database)
          .then(
            response => {
              this.spinShow = false
              this.tableList = response.results
            }
          )
      },
      handleGetTableInfo(e) {
        if (e.length !== 0) {
          this.spinShow = true
          this.query_type = ' / 表结构'
          GetTableInfo(this.database, e)
            .then(
              response => {
                this.spinShow = false
                this.query_result = response.results
              }
            )
        }
      },
      handleSQLAdvisor() {
        this.clearDisplay()
        this.$refs.checkData.validate((valid) => {
          const sql = this.checkData.sql.replace(/^\s+|\s+$/g, '')
          if (this.database.length === 0 || sql.length === 0) {
            return
          }
          this.query_type = ' / SQLAdvisor 优化建议'
          const data = {
            sql: this.checkData.sql
          }
          GetSqlAdvisor(this.database, data)
            .then(
              response => {
                console.log(response)
                this.spinShow = false
                this.query_result = response.results
              }
            )
        })
      },
      handleSOAR(soar_type) {
        this.clearDisplay()
        this.$refs.checkData.validate((valid) => {
          const sql = this.checkData.sql.replace(/^\s+|\s+$/g, '')
          if (this.database.length === 0 || sql.length === 0) {
            return
          }
          const data = {
            sql: this.checkData.sql,
            soar_type: soar_type
          }
          GetSqlSOAR(this.database, data)
            .then(
              response => {
                this.query_result = response.results
                if (soar_type === 'only_syntax' && this.query_result.length === 0) {
                  this.query_result = 'SQL语法检测通过'
                }
              }
            )
        })
      }
    }
  }
</script>

<style scoped>
  .parm_check_element {
    width: 320px;
    margin-left: 20px;
  }
  .el-scrollbar-class {
    height: 100%;
    overflow: scroll;
    overflow-x: hidden;
  }
  .scrollbar-div {
    margin-left: 10%;
    overflow:auto;
  }
</style>

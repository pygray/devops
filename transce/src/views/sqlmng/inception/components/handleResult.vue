<template>
  <div>
    <div v-if="row.type === 'select'">
      <el-row :gutter="20">
        <el-col :span="24">
          <div style="height:400px;">
          <el-scrollbar class="el-scrollbar-class">
            <div class="wrapper">
              <div class="inner" v-for="(item, index) in handleResultExecute" :value="item.value" :key="index">{{ item.value.replace(/^\"|\"$/g,'') }}</div>
            </div>
          </el-scrollbar>
          </div>
        </el-col>
      </el-row>
    </div>

    <div v-else>
      <el-tabs value="handle_result_check" @tab-click="changeTab">
        <el-tab-pane label="Inception审核" name="handle_result_check">
          <el-row :gutter="20">
            <el-col :span="24">
              <div style="height:400px;">
              <el-scrollbar class="el-scrollbar-class">
                <div class="wrapper">
                  <div class="inner" v-for="(item, index) in handleResultCheck" :value="item.value" :key="index">{{ item.value }}</div>
                </div>
              </el-scrollbar>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>

        <el-tab-pane label="Inception执行" name="handle_result_execute">
          <el-row :gutter="20">
            <el-col :span="24">
              <div style="height:400px;">
              <el-scrollbar class="el-scrollbar-class">
                <div class="wrapper">
                  <div class="inner" v-for="(item, index) in handleResultExecute" :value="item.value" :key="index">{{ item.value }}</div>
                </div>
              </el-scrollbar>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>

        <el-tab-pane label="Inception回滚" name="handle_result_rollback">
          <el-row :gutter="20">
            <el-col :span="24">
              <div style="height:400px;">
              <el-scrollbar class="el-scrollbar-class">
                <div class="wrapper">
                  <div class="inner" v-for="(item, index) in handleResultRollback" :value="item.value" :key="index">{{ item.value }}</div>
                </div>
              </el-scrollbar>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </div>
    <div>
      <br>
      <el-button type="primary" size="large" @click="exportData"><el-icon type="ios-cloud-download-outline"></el-icon> 导出文件</el-button>
      <span class="totalDesc">数据量共计 {{ dataLength }} 条</span>
    </div>
  </div>
</template>

<script>
  import request from '@/utils/request'
  export default {
    props: ['row', 'handleResultCheck', 'handleResultExecute', 'handleResultRollback'],
    created() {
      this.tabName = this.row.type === 'select' ? 'handle_result_execute' : 'handle_result_check'
      this.dataLength = this.row.type === 'select' ? this.handleResultExecute.length : this.handleResultCheck.length
    },
    data() {
      return {
        tabName: '',
        dataLength: 0,
        handleMap: {
          handle_result_check: this.handleResultCheck ? this.handleResultCheck : [],
          handle_result_execute: this.handleResultExecute ? this.handleResultExecute : [],
          handle_result_rollback: this.handleResultRollback ? this.handleResultRollback : []
        }
      }
    },
    methods: {
      changeTab(data) {
        this.tabName = data.name
        this.dataLength = this.handleMap[data.name].length
      },
      exportData() {
        const sfx = '.data'
        const url = '/media/download/sqlhandle/' + this.row.id + sfx
        const params = { data_type: this.tabName }
        console.log(params)
        request({
          method: 'get',
          url: url,
          responseType: 'blob',
          params
        })
          .then((response) => {
            if (!response) {
              return
            }
            const url = window.URL.createObjectURL(response)
            const link = document.createElement('a')
            link.style.display = 'none'
            link.href = url
            link.setAttribute('download', this.tabName + '_' + this.row.id + sfx)
            document.body.appendChild(link)
            link.click()
          })
      }
    }
  }
</script>

<style scoped>
  .wrapper {
    background-color:black;
    color:white
  }
  .inner {
    margin-bottom: 10px;
    margin-left: 10px
  }
  .totalDesc {
    margin-left: 10px;
    color: #7b7b7b
  }
  .el-scrollbar-class {
    height: 100%;
    overflow: scroll;
    overflow-x: hidden;
  }
</style>

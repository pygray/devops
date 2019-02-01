<template>
  <div>
    <div style="margin-top:10px;margin-bottom:10px">

      <el-row :gutter="20">
        <el-col :span="2">
          <p><b>ID：</b></p>
        </el-col>
        <el-col :span="10">
          <p> {{ row.id }} </p>
        </el-col>
        <el-col :span="2">
          <p><b>目标库：</b></p>
        </el-col>
        <el-col :span="10">
          <p> {{ row.db_name }} </p>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="2">
          <p><b>提交时间：</b></p>
        </el-col>
        <el-col :span="10">
          <p> {{ getTime }} </p>
        </el-col>
        <el-col :span="2">
          <p><b>影响的行数：</b></p>
        </el-col>
        <el-col :span="10">
          <p> {{ row.exe_affected_rows }} </p>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="2">
          <p><b>发起人：</b></p>
        </el-col>
        <el-col :span="10">
          <p> {{row.commiter}} </p>
        </el-col>
        <el-col :span="2">
          <p><b>核准人：</b></p>
        </el-col>
        <el-col :span="10">
          <p> {{row.treater}} </p>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="2">
          <p><b>环境：</b></p>
        </el-col>
        <el-col :span="10">
          <p v-show="row.env === 'test'">测试</p>
          <p v-show="row.env === 'ppe'">预发布</p>
          <p v-show="row.env === 'prod'">生产</p>
        </el-col>
        <el-col :span="2">
          <p><b>工单状态：</b></p>
        </el-col>
        <el-col :span="10">
          <p v-if="row.status === -4">
            <el-tag color="red">回滚失败</el-tag>
          </p>
          <p v-if="row.status === -3">
            <el-tag>已回滚</el-tag>
          </p>
          <p v-else-if="row.status === -2">
            <el-tag>已暂停</el-tag>
          </p>
          <p v-else-if="row.status === -1">
            <el-tag color="blue" size="mini"><font color="white">待执行</font></el-tag>
          </p>
          <p v-else-if="row.status === 0">
            <el-tag color="mediumseagreen" size="mini"><font color="white">成功</font></el-tag>
          </p>
          <p v-else-if="row.status === 1">
            <el-tag color="yellow" size="mini"><font color="white">已放弃</font></el-tag>
          </p>
          <p v-else-if="row.status === 2">
            <el-tag color="red" size="mini"><font color="white">任务失败</font></el-tag>
          </p>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="2">
          <p><b>备注：</b></p>
        </el-col>
        <el-col :span="10">
          <p> {{ row.remark }} </p>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  export default {
    props: ['row', 'sqlContent'],
    computed: {
      getTime: function() {
        return this.row.createtime.split('.')[0].replace('T', ' ')
      }
    }
  }
</script>

<style scoped>
</style>

<template>
  <div>
    <div>
      <el-row>
        <el-col :span="24">
          <div style="height:400px;">
          <el-scrollbar class="el-scrollbar-class">
            <div class="inner" v-for="(item, index) in sqlContent" :value="item.value" :key="index">{{ item.value }} </div>
          </el-scrollbar>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  export default {
    props: ['sqlContent']
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

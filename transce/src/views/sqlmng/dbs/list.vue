<template>
  <div class="db-list">
    <el-table
      :data="value"
      border
      stripe
      style="width: 100%">

      <el-table-column
        label="#"
        type="index">
      </el-table-column>

      <el-table-column
        label="数据库名"
        prop="name">
      </el-table-column>

      <el-table-column
        label="数据库地址"
        prop="host">
      </el-table-column>

      <el-table-column
        label="端口"
        prop= "port">
      </el-table-column>

      <el-table-column
        label="用户名"
        prop= "user">
      </el-table-column>

      <el-table-column
        label="环境"
        prop= "env">
      </el-table-column>

      <el-table-column
        label="备注"
        prop= "remark">
      </el-table-column>

      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            @click="handleEdit(scope.row)">修改</el-button>

          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>

    </el-table>
  </div>
</template>

<script>
  export default {
    name: 'db-list',
    props: ['value'],
    methods: {
      /* 点击编辑按钮，将子组件的事件传递给父组件 */
      handleEdit(value) {
        this.$emit('edit', value)
      },
      /* 删除 */
      handleDelete(db) {
        const id = db.id
        const name = db.name
        this.$confirm(`此操作将删除: ${name}, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$emit('delete', id)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      }
    }
  }
</script>

<style scoped>

</style>

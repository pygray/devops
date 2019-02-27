<template>
  <div class="idc-list">
    <el-table
      class="table"
      :data="idcValue"
      border
      size="small">
      <el-table-column
        prop="name"
        label="厂商名称"
        align="center">
      </el-table-column>
      <el-table-column
        prop="letter"
        label="厂商简称"
        align="center">
      </el-table-column>
      <el-table-column
        prop="phone"
        label="手机"
        align="center">
      </el-table-column>
      <el-table-column
        prop="email"
        label="邮箱"
        align="center">
      </el-table-column>
      <el-table-column
        prop="address"
        label="地址"
        align="center">
      </el-table-column>
      <el-table-column
        prop=""
        label="操作"
        align="center">
        <template slot-scope="scope">
          <el-button v-if="hasPerm('cmdb.change_idc')" type="primary" size="mini" @click="handleEdit(scope.row)">修改</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
  export default {
    name: 'idc-list',
    props: ['idcValue'],
    data() {
      return {}
    },
    methods: {
      handleEdit(value) {
        this.$emit('edit', value)
      },
      handleDelete(idc) {
        const id = idc.id
        const name = idc.name
        this.$confirm(`此操作将删除该厂商: ${name}, 是否继续?`, '提示', {
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

<style lang="scss" scoped>

</style>

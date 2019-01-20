<template>
  <div class="server-list" style="text-align: center">
    <el-table
      :data="serverValue"
      style="width: 100%;text-align: center"
      border>
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="主机名称: ">
              <span>{{ props.row.hostname }}</span>
            </el-form-item>
            <el-form-item label="实例ID:">
              <span>{{ props.row.InstanceId }}</span>
            </el-form-item>
            <el-form-item label="IP地址:">
              <span>{{ props.row.ip }}</span>
            </el-form-item>
            <el-form-item label="CPU: ">
              <span>{{ props.row.cpu }}</span>
            </el-form-item>
            <el-form-item label="内存: ">
              <span>{{ props.row.memory }}</span>
            </el-form-item>
            <el-form-item label="系统: ">
              <span>{{ props.row.os }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="云厂商"
        prop="idc.name"
        align="center">
      </el-table-column>
      <el-table-column
        label="项目"
        prop="product.name"
        align="center">
      </el-table-column>
      <el-table-column
        label="服务"
        prop="service.name">
      </el-table-column>
      <el-table-column
        label="主机名"
        prop="hostname"
        align="center">
      </el-table-column>
      <el-table-column
        label="IP地址"
        prop="ip"
        align="center">
      </el-table-column>
      <el-table-column
        label="状态"
        prop="status"
        align="center">
      </el-table-column>
      <el-table-column
        label="备注"
        prop="remark"
        align="center">
      </el-table-column>
      <el-table-column
        prop=""
        label="操作"
        align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="handleEdit(scope.row)">修改</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">下线</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>

</template>

<script>
    export default {
      name: 'server-list',
      props: ['serverValue'],
      methods: {
        handleEdit(value) {
          this.$emit('edit', value)
        },
        handleDelete(server) {
          const id = server.id
          this.$confirm('是否删除 ' + server.hostname + '【' + server.ip + '】', '提示', {
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
  .table-form-expand {
    font-size: 0;
    label {
      width: 90px;
      color: #99a9bf;
    }
    .el-form-item {
      margin-right: 0;
      margin-bottom: 0;
      width: 50%;
    }
  }

</style>

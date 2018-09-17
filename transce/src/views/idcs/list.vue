<template>
  <div class="idc-list">
    <el-table
      :data="idcValues"
      style="width: 100%"
      :default-sort = "{prop: 'date', order: 'descending'}"
      >
      <el-table-column
        label="ID"
        sortable
        width="180">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="名称"
        sortable
        width="180">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="简称"
        sortable
        width="180">
        <template slot-scope="scope">
            <span>{{ scope.row.IdcLetter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="手机"
        width="180">
        <template slot-scope="scope">
          <span>{{ scope.row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="邮箱"
        width="180">
        <template slot-scope="scope">
          <span>{{ scope.row.email }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="地址"
        width="180">
        <template slot-scope="scope">
          <span>{{ scope.row.IdcAddress }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="text-align: center; margin-top:10px;" v-show="totalNum>=10">
      <el-pagination
        background
        layout="total, prev, pager, next"
        @current-change="handleCurrentChange"
        :total="totalNum">
      </el-pagination>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'idc-list',
    props: ['idcValues'],
    data() {
      return {

      }
    },
    methods: {
      handleEdit(value) {
        this.$emit('edit', value)
      },
      handleDelete() {}
    }
  }

</script>

<style lang="scss">
  .idc-list {}
</style>

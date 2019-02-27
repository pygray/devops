<template>
  <div class="idc" style="padding: 10px;">
    <el-card shadow="always">
    <div>
      <el-col :span="8" style="margin-bottom: 20px">
        <el-input placeholder="搜索" v-model="params.search" @keyup.enter.native="searchClick" size="small">
          <el-button slot="append" icon="el-icon-search" @click="searchClick"></el-button>
        </el-input>
      </el-col>
      <div class="add-idc-btn">
        <el-button v-if="hasPerm('cmdb.add_idc')" type="primary" @click="addClick" size="small">新增厂商</el-button>
      </div>
    </div>

    <!-- 厂商列表 -->
    <idc-list
      :idcValue="idcs"
      @edit="handleIdcEdit"
      @delete="handleIdcDelete"
      style="margin-bottom: 20px;">
    </idc-list>
    <div class="text-center" v-show="idc_total_num>=10">
      <el-pagination
        style="text-align: center"
        background
        @current-change="handleCurrentChange"
        layout="total, prev, pager, next, jumper"
        :current-page.sync="params.page"
        :total="idc_total_num">
      </el-pagination>
    </div>

    <!-- 新增厂商 -->
    <el-dialog
      title="新增厂商"
      :visible.sync="dialogVisibleForAddIdc"
      width="50%">
      <idc-form
        ref="idcForm"
        :is-loading="isLoadingCreateIdc"
        @submit="handleSubmitAddIdc"
        @cancel="handleCancelAddIdc">
      </idc-form>
    </el-dialog>

    <!-- 编辑厂商 -->
    <el-dialog
      title="编辑"
      :visible.sync="dialogVisibleForEdit"
      width="50%">
      <idc-form
        ref="idcForm"
        :is-loading="isLoadingEditIdc"
        :form="currentValue"
        @submit="handleSubmitEdit"
        @cancel="handleCancelEdit">
      </idc-form>
    </el-dialog>
    </el-card>
  </div>
</template>

<script>
  import { getIdcsList, createIdc, deleteIdc, updateIdc } from '@/api/cmdb'
  import IdcList from './list'
  import IdcForm from './form'
  export default {
    name: 'idc',
    components: {
      'idc-form': IdcForm,
      'idc-list': IdcList
    },
    data() {
      return {
        idcs: [],
        currentValue: {},
        idc_total_num: 0,
        params: {
          page: 1,
          search: ''
        },
        dialogVisibleForAddIdc: false,
        dialogVisibleForEdit: false,
        isLoadingCreateIdc: false,
        isLoadingEditIdc: false
      }
    },
    created() {
      this.fetchData()
    },
    methods: {
      fetchData() {
        getIdcsList(this.params).then(res => {
          console.log(res)
          this.idcs = res.results
          this.idc_total_num = res.count
        })
      },
      handleCurrentChange(val) {
        this.params.page = val
        this.fetchData()
      },
      searchClick() {
        this.params.page = 1
        this.fetchData()
      },
      addClick() {
        this.dialogVisibleForAddIdc = true
      },
      handleSubmitAddIdc(value) {
        createIdc(value).then(
          () => {
            this.$message({
              message: '创建厂商成功',
              type: 'success'
            })
            this.fetchData()
            this.handleCancelAddIdc()
            this.isLoadingCreateIdc = false
          },
          () => { this.isLoadingCreateIdc = false },
          err => {
            this.isLoadingCreateIdc = false
            console.log(err.message)
          }
        )
      },
      handleCancelAddIdc() {
        this.dialogVisibleForAddIdc = false
        this.$refs.idcForm.$refs.form.resetFields()
      },
      handleIdcEdit(value) {
        this.currentValue = { ...value }
        this.dialogVisibleForEdit = true
      },
      handleSubmitEdit() {
        this.isLoadingEditIdc = true
        const id = this.currentValue.id
        updateIdc(id, this.currentValue).then(res => {
          this.dialogVisibleForEdit = false
          this.$message({
            message: '操作成功',
            type: 'success'
          })
          this.isLoadingEditIdc = false
          this.fetchData()
        }, () => { this.isLoadingEditIdc = false },
        err => {
          this.isLoadingEditIdc = false
          console.log(err.message)
        })
      },
      handleCancelEdit() {
        this.dialogVisibleForEdit = false
        this.$refs.idcForm.$refs.form.resetFields()
      },
      handleIdcDelete(id) {
        console.log(id)
        deleteIdc(id).then(
          () => {
            this.$message({
              message: '删除厂商成功',
              type: 'success'
            })
            this.fetchData()
          },
          err => {
            console.log(err.message)
          }
        )
      }
    }
  }
</script>

<style lang="scss" scoped>
  .add-idc-btn {
    float: right
  }
</style>

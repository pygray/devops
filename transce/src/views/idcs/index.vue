<template>
  <div class="idcs">
    <el-button type="primary" @click="add" size="small">添加</el-button>
    <idc-list :idcValues="idcs" @edit="handleEdit" @delete="handleDelete"></idc-list>

    <el-dialog
      title="新增"
      :visible.sync="dialogVisibleForAdd"
      width="50%">
      <idc-form
        ref="idcForm"
        :is-loading="isLoadingCreateIdc"
        @submit="handleSubmitAdd"
        @cancel="handleCancelAdd">
      </idc-form>
    </el-dialog>

  </div>
</template>

<script>
  import { getIdcList } from '@/api/idcs'
  import idcList from './list'
  import idcForm from './form'

  export default {
    name: 'idcs',
    components: {
      idcList,
      idcForm
    },
    data() {
      return {
        idcs: [],
        totalNum: 0,
        params: {
          page: 1
        }
      }
    },
    methods: {
      fetchData() {
        getIdcList().then(res => {
          this.totalNum = res.count
          this.idcs = res.data.results
        })
      }
    },
    add() {},
    handleSubmitAdd() {},
    handleCancelAdd() {},
    created() {
      this.fetchData()
    }

  }
</script>

<style lang="scss" scoped>
  .idcs {
    padding: 10px;
  }
</style>

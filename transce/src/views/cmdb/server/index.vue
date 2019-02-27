<template>
  <div style="padding: 10px">
    <el-card shadow="always">
    <el-form ref="searchForm" :model="searchForm" :inline="true" size="small">
      <el-form-item>
        <el-select v-model="searchForm.idc" style="width: 150px">
          <el-option
            v-for="(item, index) in searchIdcsList"
            :key="index"
            :label="item.name"
            :value="item.id"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select v-model="searchForm.product" style="width: 150px">
          <el-option
            v-for="(item, index) in searchProductList"
            :key="index"
            :label="item.name"
            :value="item.id"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select v-model="searchForm.service" style="width: 150px">
          <el-option
            v-for="(item, index) in searchServiceList"
            :key="index"
            :label="item.name"
            :value="item.id"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-input v-model="searchForm.search" placeholder="请输入主机名或IP地址" style="width: 180px"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchClick()">搜索</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="addClick" style="xfloat:right">新增服务器</el-button>
      </el-form-item>
      <el-form-item>
        <el-upload
          class="upload-demo"
          action="http://127.0.0.1:8000/upload/file/"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :before-remove="beforeRemove"
          multiple
          :limit="1"
          :on-exceed="handleExceed"
          :file-list="fileList">
          <el-button>导入</el-button>
          <div slot="tip" class="el-upload__tip"><font style="color: red">只能上传xlsx/xls</font></div>
        </el-upload>
      </el-form-item>
      <el-form-item>
      <el-button>导出</el-button>
      </el-form-item>
    </el-form>
    <el-table
      v-loading="loading"
      element-loading-text="拼命加载中"
      :data="serverList"
      border
      class="table"
      style="margin-bottom: 20px"
      size="small">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form  label-position="left" inline class="table-form-expand">
            <el-form-item label="操作系统：">
              <span>{{ props.row.os }}</span>
            </el-form-item>
            <el-form-item label="实例ID：">
              <span>{{ props.row.InstanceId }}</span>
            </el-form-item>
            <el-form-item label="IP：">
              <span>{{ props.row.ip }}</span>
            </el-form-item>
            <el-form-item label="CPU：">
              <span>{{ props.row.cpu }}</span>
            </el-form-item>
            <el-form-item label="内存：">
              <span>{{ props.row.memory }}</span>
            </el-form-item>
            <el-form-item label="备注：">
              <span>{{ props.row.remark }}</span>
            </el-form-item>
            <el-form-item label="磁盘：">
              <span v-for="device in props.row.devices">{{ device }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        prop="idc.name"
        label="厂商"
        align="center">
      </el-table-column>
      <el-table-column
        prop="product.name"
        label="项目"
        align="center">
      </el-table-column>
      <el-table-column
        prop="service.name"
        label="服务"
        align="center">
      </el-table-column>
      <el-table-column
        prop="hostname"
        label="主机名"
        align="center">
      </el-table-column>
      <el-table-column
        prop="ip"
        label="IP"
        align="center">
      </el-table-column>
      <el-table-column
        prop="status"
        label="状态"
        width="60"
        align="center">
      </el-table-column>
      <el-table-column
        prop="LastCheck"
        label="LAST CHECK"
        width="155"
        align="center">
      </el-table-column>
      <el-table-column
        prop=""
        label="操作"
        align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="editClick(scope.row)">修改</el-button>
          <el-button type="danger" size="mini" @click="deleteClick(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="text-align: center" v-show="total_num>=10">
      <el-pagination
        background
        @current-change="paginationChange"
        layout="total, prev, pager, next, jumper"
        :current-page.sync="page"
        :total="total_num">
      </el-pagination>
    </div>

    <!-- 新增服务器 -->
    <el-dialog title="新增服务器" :visible.sync="dialogVisibleForAddServer">
      <el-form ref="addServerForm" :model="addServerForm" label-width="70px" :rules="addServerFormRules" size="small">
        <el-form-item label="IP" prop="ip">
          <el-input v-model="addServerForm.ip" placeholder="请输入IP地址"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisibleForAddServer = false">取 消</el-button>
        <el-button type="primary" @click="submitAddServerClick">新 增</el-button>
      </div>
    </el-dialog>

    <!-- 修改服务器 -->
    <el-dialog title="修改服务器" :visible.sync="changeServerVisible">
      <el-form ref="changeServerForm" :model="changeServerForm" label-width="70px" :rules="changeServerFormRules" size="small">
        <el-form-item label="主机名称" prop="hostname">
          <el-input v-model="changeServerForm.hostname" :disabled="true" placeholder="请输入主机名称" disabled="disabled"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="changeServerForm.status">
            <el-option
              v-for="(item, index) in statusList"
              :key="index"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="厂商" prop="idc">
          <el-select v-model="changeServerForm.idc" @change="changeIdc">
            <el-option
              v-for="(item, index) in idcList"
              :key="index"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目" prop="product">
          <el-select v-model="changeServerForm.product" @change="changeProduct">
            <el-option
              v-for="(item, index) in productList"
              :key="index"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="服务" prop="service">
          <el-select v-model="changeServerForm.service">
            <el-option
              v-for="(item, index) in serviceList"
              :key="index"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="changeServerForm.remark" placeholder="请输入备注"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="changeServerVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitChangeServerClick">确 定</el-button>
      </div>
    </el-dialog>
    </el-card>
  </div>
</template>
<script>
  import { getServerList, deleteServer, getIdcsList, getIdcProductList, getProductServiceList, updateServer, createServer } from '@/api/cmdb'
  export default {
    data() {
      return {
        loading: false,
        fileList: [],
        serverList: [],
        total_num: 0,
        page: 1,
        state: 0,
        dialogVisibleForAddServer: false,
        searchForm: {
          hostname: '',
          idc: '',
          product: '',
          service: '',
          server_purpose: '',
          'page': 1
        },
        idcList: [],
        serviceList: [],
        productList: [],
        searchServiceList: [{ id: '', name: '所有服务' }],
        searchProductList: [{ id: '', name: '所有项目' }],
        serverProductList: [],
        changeServerVisible: false,
        statusList: ['线上', '下线', '测试', '故障', '发布', '维护'],
        changeServerForm: {
          id: '',
          hostname: '',
          status: '',
          remark: '',
          idc: '',
          product: '',
          service: ''
        },
        changeServerNewForm: {},
        changeServerFormRules: {
          status: [
            { required: true, trigger: 'blur', message: '请选择状态' }
          ],
          idc: [
            { required: true, trigger: 'change', message: '请选择厂商' }
          ],
          product: [
            { required: true, trigger: 'change', message: '请选择项目' }
          ],
          service: [
            { required: true, trigger: 'change', message: '请选择服务' }
          ]
        },
        addServerForm: {
          product: null,
          service: null,
          hostname: '',
          InstanceId: '',
          ip: '',
          cpu: '',
          memory: '',
          status: '',
          os: '',
          remark: '',
          idc: null
        },
        addServerFormRules: {
          ip: [
            { required: true, trigger: 'blur', message: '请输入IP' }
          ]
        }
      }
    },
    computed: {
      searchIdcsList() {
        return [{ id: '', name: '所有厂商' }].concat(this.idcList)
      }
    },
    watch: {
      state() {
        getIdcsList({ page_size: 0 }).then(res => {
          this.idcList = res.map(item => {
            return { id: item.id, name: item.name }
          })
        })
        this.fetchData()
      },
      'searchForm.idc'(val) {
        if (!val) {
          this.searchForm.product = ''
          return
        }
        getIdcProductList(val).then(res => {
          this.searchProductList = res.results.map(item => {
            return { id: item.id, name: item.name }
          })
        })
        this.searchProductList.splice(0, 0, { id: '', name: '所有项目' })
      },
      'searchForm.product'(val) {
        if (!val) {
          this.searchForm.service = ''
          return
        }
        getProductServiceList(val).then(res => {
          this.searchServiceList = this.searchServiceList.concat(res.results.map(item => {
            return { id: item.id, name: item.name }
          }))
        })
      },
      'changeServerForm.idc'(val) {
        if (!val) {
          this.changeServerForm.product = ''
          return
        }
        getIdcProductList(val).then(res => {
          this.productList = this.productList.concat(res.results.map(item => {
            return { id: item.id, name: item.name }
          }))
        })
      },
      'changeServerForm.product'(val) {
        if (!val) {
          this.changeServerForm.service = ''
          return
        }
        getProductServiceList(val).then(res => {
          this.serviceList = this.serviceList.concat(res.results.map(item => {
            return { id: item.id, name: item.name }
          }))
        })
      }
    },
    created() {
      this.state = 1
    },
    methods: {
      addClick() {
        if (this.$refs['addServerForm'] !== undefined) {
          this.$refs['addServerForm'].resetFields()
        }
        this.dialogVisibleForAddServer = true
      },
      submitAddServerClick() {
        this.$refs['addServerForm'].validate((valid) => {
          if (!valid) {
            return
          }
          createServer(this.addServerForm).then(res => {
            this.dialogVisibleForAddServer = false
            this.fetchData(Object.assign(this.searchForm))
            this.$message({
              message: '创建服务器成功',
              type: 'success'
            })
          })
        })
      },
      fetchData(params) {
        this.loading = true
        getServerList(params).then(res => {
          this.serverList = res.results
          this.total_num = res.count
          this.loading = false
        })
      },
      paginationChange(val) {
        this.searchForm.page = val
        this.fetchData(Object.assign(this.searchForm))
      },
      searchClick() {
        this.fetchData(Object.assign(this.searchForm))
      },
      changeIdc() {
        this.productList = []
        this.changeServerForm.product = ''
      },
      changeProduct() {
        this.serviceList = []
        this.changeServerForm.service = ''
      },
      handleRemove(file, fileList) {
        console.log(file, fileList)
      },
      handlePreview(file) {
        console.log(file)
      },
      handleExceed(files, fileList) {
        this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${file.name} ？`)
      },
      editClick(row) {
        if (this.$refs['changeServerForm'] !== undefined) {
          this.$refs['changeServerForm'].resetFields()
        }
        const { id, hostname, status, remark } = row
        const { idc, product, service } = { idc: row.idc.id, product: row.product.id, service: row.service.id }
        this.changeServerForm = { id, hostname, status, remark, idc, product, service }
        this.changeServerVisible = true
      },
      submitChangeServerClick() {
        this.$refs['changeServerForm'].validate((valid) => {
          if (!valid) {
            return
          }
          updateServer(this.changeServerForm.id, this.changeServerForm).then(res => {
            this.changeServerVisible = false
            this.fetchData(Object.assign(this.searchForm))
            this.$message({
              message: '操作成功',
              type: 'success'
            })
          })
        })
      },
      deleteClick(row) {
        this.$confirm('是否删除 ' + row.hostname + '【' + row.ip + '】', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteServer(row.id).then(() => {
            this.$message({
              message: '删除服务器成功',
              type: 'success'
            })
            if (this.serverList.length === 1 && this.searchForm.page > 1) {
              this.searchForm.page = this.searchForm.page - 1
            }
            this.fetchData(Object.assign(this.searchForm))
          })
        }).catch(() => {
          this.$message({
            message: '操作失败',
            type: 'error'
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

<template>
  <div class="apply">
    <el-form :model="form" :rules="rules" ref="form" label-width="180px">
      <el-form-item label="选择项目：" prop="name">
        <el-select v-model="form.name" filterable placeholder="请选择项目" style="width: 60%;">
          <el-option
            v-for="item in project_list"
            :key="item.index"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="选择项目版本：" prop="version">
        <el-select v-model="form.version" filterable placeholder="请选择项目版本" style="width: 60%;">
          <el-option
            v-for="item in tag_list"
            :key="item.index"
            :label="item.name"
            :value="item.name">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="版本信息：" prop="info">
        <el-input v-model="form.info" disabled  placeholder= "版本信息" style="width: 60%;"></el-input>
      </el-form-item>

      <el-form-item label="指派给：" prop="assign_to">
        <el-select v-model="form.reviewer" filterable placeholder="请选择发布处理人" style="width: 60%;">
          <el-option
            v-for="item in users_list"
            :key="item.index"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="上线详情：" prop="detail">
        <el-input v-model="form.detail" type="textarea" placeholder= "上线详情" rows="8"  style="width: 60%;"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">创建</el-button>
        <el-button @click="onCancel">退出</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import { getUserList } from '@/api/account'
  import { getProjectList, getProjectTag, getOneProject } from '@/api/projects'
  import { createDeploy } from '@/api/release'
  export default {
    data() {
      return {
        form: {
          id: '',
          name: '',
          version: '',
          info: '',
          detail: '',
          reviewer: ''
        },
        params: {
          page_size: 100
        },
        rules: {
          name: [
            { required: true, message: '请输入项目', trigger: 'blur' }
          ],
          version: [
            { required: true, message: '请输入项目版本', trigger: 'blur' }
          ],
          info: [
            { required: true, message: '请输入版本信息', trigger: 'blur' }
          ],
          reviewer: [
            { required: true, message: '请输入发布指派人', trigger: 'blur' }
          ]
        },
        users_list: [],
        project_list: [],
        tag_list: [],
        message_list: [],
        state: 0
      }
    },
    watch: {
      state() {
        getProjectList().then(res => {
          this.project_list = res.map(item => {
            return { id: item.id, name: item.name }
          })
        })
        getUserList(this.params).then(res => {
          this.users_list = res.results
        })
      },
      'form.name'(val) {
        // console.log(val)
        if (!val) {
          this.form.version = ''
          return
        }
        if (typeof val === 'number') {
          this.form.id = val
          console.log(this.form.id)
          getProjectTag(this.form.id).then(res => {
            this.tag_list = res
            this.message_list = res
          })
          this.form.version = ''
        }
        // this.$refs['form'].resetFields()
        // getOneGroup(2).then(res => {
        //   this.sa_list = res.members
        //   // console.log(this.sa_list)
        // })
        // }
      },
      'form.version'(val) {
        if (!val) {
          this.form.info = ''
          return
        }
        for (var i = 0; i < this.message_list.length; i++) {
          if (this.message_list[i].name === val) {
            this.form.info = this.message_list[i].message
            break
          }
          this.form.info = ''
        }
      }
    },
    created() {
      this.state = 1
    },
    methods: {
      onSubmit() {
        this.$message('submit!')
        this.$refs.form.validate((valid) => {
          if (!valid) {
            return
          }
          getOneProject(this.form.id).then(res => {
            const name = res[0].name
            this.form.name = name
            const params = Object.assign({}, this.form)
            console.log(params)
            // console.log(this.form.name)
            createDeploy(params).then(res => {
              this.$message({
                message: '创建成功',
                type: 'success'
              })
              this.$router.push({ path: '/deploy/list' })
            })
          })
        })
      },
      onCancel() {
        this.$message({
          message: 'cancel!',
          type: 'warning'
        })
      }
    }
  }
</script>

<style scoped>
  .line {
    text-align: center;
  }
  .apply {
    margin-top:2cm;
  }
</style>

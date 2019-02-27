<template>
  <div class="db-form">
    <el-form :model="form" :rules="rules" ref="form" label-width="100px" class="demo-form" size="small">

      <el-form-item label="环境: ">
        <el-select v-model="form.env" placeholder="请选择环境">
          <el-option value="test">测试</el-option>
          <el-option value="ppe">预发布</el-option>
          <el-option value="prod">生产</el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="数据库名: " prop="name">
        <el-input v-model="form.name" placeholder="请输入数据库名称"></el-input>
      </el-form-item>

      <el-form-item label="地址: " prop="host">
        <el-input v-model="form.host" placeholder="请输入地址"></el-input>
      </el-form-item>

      <el-form-item label="端口: " prop="port">
        <el-input v-model="form.port" placeholder="请输入端口"></el-input>
      </el-form-item>

      <el-form-item label="用户名: " prop="user">
        <el-input v-model="form.user" placeholder="请输入用户名"></el-input>
      </el-form-item>

      <el-form-item label="密码: " prop="password">
        <el-input v-model="form.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>

      <el-form-item label="备注: " prop="remark">
        <el-input v-model="form.remark" placeholder="请输入备注"></el-input>
      </el-form-item>

      <el-form-item label="连接测试: " >
        <el-button type="success" size="small" @click="updateCheckConn">连接</el-button>
      </el-form-item>
      <el-form-item>
        <div class="btn-wrapper">
          <el-button size="small" @click="cancel">取消</el-button>
          <el-button size="small" type="primary" @click="submitForm">保存</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import { CheckConn } from '@/api/sql/dbs'
  export default {
    name: 'db-form',
    props: {
      form: { // 接受父组件传递过来的值渲染表单
        type: Object,
        default() {
          return {
            name: '',
            host: '',
            port: '',
            user: '',
            password: '',
            remark: '',
            cluster: null
            // related_user: null
          }
        }
      }
    },
    data() {
      return {
        rules: {
          name: [
            { required: true, message: '数据库名不能为空', trigger: 'blur' }
          ],
          host: [
            { required: true, message: '数据库地址不能为空', trigger: 'blur' }
          ],
          port: [
            { required: true, message: '数据库端口不能为空', trigger: 'blur' }
          ],
          user: [
            { required: true, message: '用户名不能为空', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '密码不能为空', trigger: 'blur' }
          ]
        },
        state: 0
      }
    },
    methods: {
      updateCheckConn() {
        const data = {
          check_type: 'update_target_db',
          id: this.form.id
        }
        this.handleCheckConn(data)
      },

      handleCheckConn(data) {
        CheckConn(data)
          .then(
            res => {
              const status = res.status
              const data = res.data
              if (status === 0) {
                this.$message.success('连接成功')
              } else {
                this.$message.warning('连接失败 （' + data + '）')
              }
            })
      },
      submitForm() {
        this.$refs.form.validate(valid => {
          if (!valid) {
            return
          }
          this.$emit('submit', this.form)
        })
      },
      cancel() {
        this.$emit('cancel')
      }
    }
  }
</script>

<style scoped>

</style>

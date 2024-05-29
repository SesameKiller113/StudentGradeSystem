<template>
    <div>
        <Row>
            <Col span="16" offset="4">
                <Row>
                    <Col span="6" style="text-align: left" >
                        <a herf="javascript:void(0)" @click='this.$router.push("/students")'>Student Grade Management</a>
                    </Col>
                    <Col span="16" style="text-align: right">
                        <a herf="javascript:void(0)" @click='this.$router.push("/")'>Logout</a>
                    </Col>
                </Row>
                <Row style="text-align: center; display: inline" >
                    <h1 style="color: darkorange; margin-top: 10px">Teacher Account Management</h1>
                </Row>
                <Row style="margin-top: 15px">
                  <Col span="2" offset="9"><Button type="primary" size="large" @click="get_teachers">List Search</Button></Col>
                  <Col span="2" offset="3"><Button type="success" size="large" @click="show_add"  style="background-color: crimson">Add Account</Button></Col>
                </Row>
                <Row style="margin-top: 30px">
                    <Col span="24">
                        <Table :columns="columns" :data="data">
                            <template #action="{row, index}">
                                <Button type="primary" size="default" style="margin-right: 5px" @click="show_edit(row)">Edit</Button>
                                <Button type="error" size="default" @click="del_confirm(row)">Delete</Button>
                            </template>
                        </Table>
                    </Col>
                </Row>
            </Col>
        </Row>
    </div>
    <div>
        <Modal
            v-model="add.modal"
            title="Add Teacher Account"
            :loading="add.loading"
            ok-text="Confirm"
            cancel-text="Cancel"
            @on-ok="add_confirm"
            @on-cancel="add_cancel">
            <p>
                <Row>
                    <Col span="4">Username</Col>
                    <Col span="20"><Input v-model="add.param.username" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">Password</Col>
                    <Col span="20"><Input v-model="add.param.password" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
        </Modal>
        <Modal
            v-model="edit.modal"
            title="Edit Teacher Account"
            :loading="edit.loading"
            ok-text="Confirm"
            cancel-text="Cancel"
            @on-ok="edit_confirm"
            @on-cancel="edit_cancel">
            <p>
                <Row>
                    <Col span="4">TeacherID</Col>
                    <Col span="20"><Input v-model="edit.param.id" size="small" style="width: 80%" disabled/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">Username</Col>
                    <Col span="20"><Input v-model="edit.param.username" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">Password</Col>
                    <Col span="20"><Input v-model="edit.param.password" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
        </Modal>
    </div>
</template>

<script>
import {Button, Col, Row, Table} from "view-ui-plus";

export default {
  components: {Col, Table, Button, Row},
      data(){
          return {
              add: {
                  modal: false,
                  loading: true,
                  param: {
                      username: '',
                      password: '',
                  },
              },
              edit: {
                  modal: false,
                  loading: true,
                  param: {
                      id: '',
                      username: '',
                      password: '',
                  },
              },
              columns: [
                  {
                      title: 'TeacherID',
                      key: 'id',
                      align: 'center',
                  },
                  {
                      title: 'Username',
                      key: 'username',
                      align: 'center',
                  },
                  {
                      title: 'Password',
                      key: 'password',
                      align: 'center',
                  },
                  {
                      title: 'Action',
                      slot: 'action',
                      align: 'center',
                      minWidth: 120,
                  },
              ],
              data: [],
          }
      },
      mounted() {
          this.get_teachers()
      },
      methods: {
          get_teachers() {
              this.$axios({
                  withCredentials: true,
                  method: "GET",
                  url: "http://127.0.0.1:9000/teacher_list",
              }).then((res)=>{
                  console.log(res)
                  if(res.status != 200){
                      this.$Message.error('Interface Error(' + res.status + ')')
                      return
                  }
                  if (res.data.code != 0){
                      this.$Message.error('Data fetching error(' + res.data.message + ')')
                  }
                  this.data = res.data.data
              }).catch((error)=>{

              })
          },

          show_add() {
              this.add.modal = true
          },
          add_confirm() {
              if (this.add.param.username == ''){
                  this.$Message.error("Name cannot be empty")
                  this.add.loading = false
                  this.$nextTick(()=>{
                      this.add.loading = true
                  })
                  return
              }
              let param = {username: this.add.param.username}
              if (this.add.param.password != ''){
                  param.password = this.add.param.password
              }

              this.$axios({
                withCredentials: true,
                method: "POST",
                url: "http://127.0.0.1:9000/teacher_add",
                data: JSON.stringify(param),
                headers:{
                  'Content-Type': "application/json",
                },
            }).then((res)=>{
                console.log(res)
                if(res.status != 200){
                    this.$Message.error('Interface Error(' + res.status + ')')
                    return
                }
                if (res.data.code != 0){
                    this.$Message.error('API Error(' + res.data.message + ')')
                    return
                }
                this.add_reset()
                this.$Message.success(res.data.message)
                this.add.loading = false
                  this.$nextTick(()=>{
                      this.add.loading = true
                  })
                this.get_teachers()
            }).catch((error)=>{
                this.$Message.error('Netword Error(' + error + ')')
                return
            })
          },
          add_reset() {
              this.add.param.username = ''
              this.add.param.password = ''
              this.add.modal = false
          },
          add_cancel() {
              this.add_reset()
          },

          del_confirm(row) {
              const self = this
              this.$Modal.confirm({
                  title: "<h2 style='color: #ff002f' text-align: center; display: inline>Delete Confirmation</h2>",
                  content: `<p style="font-size: large; color: royalblue" text-align: center; display: inline>Are you sure you want to delete(${row.name})?</p>`,
                  okText: "Confirm",
                  cancelText: "Cancel",
                  onOk(){
                      console.log("OK button clicked")
                      self.del_teacher(row.id)
                  },
                  onCancel(){
                      return
                  },
              })
          },
          del_teacher(id) {
              const param = {id:id}
              this.$axios({
                withCredentials: true,
                method: "POST",
                url: "http://127.0.0.1:9000/teacher_del",
                data: JSON.stringify(param),
                headers:{
                  'Content-Type': "application/json",
                },
            }).then((res)=>{
                console.log(res)
                if(res.status != 200){
                    this.$Message.error('Interface Error(' + res.status + ')')
                    return
                }
                if (res.data.code != 0){
                    this.$Message.error('API Error(' + res.data.message + ')')
                    return
                }
                this.$Message.success(res.data.message)
                this.get_teachers()
            }).catch((error)=>{
                this.$Message.error('Netword Error(' + error + ')')
                return
            })
          },

          show_edit(row) {
              this.edit_reset()
              this.edit.param.id = row.id
              this.edit.param.username = row.username
              this.edit.param.password = row.password
              this.edit.modal = true
          },
          edit_confirm() {
              if (this.edit.param.name == ''){
                  this.$Message.error("Name cannot be empty")
                  this.edit.loading = false
                  this.$nextTick(()=>{
                      this.edit.loading = true
                  })
                  return
              }
              const param = {
                  id: this.edit.param.id,
                  username: this.edit.param.username,
                  password: this.edit.param.password,

              }
              this.$axios({
                withCredentials: true,
                method: "POST",
                url: "http://127.0.0.1:9000/teacher_edit",
                data: JSON.stringify(param),
                headers:{
                  'Content-Type': "application/json",
                },
            }).then((res)=>{
                console.log(res)
                if(res.status != 200){
                    this.$Message.error('Interface Error(' + res.status + ')')
                    return
                }
                if (res.data.code != 0){
                    this.$Message.error('API Error(' + res.data.message + ')')
                    return
                }
                this.edit_reset()
                this.$Message.success(res.data.message)
                this.edit.loading = false
                  this.$nextTick(()=>{
                      this.edit.loading = true
                  })
                this.get_teachers()
            }).catch((error)=>{
                this.$Message.error('Netword Error(' + error + ')')
                return
            })
          },
          edit_reset() {
              this.edit.param.id = ''
              this.edit.param.username = ''
              this.edit.param.password = ''
              this.edit.modal = false
          },
          edit_cancel() {
              this.edit_reset()
          },
      },
}
</script>
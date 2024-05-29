<template>
    <div>
        <Row>
            <Col span="16" offset="4">
                <Row>
                    <Col span="6" style="text-align: left" >
                        <a herf="javascript:void(0)" @click='this.$router.push("/teachers")'>Teacher Account Management</a>
                    </Col>
                    <Col span="16" style="text-align: right">
                        <a herf="javascript:void(0)" @click='this.$router.push("/")'>Logout</a>
                    </Col>
                </Row>
                <Row style="text-align: center; display: inline" >
                    <h1 style="color: #7d97ef; margin-top: 10px">Student Grade Management</h1>
                </Row>
                <Row style="margin-top: 15px">
                  <Col span="2" offset="9"><Button type="primary" size="large" @click="get_students">List Search</Button></Col>
                  <Col span="2" offset="3"><Button type="success" size="large" @click="show_add">Add</Button></Col>
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
            title="Add Student Information"
            :loading="add.loading"
            ok-text="Confirm"
            cancel-text="Cancel"
            @on-ok="add_confirm"
            @on-cancel="add_cancel">
            <p>
                <Row>
                    <Col span="4">Name</Col>
                    <Col span="20"><Input v-model="add.param.name" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">Chinese</Col>
                    <Col span="20"><Input v-model="add.param.chinese" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">Math</Col>
                    <Col span="20"><Input v-model="add.param.math" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">English</Col>
                    <Col span="20"><Input v-model="add.param.english" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
        </Modal>
        <Modal
            v-model="edit.modal"
            title="Edit Student Information"
            :loading="edit.loading"
            ok-text="Confirm"
            cancel-text="Cancel"
            @on-ok="edit_confirm"
            @on-cancel="edit_cancel">
            <p>
                <Row>
                    <Col span="4">StudentsID</Col>
                    <Col span="20"><Input v-model="edit.param.id" size="small" style="width: 80%" disabled/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">Name</Col>
                    <Col span="20"><Input v-model="edit.param.name" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">Chinese</Col>
                    <Col span="20"><Input v-model="edit.param.chinese" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">Math</Col>
                    <Col span="20"><Input v-model="edit.param.math" size="small" style="width: 80%"/></Col>
                </Row>
            </p>
            <p>
                <Row style="margin-top: 5px">
                    <Col span="4">English</Col>
                    <Col span="20"><Input v-model="edit.param.english" size="small" style="width: 80%"/></Col>
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
                      name: '',
                      chinese: '',
                      math: '',
                      english: '',
                  },
              },
              edit: {
                  modal: false,
                  loading: true,
                  param: {
                      id: '',
                      name: '',
                      chinese: '',
                      math: '',
                      english: '',
                  },
              },
              columns: [
                  {
                      title: 'StudentsID',
                      key: 'id',
                      align: 'center',
                  },
                  {
                      title: 'Name',
                      key: 'name',
                      align: 'center',
                  },
                  {
                      title: 'Chinese',
                      key: 'chinese',
                      align: 'center',
                  },
                  {
                      title: 'Math',
                      key: 'math',
                      align: 'center',
                  },
                  {
                      title: 'English',
                      key: 'english',
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
          this.get_students()
      },
      methods: {
          get_students() {
              this.$axios({
                  withCredentials: true,
                  method: "GET",
                  url: "http://127.0.0.1:9000/student_list",
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
              if (this.add.param.name == ''){
                  this.$Message.error("Name cannot be empty")
                  this.add.loading = false
                  this.$nextTick(()=>{
                      this.add.loading = true
                  })
                  return
              }
              let param = {name: this.add.param.name}
              if (this.add.param.chinese != ''){
                  param.chinese = this.add.param.chinese
              }
              if (this.add.param.math != ''){
                  param.math = this.add.param.math
              }
              if (this.add.param.english != ''){
                  param.english = this.add.param.english
              }

              this.$axios({
                withCredentials: true,
                method: "POST",
                url: "http://127.0.0.1:9000/student_add",
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
                this.get_students()
            }).catch((error)=>{
                this.$Message.error('Netword Error(' + error + ')')
                return
            })
          },
          add_reset() {
              this.add.param.name = ''
              this.add.param.chinese = ''
              this.add.param.math = ''
              this.add.param.english = ''
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
                      self.del_student(row.id)
                  },
                  onCancel(){
                      return
                  },
              })
          },
          del_student(id) {
              const param = {id:id}
              this.$axios({
                withCredentials: true,
                method: "POST",
                url: "http://127.0.0.1:9000/student_del",
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
                this.get_students()
            }).catch((error)=>{
                this.$Message.error('Netword Error(' + error + ')')
                return
            })
          },

          show_edit(row) {
              this.edit_reset()
              this.edit.param.id = row.id
              this.edit.param.name = row.name
              this.edit.param.chinese = row.chinese
              this.edit.param.math = row.math
              this.edit.param.english = row.english
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
                  name: this.edit.param.name,
                  chinese: this.edit.param.chinese,
                  math: this.edit.param.math,
                  english: this.edit.param.english,
              }
              this.$axios({
                withCredentials: true,
                method: "POST",
                url: "http://127.0.0.1:9000/student_edit",
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
                this.get_students()
            }).catch((error)=>{
                this.$Message.error('Netword Error(' + error + ')')
                return
            })
          },
          edit_reset() {
              this.edit.param.id = ''
              this.edit.param.name = ''
              this.edit.param.chinese = ''
              this.edit.param.math = ''
              this.edit.param.english = ''
              this.edit.modal = false
          },
          edit_cancel() {
              this.edit_reset()
          },
      },
}
</script>
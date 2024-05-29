<template>
    <div style="margin-top: 15px">
        <Row style="text-align: center; display: inline">
          <h1 style="color: #7d97ef">Student Management System</h1>
        </Row>
    </div>
    <div>
        <Row>
            <Col span="8" offset="8">
                <Row style="margin-top: 10px">
                    <Col span="5" style="font-size: large">Username:</Col>
                    <Col span="19"><Input v-model="username"/></Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col span="5" style="font-size: large">Password:</Col>
                    <Col span="19"><Input type="password" v-model="password"/></Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col offset="4" span="20">
                        <Button type="success" long @click="login" @keyup.enter="login">Log In</Button>
                    </Col>
                </Row>
            </Col>
        </Row>
    </div>
    <div>
        <Row style="margin-top: 40px">
            <img src="C:\Users\sheny\OneDrive\Desktop\StudentGradeSystem\background.png" alt="Description of the image">
        </Row>
    </div>
</template>

<script>
export default{
    data(){
        return{
          username: '',
          password: '',
      }
    },
    methods:{
        login(){
            if (this.username == '' && this.password == '') {
              this.$Message.info('Please input your username and password')
              return
            }
            if (this.username == '') {
                this.$Message.info('Please input your username')
                return
            }
            if (this.password == ''){
                this.$Message.info('Please input your password')
                return
            }
            const param = {username: this.username, password: this.password}
            this.$axios({
                withCredentials: true,
                method: "POST",
                url: "http://127.0.0.1:9000/login",
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
                if(res.data.code == 0){
                    this.$Message.success("Login Success")
                    this.$router.push("/students")
                    return
                }
                else{
                    this.$Message.error("Login Failed(" + res.data.message + ')')
                    return
                }
            }).catch((error)=>{
                this.$Message.error('Netword Error(' + error + ')')
                return
            })
        }
    },
}
</script>
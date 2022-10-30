<template>
  <user-layout>
    <el-result v-if="isLoading" title="Loading..." subTitle="加载中，请稍后">
      <template slot="icon">
        <el-image style="width: 200px; height: 200px;" :src="loadingImg"></el-image>
      </template>
    </el-result>
    <el-result v-if="isErr" icon="error" title="注册验证失败" :subTitle="errMsg">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="backLogin">返回登录</el-button>
      </template>
    </el-result>
    <el-result v-if="isSuc" icon="info" :title="info" subTitle="请点击下方按钮完成注册">
      <template slot="extra">
        <el-button type="success" size="medium" @click="handleConfirm">确认注册</el-button>
      </template>
    </el-result>
    <el-result v-if="isDone" icon="success" title="注册成功" subTitle="请点击下方按钮登录">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="backLogin">返回登录</el-button>
      </template>
    </el-result>

  </user-layout>
</template>

<script>
import loadingImg from '@/assets/images/loading.gif'
import UserLayout from '../layout'
import {confirmRegister, verifyRegister} from "@/api/user";

export default {
  name: "verify",
  components: {UserLayout},
  data() {
    return {
      loadingImg: loadingImg,
      verifyCode: "",
      info: "",
      errMsg: "",
      isLoading: true,
      isSuc: false,
      isErr: false,
      isDone: false,
      redirect: undefined
    }
  },
  created() {
    this.verifyCode = this.$route.params.code;
    this.checkVerifyCode();
  },
  methods: {
    checkVerifyCode() {
      if (this.verifyCode && this.verifyCode !== "") {
        verifyRegister(this.verifyCode).then( res => {
          this.isLoading = false;
          if (res.data.code === 0) {
            this.isSuc = true;
          } else {
            this.errMsg = res.data.msg;
            this.isErr = true;
          }
        })
      }
    },
    handleConfirm() {
      if (this.verifyCode && this.verifyCode !== "") {
        this.isSuc = false;
        this.isLoading = true;
        confirmRegister(this.verifyCode).then(res => {
          this.isLoading = false;
          if (res.data.code === 0) {
            this.isDone = true;
          } else {
            this.errMsg = res.data.msg;
            this.isErr = true;
          }
        })
      }
    },
    backLogin() {
      this.$router.push({path: "/login"});
    }
  }
}
</script>

<style scoped>

</style>

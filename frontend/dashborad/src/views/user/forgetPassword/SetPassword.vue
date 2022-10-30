<template>
  <user-layout>
    <el-result v-if="isLoading" title="Loading..." subTitle="加载中，请稍后">
      <template slot="icon">
        <el-image style="width: 200px; height: 200px;" :src="loadingImg"></el-image>
      </template>
    </el-result>
    <el-result v-if="isErr" icon="error" title="找不到账号" :subTitle="errMsg">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="backLogin">返回登录</el-button>
      </template>
    </el-result>
    <el-result v-if="isDone" icon="success" title="密码修改成功" subTitle="请点击下方按钮登录">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="backLogin">返回登录</el-button>
      </template>
    </el-result>
    <div v-if="isSuc">
      <div class="title">重置 <strong>{{ email }}</strong> 的密码</div>
      <el-form ref="setPwdForm" :model="setPwdForm" :rules="setPwdRules">
        <el-form-item prop="password">
          <el-input
            v-model="setPwdForm.password"
            type="password"
            auto-complete="off"
            placeholder="密码"
            show-password
            @keyup.enter.native="handleConfirm"
          >
            <svg-icon slot="prefix" icon-class="password" class="el-input__icon input-icon" />
          </el-input>
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="setPwdForm.confirmPassword"
            type="password"
            auto-complete="off"
            placeholder="再次输入密码"
            show-password
            @keyup.enter.native="handleConfirm"
          >
            <svg-icon slot="prefix" icon-class="eye" class="el-input__icon input-icon" />
          </el-input>
        </el-form-item>
        <el-form-item prop="code">
          <el-input
            v-model="setPwdForm.code"
            auto-complete="off"
            placeholder="验证码"
            style="width: 63%"
          >
            <svg-icon slot="prefix" icon-class="validCode" class="el-input__icon input-icon" />
          </el-input>
          <div class="set-pwd-code">
            <img :src="codeImg" class="set-pwd-code-img" @click="getCode">
          </div>
        </el-form-item>
        <el-form-item style="width:100%;">
          <el-button
            :loading="loading"
            size="medium"
            type="primary"
            style="width:100%;"
            @click.native.prevent="handleConfirm"
          >
            <span v-if="!loading">提 交</span>
            <span v-else>提 交 中...</span>
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </user-layout>
</template>

<script>
import UserLayout from "@/views/user/layout";
import {confirmForgetPwd, getCaptchaCode, verifyForgetPwd} from "@/api/user";
import loadingImg from "@/assets/images/loading.gif";
import md5 from 'js-md5'

export default {
  name: "SetPassword",
  components: {UserLayout},
  data (){
    return {
      email: "",
      setPwdForm: {
        password: "",
        confirmPassword: "",
        code: "",
        key: ""
      },
      setPwdRules: {
        password: [
          { required: true, trigger: "blur", message: "密码不能为空" },
        ],
        confirmPassword: [
          { required: true, trigger: "blur", message: "确认密码不能为空" },
        ],
        code: [{ required: true, trigger: "change", message: "验证码不能为空" }]
      },
      codeImg: "",
      errMsg: "",
      loadingImg: loadingImg,
      isLoading: true,
      isSuc: false,
      isErr: false,
      isDone: false,
      loading: false
    }
  },
  created() {
    this.verifyCode = this.$route.params.code;
    this.checkVerifyCode();
  },
  methods: {
    getCode() {
      getCaptchaCode().then( res => {
        if (res.code === 0) {
          this.codeImg = res.data.img;
          this.setPwdForm.key = res.data.key;
        }
      })
    },
    checkVerifyCode() {
      if (this.verifyCode && this.verifyCode !== "") {
        verifyForgetPwd(this.verifyCode).then(res => {
          this.isLoading = false;
          if (res.data.code === 0) {
            this.getCode();
            this.email = res.data.data.email;
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
        this.loading = true;
        let setPwdForm = {
          password: md5(this.setPwdForm.password),
          key: this.setPwdForm.key,
          code: this.setPwdForm.code
        }
        confirmForgetPwd(this.verifyCode, setPwdForm).then(res => {
          this.isLoading = false;
          this.loading = false;
          if (res.code === 0) {
            this.isSuc = false;
            this.isDone = true;
          }
        })
      }
    },
    backLogin() {
      this.$router.push({path: "/login"});
    }
  },
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>

.title {
  text-align: center;
}

.set-pwd-code {
  width: 33%;
  height: 38px;
  float: right;
  img {
    cursor: pointer;
    vertical-align: middle;
  }
}

.set-pwd-code-img {
  height: 38px;
}

</style>

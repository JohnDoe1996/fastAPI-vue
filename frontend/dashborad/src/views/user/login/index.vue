<template>
  <user-layout>
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules">
      <el-form-item prop="user">
        <el-input v-model="loginForm.user" type="text" auto-complete="off" placeholder="用户名/邮箱">
          <svg-icon slot="prefix" icon-class="user" class="el-input__icon input-icon"/>
        </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="loginForm.password"
          type="password"
          auto-complete="off"
          placeholder="密码"
          show-password
          @keyup.enter.native="handleLogin"
        >
          <svg-icon slot="prefix" icon-class="password" class="el-input__icon input-icon"/>
        </el-input>
      </el-form-item>
      <el-form-item prop="code"  v-if="useCaptcha">
        <el-input
          v-model="loginForm.code"
          auto-complete="off"
          placeholder="验证码"
          style="width: 63%"
        >
          <svg-icon slot="prefix" icon-class="validCode" class="el-input__icon input-icon"/>
        </el-input>
        <div class="login-code">
          <img :src="codeImg" class="login-code-img" @click="getCode">
        </div>
      </el-form-item>
      <div style="display: flex; justify-content: space-between;">
        <el-checkbox v-model="loginForm.rememberMe" style="margin:0px 0px 25px 0px;">记住密码</el-checkbox>
        <router-link :to="{path: '/forget-password', query: allQuery}" style="color: blue; font-size: 14px; margin:0px 0px 25px 0px;">忘记密码?</router-link>
      </div>
      <el-form-item style="width:100%;">
        <el-button
          :loading="loading"
          size="medium"
          type="primary"
          style="width:100%;"
          @click.native.prevent="handleLogin"
        >
          <span v-if="!loading">登 录</span>
          <span v-else>登 录 中...</span>
        </el-button>
        <div style="color: blue; font-size: 13px; text-align: center;">
          <router-link :to="{path: '/register', query: allQuery}">还没有账号？</router-link>
        </div>
      </el-form-item>
    </el-form>
  </user-layout>
</template>

<script>
import Cookies from "js-cookie";
import { decrypt, encrypt } from "@/utils/jsencrypt";
import UserLayout from '../layout'

import { getCaptchaCode } from '@/api/user'

export default {
  name: 'Login',
  components: { UserLayout },
  data() {
    const validatePassword = (rule, value, callback) => {
      if (value == ''){
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码长度不小于6位'))
      } else {
        callback()
      }
    }
    return {
      useCaptcha: false,
      loginForm: {
        user: '',
        password: '',
        code: '',
        key: '',
      },
      rememberMe: false,
      loginRules: {
        user: [{ required: true, trigger: 'blur', message: "请输入用户名/邮箱" }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        // code: [{required: true, message: '请输入验证码', trigger: 'blur' }],
      },
      passwordType: 'password',
      capsTooltip: false,
      loading: false,
      showDialog: false,
      redirect: undefined,
      codeImg: "",
      allQuery: {},
      otherQuery: {}
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        const query = route.query;
        this.allQuery = query;
        if (query) {
          this.redirect = query.redirect;
          this.otherQuery = this.getOtherQuery(query);
        }
      },
      immediate: true
    }
  },
  created() {
    this.getCode();
    this.getCookie()
  },
  methods: {
    getCode() {
      getCaptchaCode().then( res => {
        if (res.code === 0) {
          if (res.data.key) {
            this.useCaptcha = true;
            this.loginRules['code'] = [{required: true, message: '请输入验证码', trigger: 'blur' }];
            this.codeImg = res.data.img;
            this.loginForm.key = res.data.key;
          }
        }
      })
    },
    getCookie() {
      const username = Cookies.get("username");
      const password = Cookies.get("password");
      const rememberMe = Cookies.get("rememberMe");
      this.loginForm = {
        username: username === undefined ? this.loginForm.user : username,
        password: password === undefined ? this.loginForm.password : decrypt(password),
        rememberMe: rememberMe === undefined ? false : Boolean(rememberMe)
      };
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
           if (this.rememberMe) {
            Cookies.set("username", this.loginForm.user, { expires: 30 });
            Cookies.set("password", encrypt(this.loginForm.password), { expires: 30 });
            Cookies.set("rememberMe", this.rememberMe, { expires: 30 });
          } else {
            Cookies.remove("username");
            Cookies.remove("password");
            Cookies.remove("rememberMe");
          }
          console.log(this.loginForm)
          this.$store.dispatch('user/login', this.loginForm).then(res => {
              console.log(res);
              if (res.code === 0) {
                this.$router.push({ path: this.redirect || '/', query: this.otherQuery })
              } else {
                this.getCode();
              }
              this.loading = false
            })
            .catch(() => {
              this.getCode();
              this.loading = false
            })
        } else {
          console.log('登录失败')
          return false
        }
      })
    },
    getOtherQuery(query) {
      return Object.keys(query).reduce((acc, cur) => {
        if (cur !== 'redirect') {
          acc[cur] = query[cur]
        }
        return acc
      }, {})
    }
  }
}
</script>

<style lang="scss">


.login-form {
  border-radius: 6px;
  background: #ffffff;
  width: 400px;
  padding: 25px 25px 5px 25px;
  .el-input {
    height: 38px;
    input {
      height: 38px;
    }
  }
  .input-icon {
    height: 39px;
    width: 14px;
    margin-left: 2px;
  }
}
.login-tip {
  font-size: 13px;
  text-align: center;
  color: #bfbfbf;
}
.login-code {
  width: 33%;
  height: 38px;
  float: right;
  img {
    cursor: pointer;
    vertical-align: middle;
  }
}
.el-login-footer {
  height: 40px;
  line-height: 40px;
  position: fixed;
  bottom: 0;
  width: 100%;
  text-align: center;
  color: #fff;
  font-family: Arial;
  font-size: 12px;
  letter-spacing: 1px;
}
.login-code-img {
  height: 38px;
}

</style>

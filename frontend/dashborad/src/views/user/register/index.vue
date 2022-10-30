<template>
  <user-layout>
    <el-form ref="registerForm" :model="registerForm" :rules="registerRules">
      <el-form-item prop="username">
        <el-input v-model="registerForm.username" type="text" auto-complete="off" placeholder="用户名">
          <svg-icon slot="prefix" icon-class="user" class="el-input__icon input-icon" />
        </el-input>
      </el-form-item>
      <el-form-item prop="email">
        <el-input v-model="registerForm.email" type="text" auto-complete="off" placeholder="邮箱">
          <svg-icon slot="prefix" icon-class="email" class="el-input__icon input-icon" />
        </el-input>
      </el-form-item>
      <el-form-item prop="mobile">
        <el-input v-model="registerForm.phone" type="text" auto-complete="off" placeholder="手机号码">
          <svg-icon slot="prefix" icon-class="phone" class="el-input__icon input-icon" />
        </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="registerForm.password"
          type="password"
          auto-complete="off"
          placeholder="密码"
          show-password
          @keyup.enter.native="handleRegister"
        >
          <svg-icon slot="prefix" icon-class="password" class="el-input__icon input-icon" />
        </el-input>
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <el-input
          v-model="registerForm.confirmPassword"
          type="password"
          auto-complete="off"
          placeholder="再次输入密码"
          show-password
          @keyup.enter.native="handleRegister"
        >
          <svg-icon slot="prefix" icon-class="eye" class="el-input__icon input-icon" />
        </el-input>
      </el-form-item>
      <el-form-item prop="code">
        <el-input
          v-model="registerForm.code"
          auto-complete="off"
          placeholder="验证码"
          style="width: 63%"
        >
          <svg-icon slot="prefix" icon-class="validCode" class="el-input__icon input-icon" />
        </el-input>
        <div class="register-code">
          <img :src="codeImg" class="register-code-img" @click="getCode">
        </div>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button
          :loading="loading"
          size="medium"
          type="primary"
          style="width:100%;"
          @click.native.prevent="handleRegister"
        >
          <span v-if="!loading">注 册</span>
          <span v-else>提 交 中...</span>
        </el-button>
        <div style="color: blue; font-size: 13px; text-align: center;">
          <router-link :to="{path: '/login', query: allQuery}">返回登录</router-link>
        </div>
      </el-form-item>
    </el-form>
  </user-layout>
</template>

<script>
import UserLayout from '../layout'
import {register} from "@/api/user";
import {getCaptchaCode} from "@/api/user";
import {deepClone} from "@/utils";
import md5 from 'js-md5'


export default {
  name: "index",
  components: {UserLayout},
  data() {
    return {
      cookiePassword: "",
      registerForm: {
        username: "",
        email: "",
        phone: "",
        password: "",
        confirmPassword: "",
        code: "",
        key: ""
      },
      registerRules: {
        username: [
          { required: true, trigger: "blur", message: "用户名不能为空" },
          { pattern: /^[a-zA-Z]{1}([a-zA-Z0-9]|[-_]){4,19}$/, trigger: "blur", message: "只能输入5-20个以字母开头、可带数字、“_”、“-”的字串"},
        ],
        email: [
          { required: true, trigger: "blur", message: "邮箱不能为空" },
          { type: "email", trigger: "blur", message: "请输入正确的邮箱地址"},
        ],
        phone: [
          { required: true, trigger: "blur", message: "手机号不能为空" },
          { pattern: /^1[2-9][0-9]\d{8}$/, message: "请输入正确的手机号码", trigger: "blur"},
        ],
        password: [
          { required: true, trigger: "blur", message: "密码不能为空" },
        ],
        confirmPassword: [
          { required: true, trigger: "blur", message: "确认密码不能为空" },
        ],
        code: [{ required: true, trigger: "change", message: "验证码不能为空" }]
      },
      codeImg: "",
      allQuery: {},
      otherQuery: {},
      loading: false,
      redirect: undefined
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
    this.getCode()
  },
  methods: {
    getCode() {
      getCaptchaCode().then( res => {
        if (res.code === 0) {
          this.codeImg = res.data.img;
          this.registerForm.key = res.data.key;
        }
      })
    },
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.loading = true;
          const registerForm = deepClone(this.registerForm);
          registerForm.password = md5(registerForm.password);
          registerForm.confirmPassword = md5(registerForm.confirmPassword);
          register(registerForm).then(res => {
            if(res.code === 0){
              this.$notify.success({
              title: '注册成功',
              duration: 3000,
              showClose: true,
              message: '注册成功，请注意查收验证邮箱，验证后方可登录。',
              onClose: () => {
                this.$router.push({ path: this.redirect || "/login" }).catch(() => {});
              }
            })
            }
          }).catch(() => {
            this.loading = false;
            this.getCode();
          });
        }
      });
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

<style rel="stylesheet/scss" lang="scss" scoped>
.register-tip {
  font-size: 13px;
  text-align: center;
  color: #bfbfbf;
}

.register-code {
  width: 33%;
  height: 38px;
  float: right;
  img {
    cursor: pointer;
    vertical-align: middle;
  }
}

.register-code-img {
  height: 38px;
}
</style>

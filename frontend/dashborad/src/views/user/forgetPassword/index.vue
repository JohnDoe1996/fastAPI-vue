<template>
  <user-layout>
    <el-form ref="forgetForm" :model="forgetForm" :rules="forgetRules">
      <el-form-item prop="email">
        <el-input v-model="forgetForm.email" type="text" auto-complete="off" placeholder="邮箱">
          <svg-icon slot="prefix" icon-class="email" class="el-input__icon input-icon" />
        </el-input>
      </el-form-item>
      <el-form-item prop="code">
        <el-input
          v-model="forgetForm.code"
          auto-complete="off"
          placeholder="验证码"
          style="width: 63%"
        >
          <svg-icon slot="prefix" icon-class="validCode" class="el-input__icon input-icon" />
        </el-input>
        <div class="forget-code">
          <img :src="codeImg" class="forget-code-img" @click="getCode">
        </div>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button
          :loading="loading"
          size="medium"
          type="primary"
          style="width:100%;"
          @click.native.prevent="handleForget"
        >
          <span v-if="!loading">提 交</span>
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
import {forgetPassword, getCaptchaCode, register} from "@/api/user";

export default {
  name: "ForgetPassword",
  components: {UserLayout},
  data() {
    return {
      cookiePassword: "",
      forgetForm: {
        email: "",
        password: "",
        code: "",
        key: ""
      },
      forgetRules: {
        email: [
          { required: true, trigger: "blur", message: "邮箱不能为空" },
          { type: "email", trigger: "blur", message: "请输入正确的邮箱地址"},
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
          this.forgetForm.key = res.data.key;
        }
      })
    },
    handleForget() {
      this.$refs.forgetForm.validate(valid => {
        if (valid) {
          this.loading = true;
          forgetPassword(this.forgetForm).then(res => {
            if(res.code === 0){
              this.$notify.success({
              title: '提交成功',
              duration: 3000,
              showClose: true,
              message: '提交成功，请注意查收验证邮箱，打开邮件中的链接重置密码。',
              onClose: () => {
                this.$router.push({ path: this.redirect || "/login" });
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

.forget-code {
  width: 33%;
  height: 38px;
  float: right;
  img {
    cursor: pointer;
    vertical-align: middle;
  }
}

.forget-code-img {
  height: 38px;
}
</style>

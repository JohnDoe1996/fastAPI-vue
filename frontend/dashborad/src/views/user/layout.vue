<template>
  <div class="user-page">
    <div class="user-page-form">
<!--      <h3 class="title">{{ title }}</h3>-->
      <slot></slot>
    </div>
    <!--  底部  -->
    <div class="el-user-page-footer">

    </div>
  </div>
</template>

<script>

export default {
  name: "UserLayout",
  data() {
    return {
      title: process.env.VUE_APP_TITLE || "",
    };
  },
};
</script>

<style rel="stylesheet/scss" lang="scss">
.user-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-size: cover;
  background-image: url("../../assets/images/login-background.jpg");
}
.title {
  margin: 0px auto 30px auto;
  text-align: center;
  color: #707070;
}

.user-page-form {
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

.el-user-page-footer {
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

.logo-w {
    width: 300px;
    height: 80px;
    vertical-align: middle;
    margin-right: 12px;
    margin-bottom: 10px;
}
</style>


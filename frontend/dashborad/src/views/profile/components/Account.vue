<template>
  <el-form ref="form" :model="form" :rules="rules" label-width="80px">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="form.username" placeholder="请输入昵称"/>
    </el-form-item>
    <el-form-item label="用户昵称" prop="nickname">
      <el-input v-model="form.nickname" placeholder="请输入昵称"/>
    </el-form-item>
    <el-form-item label="手机号码" prop="phone">
      <el-input v-model="form.phone" maxlength="11" />
    </el-form-item>
    <el-form-item label="邮箱" prop="email">
      <el-input v-model="form.email" maxlength="50" />
    </el-form-item>
    <el-form-item label="性别" prop="sex">
      <el-radio-group v-model="form.sex">
        <el-radio
          v-for="(dict,index) in sexOptions"
          :key="index"
          :label="dict.value"
        >{{ dict.label }}
        </el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" size="mini" @click="submit">保存</el-button>
<!--      <el-button type="danger" size="mini" @click="close">关闭</el-button>-->
    </el-form-item>
  </el-form>
</template>

<script>

import { changeInfo } from "@/api/user";

export default {
  props: {
    user: {
      type: Object
    }
  },
  data() {
    return {
      form: {},
      // 表单校验
      rules: {
        username: [
          { required: true, message: "用户名不能为空", trigger: "blur" }
        ],
        nickname: [
          { required: true, message: "用户昵称不能为空", trigger: "blur" }
        ],
        email: [
          { required: true, message: "邮箱地址不能为空", trigger: "blur" },
          { type: "email", message: "'请输入正确的邮箱地址", trigger: ["blur", "change"] }
        ],
        phone: [
          { required: true, message: "手机号码不能为空", trigger: "blur" },
          { pattern: /^1[2-9][0-9]\d{8}$/, message: "请输入正确的手机号码", trigger: "blur" }
        ],
        sex: [
          { required: true, message: "性别不能为空", trigger: "blur" }
        ]
      },
      // 性别状态字典
      sexOptions: [],
    };
  },
  created() {
    this.form = {
      username: this.user.username,
      nickname: this.user.nickname,
      phone: this.user.phone,
      email: this.user.email,
      sex: this.user.sex,
    }
    this.getDicts("permission_user_sex").then(response => {
      this.sexOptions = response.data.details;
    });
  },
  methods: {
    submit() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          changeInfo(this.form).then( response => {
            this.msgSuccess("修改成功");
          });
        }
      });
    },
    close() {
      this.$store.dispatch("tagsView/delView", this.$route);
      this.$router.push({ path: "/index" });
    }
  }
};
</script>

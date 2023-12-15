<template>
  <div class="app-container">
    <div v-if="user">
      <el-row :gutter="20">

        <el-col :span="6" :xs="24">
          <user-card :user="user" />
        </el-col>

        <el-col :span="18" :xs="24">
          <el-card>
            <el-tabs v-model="activeTab">
              <el-tab-pane label="修改信息" name="account">
                <account :user="user" />
              </el-tab-pane>
              <el-tab-pane label="修改密码" name="password">
                <reset-pwd></reset-pwd>
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>

      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import UserCard from './components/UserCard'
import Account from './components/Account'
import ResetPwd from './components/ResetPwd'

export default {
  name: 'Profile',
  components: { UserCard, Account, ResetPwd },
  data() {
    return {
      user: {},
      activeTab: 'account'
    }
  },
  computed: {
    ...mapGetters([
      'username',
      'nickname',
      'email',
      'phone',
      'avatar',
      'sex',
      'roles_name',
      'roles'
    ])
  },
  created() {
    this.getUser()
  },
  methods: {
    getUser() {
      this.user = {
        username: this.username,
        nickname: this.nickname,
        phone: this.phone,
        role: this.roles_name.join(' | '),
        email: this.email,
        avatar: this.avatar,
        sex: this.sex
      }
    }
  }
}
</script>

<template>
  <el-card style="margin-bottom:20px;">
    <div slot="header" class="clearfix">
      <span>个人信息</span>
    </div>

    <div class="user-profile">
      <div class="box-center">
<!--        <pan-thumb :image="fileBase + user.avatar" :height="'100px'" :width="'100px'" :hoverable="false">-->
<!--          <div>Hello</div>-->
<!--          {{ user.nickname }}-->
<!--        </pan-thumb>-->
      <user-avatar :user="user"></user-avatar>
      </div>
      <div class="box-center">
        <div class="user-name text-center">{{ user.nickname }}</div>
        <div class="user-role text-center text-muted">{{ user.role | uppercaseFirst }}</div>
      </div>
      <div>
        <ul class="list-group list-group-striped">
          <li class="list-group-item">
            <svg-icon icon-class="user"/>
            用户名称
            <div class="pull-right">{{ user.username }}</div>
          </li>
          <li class="list-group-item">
            <svg-icon icon-class="phone"/>
            手机号码
            <div class="pull-right">{{ user.phone }}</div>
          </li>
          <li class="list-group-item">
            <svg-icon icon-class="email"/>
            用户邮箱
            <div class="pull-right">{{ user.email }}</div>
          </li>
        </ul>
      </div>
    </div>

  </el-card>
</template>

<script>
import PanThumb from '@/components/PanThumb'
import userAvatar from "./userAvatar";
import UserAvatar from "@/views/profile/components/userAvatar";

export default {
  components: {UserAvatar, PanThumb },
  data () {
    return {
      fileBase: process.env.VUE_APP_MEDIA_BASE,
      defaultAvatar: "images/avatar/default/avatar.jpg",
    }
  },
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          name: '',
          email: '',
          avatar: '',
          role: ''
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.box-center {
  margin: 0 auto;
  display: table;
}

.text-muted {
  color: #777;
}

.user-profile {
  .user-name {
    font-weight: bold;
  }

  .box-center {
    padding-top: 10px;
  }

  .user-role {
    padding-top: 10px;
    font-weight: 400;
    font-size: 14px;
  }

  .box-social {
    padding-top: 30px;

    .el-table {
      border-top: 1px solid #dfe6ec;
    }
  }

  .user-follow {
    padding-top: 20px;
  }
}

.user-bio {
  margin-top: 20px;
  color: #606266;

  span {
    padding-left: 4px;
  }

  .user-bio-section {
    font-size: 14px;
    padding: 15px 0;

    .user-bio-section-header {
      border-bottom: 1px solid #dfe6ec;
      padding-bottom: 10px;
      margin-bottom: 10px;
      font-weight: bold;
    }
  }
}
</style>

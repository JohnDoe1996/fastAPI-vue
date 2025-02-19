<template>
  <div class="app-container">
    <el-form ref="queryForm" :model="queryParams" :inline="true" label-width="68px">
      <el-form-item label="编号" prop="id">
        <el-input
          v-model="queryParams.id"
          placeholder="请输入用户编号"
          clearable
          size="small"
          style="width: 200px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="用户名" prop="nickname">
        <el-input
          v-model="queryParams.username"
          placeholder="请输入用户名"
          clearable
          size="small"
          style="width: 200px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="昵称" prop="nickname">
        <el-input
          v-model="queryParams.nickname"
          placeholder="请输入用户昵称"
          clearable
          size="small"
          style="width: 200px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="邮箱" prop="username">
        <el-input
          v-model="queryParams.email"
          placeholder="请输入用户邮箱"
          clearable
          size="small"
          style="width: 200px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="手机号码" prop="nickname">
        <el-input
          v-model="queryParams.phone"
          placeholder="请输入用户手机号"
          clearable
          size="small"
          style="width: 200px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="用户状态" clearable size="small" style="width: 200px">
          <el-option v-for="dict in statusOptions" :key="dict.id" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间">
        <el-date-picker
          v-model="dateRange"
          size="small"
          style="width: 240px"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="~"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" icon="el-icon-plus" size="mini" @click="handleAdd">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" icon="el-icon-edit" size="mini" :disabled="single" @click="handleUpdate">修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
        >删除
        </el-button>
      </el-col>
    </el-row>

    <el-table v-loading="loading" :data="userList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="50" align="center" />
      <el-table-column label="编号" align="center" prop="id" width="55" :show-overflow-tooltip="true" />
      <el-table-column label="用户名" align="center" prop="username" :show-overflow-tooltip="true" />
      <el-table-column label="昵称" align="center" prop="nickname" :show-overflow-tooltip="true" />
      <el-table-column label="邮箱" align="center" prop="email" :show-overflow-tooltip="true" />
      <el-table-column label="手机号码" align="center" prop="phone" width="120" />
      <el-table-column label="活跃" align="center" prop="is_active" width="60">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.is_active" @change="handleChangIsActive(scope.row)"></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="状态" align="center" prop="status" width="70" :formatter="statusFormat"/>
      <el-table-column label="创建时间" align="center" prop="created_ts">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.created_ts) }}</span>
        </template>
      </el-table-column>
<!--      <el-table-column label="更新时间" align="center" prop="modified_ts">-->
<!--        <template slot-scope="scope">-->
<!--          <span>{{ parseTime(scope.row.modified_ts) }}</span>-->
<!--        </template>-->
<!--      </el-table-column>-->
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button size="mini" type="text" icon="el-icon-edit" @click="handleUpdate(scope.row)">修改</el-button>
          <el-button size="mini" type="text" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          <el-button size="mini" type="text" icon="el-icon-key" @click="handleResetPwd(scope.row)">重置</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.page"
      :limit.sync="queryParams.limit"
      @pagination="getList"
    />

    <!-- 添加或修改参数配置对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="600px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户昵称" prop="nickname">
              <el-input v-model="form.nickname" placeholder="请输入用户昵称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username" placeholder="请输入用户名" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号码" maxlength="11" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" placeholder="请输入邮箱" maxlength="18" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户性别" prop="sex">
              <el-select v-model="form.sex" placeholder="请选择">
                <el-option v-for="dict in sexOptions" :key="dict.value" :label="dict.label" :value="dict.value" />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择">
                <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户头像" prop="avatar">
              <avatar-upload v-if="open" :avatar="fileBase + form.avatar" @uploadAvatar="uploadPicture"/>
              <span class="upload-img-tip">提示：点击图片可进行裁剪和上传</span>
              <el-upload
                class="avatar-uploader"
                :headers="headers"
                :action="uploadAvatarUrl"
                accept=".jpg,.png,.ico,.gif,.jpeg,.tiff"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :on-error="handleAvatarError"
                :before-upload="beforeAvatarUpload"
                name="img"
                size="mini">
                <el-button type="primary" size="mini">上传</el-button>
                <el-button type="success" size="mini" @click.stop="handleDefaultImg">默认</el-button>
              </el-upload>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色" prop="roles">
              <el-select v-model="form.roles" multiple placeholder="请选择">
                <el-option v-for="item in roleOptions" :key="item.id" :label="item.name" :value="item.id">
                  <span style="float: left">{{ item.name }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px; margin-right: 15px;">{{ item.key }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import {
  listUser,
  getUser,
  delUser,
  addUser,
  updateUser,
  resetUserPwd,
  changeUserIsActive
} from '@/api/permission/user'
import {getRoleSelectList} from "@/api/permission/role";
import '@riophae/vue-treeselect/dist/vue-treeselect.css'

import AvatarUpload from './AvatarUpload'
import {getToken} from "@/utils/auth";


export default {
  name: 'User',
  components: {AvatarUpload},
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 总条数
      total: 0,
      // 用户表格数据
      userList: null,
      // 弹出层标题
      title: '',

      // 是否显示弹出层
      open: false,
      // 部门名称
      deptName: undefined,
      // 日期范围
      dateRange: [],
      // 状态数据字典
      statusOptions: [], defaultStatusValue: undefined,
      // 性别状态字典
      sexOptions: [], defaultSexValue: undefined,
      // 角色选项
      roleOptions: [], defaultRolesId: [],
      // 表单参数
      form: {},
      defaultProps: {
        children: 'children',
        label: 'name'
      },
      // 查询参数
      queryParams: {
        page: 1,
        limit: 20,
        id: undefined,
        username: undefined,
        nickname: undefined,
        email: undefined,
        phone: undefined,
        status: undefined,
        created_after_ts: undefined,
        created_before_ts: undefined,
      },
      // 头像
      fileBase: process.env.VUE_APP_MEDIA_BASE,
      defaultAvatar: "images/avatar/default/avatar.jpg",
      // 设置上传的请求头部
      headers: { Authorization: "Token " + getToken() },
      // 上传网站图片地址
      uploadAvatarUrl: process.env.VUE_APP_BASE_API + "permission/user/profile/avatar",
      // 表单校验
      rules: {
        username: [
          { required: true, message: '用户编号不能为空', trigger: 'blur' },
          { pattern: /^[a-zA-Z]{1}([a-zA-Z0-9]|[-_]){4,19}$/, trigger: "blur", message: "只能输入5-20个以字母开头的字串"},
        ],
        nickname: [
          { required: true, message: '用户名称不能为空', trigger: 'blur' }
        ],
        roles: [
          { required: true, message: '角色不能为空', trigger: 'blur' }
        ],
        email: [
          { required: true, trigger: "blur", message: "邮箱不能为空" },
          { type: "email",trigger: "blur", message: "请输入正确的邮箱地址" },
        ],
        phone: [
          { required: true, message: '手机号码不能为空', trigger: 'blur' },
          {
            pattern: /^1[2|3|4|5|6|7|8|9][0-9]\d{8}$/,
            message: '请输入正确的手机号码',
            trigger: 'blur'
          }
        ],
        sex: [
          { required: true, message: '性别不能为空', trigger: 'blur' }
        ],
        status: [
          { required: true, message: '状态不能为空', trigger: 'blur' }
        ]
      },
    }
  },
  created() {
    this.getList()
    this.getDicts('permission_user_status').then(response => {
      this.statusOptions = response.data.details
      this.statusOptions.forEach( item => { if (item.is_default) this.defaultStatusValue = item.value })
    })
    this.getDicts('permission_user_sex').then(response => {
      this.sexOptions = response.data.details;
      this.sexOptions.forEach(item => { if (item.is_default) this.defaultSexValue = item.value })
    })
    getRoleSelectList().then( response => {
      this.roleOptions = response.data.roles;
      this.getParameter('user_init_roles').then(response => {
        if (response.code === 0) {
          let values = response.data.value.split(',');
          this.defaultRolesId = [];
          this.roleOptions.forEach( item => {
            if (values.indexOf(item.key) >= 0) {
              this.defaultRolesId.push(item.id)
            }
          })
        }
      })
    })
  },
  methods: {
    /** 查询用户列表 */
    getList() {
      this.loading = true
      console.log(this.dateRange);
      if (this.dateRange.length > 0){
        this.queryParams.created_after_ts = parseInt((new Date(this.dateRange[0] + " 00:00:00")).getTime() / 1000);
        this.queryParams.created_before_ts = parseInt((new Date(this.dateRange[1] + " 23:59:59")).getTime() / 1000);
      }
      console.log(this.queryParams)
      listUser(this.queryParams).then(response => {
        this.userList = response.data.results
        this.total = response.data.total
        this.loading = false
      })
    },
    // 字典状态字典翻译
    statusFormat(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    // 取消按钮
    cancel() {
      this.open = false
      this.reset()
    },
    // 表单重置
    reset() {
      this.form = {
        id: undefined,
        username: undefined,
        nickname: undefined,
        phone: undefined,
        sex: this.defaultSexValue,
        status: this.defaultStatusValue,
        email: undefined,
        is_activate: true,
        roles: this.defaultRolesId,
        avatar: this.defaultAvatar,
      }
      this.resetForm('form')
    },
    reset_query() {
      this.queryParams = {
        page: 1,
        limit: 20,
        id: undefined,
        username: undefined,
        nickname: undefined,
        email: undefined,
        phone: undefined,
        status: undefined,
        created_after_ts: undefined,
        created_before_ts: undefined,
      }
      this.dateRange = []
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.page = 1
      this.getList()
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.reset_query()
      this.handleQuery()
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length !== 1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset()
      this.open = true
      this.title = '添加用户'
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset()
      const userId = row.id || this.ids
      getUser(userId).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改用户'
      })
    },
    /** 重置密码按钮操作 */
    handleResetPwd(row) {
      this.$prompt('请输入"' + row.username + '-' + row.nickname + '"的新密码', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(({ value }) => {
        resetUserPwd(row.id, value).then(response => {
          if (response.code === 0) {
            this.msgSuccess('修改成功，新密码是：' + value)
          } else {
            this.msgSuccess(response.msg)
          }
        })
      }).catch(() => {
      })
    },
    /** 改变活跃状态 */
    handleChangIsActive(row) {
      console.log(row.is_active)
      changeUserIsActive(row.id, row.is_active).then(response => {
        if(response.code === 0) {
          this.msgSuccess("修改成功")
        }
        this.getList();
      })
    },
    /** 提交按钮 */
    submitForm: function() {
      this.$refs['form'].validate(valid => {
        if (valid) {
          if (this.form.id !== undefined) {
            updateUser(this.form.id, this.form).then(response => {
              if (response.code === 0) {
                this.msgSuccess("修改成功")
                this.open = false
                this.getList()
              }
            })
          } else {
            addUser(this.form).then(response => {
              if (response.code === 0) {
                this.msgSuccess("添加成功")
                this.open = false
                this.getList()
              }
            })
          }
        }
      })
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const userIds = row.id || this.ids
      this.$confirm('是否确认删除数据?', '警告', {
        confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
      }).then(function() {
        return delUser(userIds)
      }).then(() => {
        this.getList()
        this.msgSuccess('删除成功')
      }).catch(function() {
      })
    },

    // 设置默认图片
    handleDefaultImg() {
      this.form.avatar = this.defaultAvatar;
    },
    //修改图片后的回传事件
    uploadPicture(path){
      this.form.avatar = path;
    },
    handleAvatarSuccess(res) {
      if (res.code == 0) {
        this.form.avatar = res.data.path;
      } else {
        this.msgError("上传网站图片失败！");
      }
    },
    handleAvatarError(err, file, fileList) {
     this.msgError(err);
    },
    beforeAvatarUpload(file) {
      const imgType = ['image/jpeg','image/x-icon'];
      const isJPG = imgType.map(function (type) {
        return file.type === type;
      });
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.msgError('上传图片只能是 JPG、PNG 格式!');
      }
      if (!isLt2M) {
        this.msgError('上传图片大小不能超过 2MB!');
      }
      return isJPG && isLt2M;
    },
  }
}
</script>

<style scoped>

.upload-img-tip {
  font-size: 10px;
}

</style>

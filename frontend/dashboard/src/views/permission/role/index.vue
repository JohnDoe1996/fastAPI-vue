<template>
  <div class="app-container">
    <el-form ref="queryForm" :model="queryParams" :inline="true" label-width="68px">
      <el-form-item label="角色名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入角色名称"
          clearable
          size="small"
          style="width: 200px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="角色描述" prop="description">
        <el-input
          v-model="queryParams.key"
          placeholder="请输入角色描述"
          clearable
          size="small"
          style="width: 200px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择菜单状态" clearable size="small" @change="handleQuery">
          <el-option
            :key="undefined"
            :label="'全部'"
            :value="undefined"
          />
          <el-option
            v-for="dict in statusOptions"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
        >新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
        >修改
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

    <el-table v-loading="loading" :data="list" @selection-change="handleSelectionChange">i
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="编号" align="center" prop="id" width="55"/>
      <el-table-column label="名称" align="center" prop="name" :show-overflow-tooltip="true"/>
      <el-table-column label="描述" align="center" prop="key" :show-overflow-tooltip="true"/>
      <el-table-column label="排序" align="center" prop="order_num" :show-overflow-tooltip="true" width="55"/>
      <el-table-column label="状态" align="center" prop="status" :formatter="statusFormat" :show-overflow-tooltip="true"/>
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
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
          >删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.page"
      :limit.sync="queryParams.page_size"
      @pagination="getList"
    />

    <!-- 添加或修改参数配置对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入参数名称" />
        </el-form-item>
        <el-form-item label="角色描述" prop="key">
          <el-input v-model="form.key" placeholder="请输入参数键" />
        </el-form-item>
        <el-row>
          <el-col :span="12">
            <el-form-item label="显示排序" prop="order_num">
              <el-input-number v-model="form.order_num" controls-position="right" :min="0" style="width: 100%"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio
                  v-for="dict in statusOptions"
                  :key="dict.value"
                  :label="dict.value"
                >{{ dict.label }}</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
         <el-form-item label="菜单权限">
          <el-checkbox v-model="menuExpand" @change="handleCheckedTreeExpand($event, 'menu')">展开/折叠</el-checkbox>
          <el-checkbox v-model="menuNodeAll" @change="handleCheckedTreeNodeAll($event, 'menu')">全选/全不选</el-checkbox>
          <el-checkbox v-model="form.menuCheckStrictly" @change="handleCheckedTreeConnect($event, 'menu')">父子联动</el-checkbox>
          <el-tree
            ref="menu"
            class="tree-border"
            :data="menuOptions"
            show-checkbox
            node-key="id"
            :check-strictly="!form.menuCheckStrictly"
            empty-text="加载中，请稍后"
            :props="defaultProps"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {getDicts} from '@/api/system/dict/data'
import {addRole, delRole, getRole, getRoleMaxOrderNum, listRole, setRole, setRoleMenus} from "@/api/permission/role";
import {listselect} from "@/api/permission/menu";

export default {
  name: 'Role',
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
      // 字典表格数据
      list: [],
      // 弹出层标题
      title: '',
      // 是否显示弹出层
      open: false,
      statusOptions: [],
      // 查询参数
      queryParams: {
        page: 1,
        page_size: 20,
        name: undefined,
        description: undefined
      },
      // 菜单列表
      menuOptions: [],
      defaultProps: {
        children: "children",
        label: "title"
      },
      menuExpand: false,
      menuNodeAll: false,
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        name: [
          { required: true, message: '角色名称不能为空', trigger: 'blur' }
        ],
      }
    }
  },
  created() {
    this.getList()
    getDicts("com_default_status").then(response => {
      this.statusOptions = response.data.details;
    })
  },
  methods: {
    /** 查询字典类型列表 */
    getList() {
      this.loading = true
      listRole(this.queryParams).then(response => {
        this.list = response.data.results
        this.total = response.data.total
        this.loading = false
      }
      )
    },
    /** 查询菜单树结构 */
    getMenuTreeselect() {
      // treeselect().then(response => {
      //   this.menuOptions = response.data.menus
      // })
      listselect().then(response => {
        this.menuOptions = this.handleTree(response.data.menus, "id");
      });
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
        key: undefined,
        name: undefined,
        status: undefined,
        order_num: undefined,
        menus: [],
        menuCheckStrictly: true,
      }
      this.resetForm('form')
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.page = 1
      this.getList()
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.queryParams = {
        page: 1,
        page_size: 20,
        name: undefined,
        key: undefined,
        status: undefined
      }
      this.handleQuery()
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset()
      this.open = true
      this.title = '添加角色'
      this.getMenuTreeselect();
      getRoleMaxOrderNum().then(response => {
        this.form.order_num = response.data.max_order_num + 1
      })
      this.statusOptions.forEach(item => { if (item.is_default) this.form.status = item.value })
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length !== 1
      this.multiple = !selection.length
    },
    // 树权限（展开/折叠）
    handleCheckedTreeExpand(value, type) {
      if (type === "menu") {
        const treeList = this.menuOptions;
        for (let i = 0; i < treeList.length; i++) {
          this.$refs.menu.store.nodesMap[treeList[i].id].expanded = value;
        }
      }
    },
    // 树权限（全选/全不选）
    handleCheckedTreeNodeAll(value, type) {
      if (type === "menu") {
        this.$refs.menu.setCheckedNodes(value ? this.menuOptions : []);
      }
    },
    // 树权限（父子联动）
    handleCheckedTreeConnect(value, type) {
      if (type === "menu") {
        this.form.menuCheckStrictly = !!value;
      }
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset()
      this.getMenuTreeselect();
      const id = row.id || this.ids
      getRole(id).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改参数'
        setTimeout(()=>{this.$refs.menu.setCheckedNodes(response.data.menus)}, 200)
      })
    },
    /** 提交按钮 */
    submitForm: function() {
      this.$refs['form'].validate(valid => {
        if (valid) {
          this.form.menus = this.$refs.menu.getCheckedKeys();
          if (this.form.id !== undefined) {
            setRole(this.form.id, this.form).then(response => {
              if (response.code === 0) {
                this.msgSuccess("角色修改成功")
                this.open = false
                this.getList()
                setRoleMenus(this.form.id, this.form.menus).then(response => {
                  if (response.code === 0) {
                    this.getList()
                  } else {
                    this.msgError("菜单权限修改失败," + response.msg)
                  }
                });
              } else {
                this.msgError("角色修改失败," + response.msg)
              }
            })

          } else {
            addRole(this.form).then(response => {
              if (response.code === 0) {
                this.msgSuccess("添加成功")
                this.open = false
                this.getList()
              } else {
                this.msgError("添加失败," + response.msg)
              }
            })
          }
        }
      })
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const ids = row.id || this.ids
      this.$confirm('是否确认删除字典编号为"' + ids + '"的数据项?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function() {
        return delRole(ids)
      }).then(() => {
        this.getList()
        this.msgSuccess('删除成功')
      }).catch(function() {
      })
    }
  }
}
</script>


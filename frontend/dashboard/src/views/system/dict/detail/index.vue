<template>
  <div class="app-container">
    <el-form ref="queryForm" :model="queryParams" :inline="true">
      <el-form-item label="字典名称" prop="dictType">
        <el-select v-model="queryParams.dict_data_id" size="small" >
          <el-option
            v-for="item in typeOptions"
            :key="item.id"
            :label="item.dict_name + ' ' + item.dict_type"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="字典标签" prop="dictLabel">
        <el-input
          v-model="queryParams.label"
          placeholder="请输入字典标签"
          clearable
          size="small"
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

    <el-table v-loading="loading" :data="dataList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="编号" align="center" prop="id" width="55"/>
      <el-table-column label="标签" align="center" prop="dict_label" :show-overflow-tooltip="true"/>
      <el-table-column label="值" align="center" prop="dict_value" :show-overflow-tooltip="true"/>
      <el-table-column label="默认" align="center" prop="is_default">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.is_default" disabled></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="状态" align="center" prop="status" :formatter="statusFormat" />
      <el-table-column label="备注" align="center" prop="remark" :show-overflow-tooltip="true"/>
<!--      <el-table-column v-if="defaultDictType != ''" label="字典名称" align="center" :show-overflow-tooltip="true">-->
<!--        <template slot-scope="scope">-->
<!--          <span>{{ defaultDictType }}</span>-->
<!--        </template>-->
<!--      </el-table-column>-->
      <el-table-column label="排序" align="center" prop="order_num" width="55"/>
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
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="24">
            <el-form-item label="归属字典" v-if="typeof form.dict_type != 'undefined'">
              <label>{{ form.dict_type + ' ( ' + form.dict_name + ' )' }}</label>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="数据标签" prop="dict_label">
              <el-input v-model="form.dict_label" placeholder="请输入数据标签" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="17">
            <el-form-item label="数据值" prop="dict_value">
              <el-input v-model="form.dict_value" placeholder="请输入数据标签" />
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item label="默认" prop="is_default">
              <el-switch v-model="form.is_default"></el-switch>
            </el-form-item>
          </el-col>
        </el-row>
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
        <el-row>
          <el-col :span="24">
            <el-form-item label="备注" prop="remark">
              <el-input v-model="form.remark" type="textarea" placeholder="请输入内容" />
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

import { listDetail, addDetail, getDetail, setDetail, delDetail, getDetailMaxOrderNum} from '@/api/system/dict/detail'
import {getDictData, getDicts} from "@/api/system/dict/data";


export default {
  name: 'DictData',
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
      dataList: [],
      // 默认字典类型
      defaultDictData: '',
      statusOptions: [],
      // 弹出层标题
      title: '',
      // 是否显示弹出层
      open: false,
      // 类型数据字典
      typeOptions: [],
      // 查询参数
      queryParams: {
        page: 1,
        limit: 10,
        dict_data_id: undefined,
        label: undefined
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        dict_label: [
          { required: true, message: '数据标签不能为空', trigger: 'blur' }
        ],
        dict_value: [
          { required: true, message: '数据值不能为空', trigger: 'blur' }
        ],
        order_num: [
          { required: true, message: '数据顺序不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    const dictId = this.$route.params && this.$route.params.id
    this.getType(dictId)
    getDicts("com_default_status").then(response => {
      this.statusOptions = response.data.details;
    })
  },
  methods: {
    /** 查询字典类型详细 */
    getType(dictId) {
      getDictData(dictId).then(response => {
        this.queryParams.dict_data_id = response.data.id
        this.typeOptions = [response.data]
        this.defaultDictData = response.data.dict_type
        this.defaultDictDataId = response.data.id
        this.getList()
      })
    },
    /** 查询字典数据列表 */
    getList() {
      this.loading = true
      listDetail(this.queryParams).then(response => {
        this.dataList = response.data.data
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
        label: undefined,
        order: 0,
        remark: undefined
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
        limit: 10,
        type_id: this.defaultDictDataId,
        label: undefined
      }
      this.handleQuery()
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset()
      this.open = true
      this.title = '添加字典数据'
      this.form.type_id = this.queryParams.dict_data_id
      getDetailMaxOrderNum(this.defaultDictDataId).then(response => {
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
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset()
      const id = row.id || this.ids
      getDetail(id).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改字典数据'
      })
    },
    /** 提交按钮 */
    submitForm: function() {
      this.$refs['form'].validate(valid => {
        if (valid) {
          this.form.dict_data_id = this.defaultDictDataId
          if (this.form.id !== undefined) {
            setDetail(this.form.id, this.form).then(response => {
              if (response.code === 0) {
                this.msgSuccess("修改成功")
                this.open = false
                this.getList()
              }
            })
          } else {
            addDetail(this.form).then(response => {
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
      const ids = row.id || this.ids
      this.$confirm('是否确认删除字典ID为"' + ids + '"的数据项?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function() {
        return delDetail(ids)
      }).then(() => {
        this.getList()
        this.msgSuccess('删除成功')
      }).catch(function() {
      })
    }
  }
}
</script>

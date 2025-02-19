import request from '@/utils/request'

// 查询角色列表
export function listRole(query) {
  return request({
    url: '/permission/role',
    method: 'get',
    params: query
  })
}


// 获取最大排序
export function getRoleMaxOrderNum() {
  return request({
    url: "/permission/role/max-order-num",
    method: "get"
  })
}

// 查询角色详细
export function getRole(roleId) {
  return request({
    url: '/permission/role/' + roleId,
    method: 'get'
  })
}

// 新增角色
export function addRole(data) {
  return request({
    url: '/permission/role',
    method: 'post',
    data: data
  })
}

// 修改角色
export function setRole(roleId, data) {
  return request({
    url: '/permission/role/' + roleId,
    method: 'put',
    data: data
  })
}


// 修改角色菜单
export function setRoleMenus(roleId, menus) {
  console.log(menus)
  return request({
    url: "/permission/role/" + roleId + "/menu",
    method: "put",
    data: {menu_ids: menus}
  })
}


// 删除角色
export function delRole(roleId) {
  return request({
    url: '/permission/role/' + roleId,
    method: 'delete'
  })
}


// 获取角色选择列表
export function getRoleSelectList() {
  return request({
    url: "/permission/role/select/list",
    method: "get"
  })
}

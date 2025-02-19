import request from '@/utils/request'

// 查询菜单列表
export function listMenu(query) {
  return request({
    url: '/permission/menu',
    method: 'get',
    params: query
  })
}

// 查询菜单详细
export function getMenu(id) {
  return request({
    url: '/permission/menu/' + id,
    method: 'get'
  })
}

// 查询菜单下拉树结构
export function treeselect() {
  return request({
    url: '/permission/menu/simple/tree',
    method: 'get'
  })
}

// 查询菜单下列表结构
export function listselect() {
  return request({
    url: '/permission/menu/simple/list',
    method: 'get'
  })
}


// 新增菜单
export function addMenu(data) {
  return request({
    url: '/permission/menu/',
    method: 'post',
    data: data
  })
}

// 修改菜单
export function updateMenu(id, data) {
  return request({
    url: '/permission/menu/' + id,
    method: 'put',
    data: data
  })
}

// 删除菜单
export function delMenu(id) {
  return request({
    url: '/permission/menu/' + id,
    method: 'delete'
  })
}

// 获取最排序
export function getMaxOrderNum(parent_id) {
  return request({
    url: "/permission/menu/" + parent_id + "/max-order-num",
    method: 'get'
  })
}

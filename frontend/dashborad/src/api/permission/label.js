import request from '@/utils/request'

// 查询b权限标签列表
export function listPermLabel(query) {
  return request({
    url: '/permission/perm-label',
    method: 'get',
    params: query
  })
}


// 查询权限标签详细
export function getPermLabel(labelId) {
  return request({
    url: '/permission/perm-label/' + labelId,
    method: 'get'
  })
}

// 新增权限标签
export function addPermLabel(data) {
  console.log(data)
  return request({
    url: '/permission/perm-label',
    method: 'post',
    data: data
  })
}

// 修改权限标签
export function setPermLabel(labelId, data) {
  return request({
    url: '/permission/perm-label/' + labelId,
    method: 'put',
    data: data
  })
}

// 删除权限标签
export function delPermLabel(labelId) {
  return request({
    url: '/permission/perm-label/' + labelId,
    method: 'delete'
  })
}



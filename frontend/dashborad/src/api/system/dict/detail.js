import request from '@/utils/request'


// 查询字典数据列表
export function listDetail(query) {
  return request({
    url: '/system/dict/detail',
    method: 'get',
    params: query
  })
}

// 查询字典数据详细
export function getDetail(id) {
  return request({
    url: '/system/dict/detail/' + id,
    method: 'get'
  })
}

// 根据字典类型查询字典数据信息 用于user获取字典
export function getDicts(dictType) {
  return request({
    url: '/system/dict/data/type_code/' + dictType,
    method: 'get'
  })
}

// 新增字典数据
export function addDetail(data) {
  return request({
    url: '/system/dict/detail',
    method: 'post',
    data: data
  })
}

// 修改字典数据
export function setDetail(id, data) {
  return request({
    url: '/system/dict/detail/' + id,
    method: 'put',
    data: data
  })
}

// 删除字典数据
export function delDetail(id) {
  return request({
    url: '/system/dict/detail/' + id,
    method: 'delete'
  })
}


export function getDetailMaxOrderNum(dictDataID) {
  return request({
    url: "/system/dict/detail/max-order-num/" + dictDataID,
    method: "get"
  })
}

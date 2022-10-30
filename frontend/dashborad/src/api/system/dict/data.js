import request from '@/utils/request'

// 获取字典
export function getDicts(type) {
  return request({
    url: "/system/dict/type/" + type,
    method: 'get'
  })
}


// 查询字典类型列表
export function listDictData(query) {
  return request({
    url: '/system/dict/data',
    method: 'get',
    params: query
  })
}

// 查询字典类型详细
export function getDictData(id) {
  return request({
    url: '/system/dict/data/' + id,
    method: 'get'
  })
}

// 新增字典类型
export function addDictData(data) {
  return request({
    url: '/system/dict/data',
    method: 'post',
    data: data
  })
}

// 修改字典类型
export function setDictData(id, data) {
  return request({
    url: '/system/dict/data/' + id,
    method: 'put',
    data: data
  })
}

// 删除字典类型
export function delDictData(id) {
  return request({
    url: '/system/dict/data/' + id,
    method: 'delete'
  })
}


export function getDictDataMaxOrderNum(){
  return request({
    url: "/system/dict/data/max-order-num",
    method: "get"
  })
}

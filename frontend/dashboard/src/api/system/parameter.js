import request from '@/utils/request'

// 获取参数
export function getParameter(key) {
  return request({
    url: "/system/config-setting/key/" + key,
    method: 'get'
  })
}


// 查询参数列表
export function listConfigSettings(query) {
  return request({
    url: '/system/config-setting',
    method: 'get',
    params: query
  })
}


// 获取参数
export function getConfigSetting(id) {
  return request({
    url: "/system/config-setting/" + id,
    method: "get"
  })
}


// 获取最大排序
export function getConfigSettingMaxOrderNum(){
  return request({
    url: "/system/config-setting/max-order-num",
    method: "get"
  })
}


// 添加参数
export function addConfigSetting(data){
  return request({
    url: "/system/config-setting",
    method: "post",
    data: data
  })
}


// 更新参数
export function setConfigSetting(id, data) {
  return request({
    url: "/system/config-setting/" + id,
    method: "put",
    data: data
  })
}


// 删除参数
export function delConfigSetting(id) {
  return request({
    url: "/system/config-setting/" + id,
    method: 'delete'
  })

}

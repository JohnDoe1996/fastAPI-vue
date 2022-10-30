import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data: data
  })
}

export function getInfo() {
  return request({
    url: '/user/info',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}


export function register(data) {
  return request({
    url: '/user/register',
    method: 'post',
    data: data
  })
}


export function verifyRegister(code) {
  return request({
    url: '/user/register/' + code,
    method: 'get'
  })
}

export function confirmRegister(code) {
  return request({
    url: '/user/register/' + code,
    method: 'put'
  })
}


export function forgetPassword(data) {
  return request({
    url: '/user/forget-password',
    method: 'post',
    data: data
  })
}


export function verifyForgetPwd(code) {
  return request({
    url: '/user/forget-password/' + code,
    method: 'get'
  })
}

export function confirmForgetPwd(code, data) {
  return request({
    url: '/user/forget-password/' + code,
    method: 'put',
    data: data
  })
}


export function getRouters(){
  return request({
    url: "/user/routers",
    method: "get"
  })
}


export function changeAvatar(data){
  return request({
    url: "/user/avatar",
    method: 'post',
    data: data
  })
}


export function changeInfo(data){
  return request({
    url: "/user/info",
    method: 'put',
    data: data
  })
}


export function changePwd(data) {
  return request({
    url: "/user/password",
    method: 'put',
    data: data
  })
}


export function getCaptchaCode() {
  return request({
    url: "/user/captcha-code",
    method: "get"
  })
}

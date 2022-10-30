/* eslint-disable */
import {asyncRoutes, constantRoutes} from '@/router'
import store from '@/store'
import Layout from '@/layout'
import {handleTree} from "@/utils/ruoyi";

/**
 * Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */
function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role))
  } else {
    return true
  }
}

/**
 * 后台查询的菜单数据拼装成路由格式的数据
 * @param routes
 */
export function generate_menu(data) {
  let routes = []
  data.forEach(item => {
    const menu = item
    menu.component = item.component == '' ? Layout : loadView(item.component)
    if (item.children) {
      menu.children = item.children === undefined ? [] : generate_menu(item.children)
    }
    routes.push(menu)
  })
  return routes
}

// import预编译比require快，但是import不支持变量，只能用require的形式，否则还要前端配置路由表
export const loadView = (view) => { // 路由懒加载
  return (resolve) => require([`@/views${view}`], resolve)
}

/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 */
export function filterAsyncRoutes(routes) {
  const res = []
  routes.forEach(route => {
    const tmp = {...route}
    if (tmp.children) {
      tmp.children = filterAsyncRoutes(tmp.children)
    }
    res.push(tmp)
  })

  return res
}

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes({commit}, roles) {
    return new Promise(resolve => {
      store.dispatch('user/getAuthMenu').then((data) => {
        let menus = handleTree(data.menus, 'id')
        let generateRoutes = [...generate_menu(menus), ...asyncRoutes]
        let accessedRoutes = filterAsyncRoutes(generateRoutes)
        commit('SET_ROUTES', accessedRoutes)
        resolve(accessedRoutes)
      })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
**/
const Layout = () => import('@/views/layout/Layout')
const Login = () => import('@/views/login/index')
const Page = () => import('@/views/404')

/* account */
const Dashboard = () => import('@/views/dashboard/dashboard')
const UserList = () => import('@/views/account/UserList')
const GroupList = () => import('@/views/account/GroupList')
const GroupPermissionList = () => import('@/views/account/GroupPermissionList')

/* cmdb */
const Idc = () => import('@/views/cmdb/idc/index')
const Server = () => import('@/views/cmdb/server/index')
const Service = () => import('@/views/cmdb/service/index')

/* task */
const Task = () => import('@/views/tasks/tasks')
const historyTask = () => import('@/views/tasks/history')
const crontabs = () => import('@/views/tasks/crontabs')

export const constantRouterMap = [
  {
    path: '/login',
    component: Login,
    hidden: true
  },
  {
    path: '/404',
    component: Page,
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    icon: 'dashboard',
    children: [{
      path: '',
      component: Dashboard,
      name: 'Dashboard',
      meta: { title: 'Dashboard', icon: 'dashboard', noCache: true }
    }]
  },
  {
    path: '/users',
    component: Layout,
    redirect: '/users/list',
    name: '用户管理',
    meta: {
      title: '用户管理',
      icon: 'user'
    },
    children: [
      {
        path: 'list',
        component: UserList,
        name: '用户列表',
        meta: { title: '用户列表', icon: 'user' }
      },
      {
        path: 'group',
        component: GroupList,
        name: '角色',
        meta: { title: '角色', icon: 'user' }
      },
      {
        path: 'group/groupPermission',
        component: GroupPermissionList,
        name: '权限列表',
        meta: { title: '权限列表', icon: 'user' },
        hidden: true
      }
    ]
  },
  {
    path: '/assets',
    component: Layout,
    redirect: '/assets/list',
    name: '资产管理',
    meta: { title: '资产管理', icon: 'documentation' },
    children: [
      {
        path: 'idc',
        name: '云厂商',
        component: Idc,
        meta: { title: '云厂商', icon: 'list' }
      },
      {
        path: 'server',
        name: '服务器',
        component: Server,
        meta: { title: '服务器', icon: 'list' }
      },
      {
        path: 'service',
        name: '业务线',
        component: Service,
        meta: { title: '业务线', icon: 'list' }
      }
    ]
  },
  {
    path: '/tasks',
    component: Layout,
    redirect: '/tasks/list',
    name: '任务管理',
    meta: { title: '任务管理', icon: 'documentation' },
    children: [
      {
        path: 'list',
        name: '任务列表',
        component: Task,
        meta: { title: '任务列表', icon: 'list' }
      },
      {
        path: 'contabs',
        name: 'crontab表达式',
        component: crontabs,
        meta: { title: 'crontab表达式', icon: 'list' }
      },
      {
        path: 'history',
        name: '历史任务',
        component: historyTask,
        meta: { title: '历史任务', icon: 'list' }
      }
    ]
  },

  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})


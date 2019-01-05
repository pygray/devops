import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import Login from '../views/login/'
import Layout from '../views/layout/Layout'
const Dashboard = () => import('@/views/dashboard/dashboard')
const UserList = () => import('@/views/account/UserList')
const GroupList = () => import('@/views/account/GroupList')
const GroupPermissionList = () => import('@/views/account/GroupPermissionList')

/* cmdb */
const Idc = () => import('@/views/cmdb/idc/index')
const Server = () => import('@/views/cmdb/server/index')
const Service = () => import('@/views/cmdb/service/index')

/* task */
const Task = () => import('@/views/tasks/cronTask/tasks')
const historyTask = () => import('@/views/tasks/cronTask/history')
const Crontab = () => import('@/views/tasks/cronTask/crontabs')

/* batch tasks */
const batchTaskApply = () => import('@/views/tasks/batchTask/add/index')
const batchTaskList = () => import('@/views/tasks/batchTask/list/index')

/**
 * hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
 *                                if not set alwaysShow, only more than one route under the children
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
 **/

// 使用了vue-routerd的[Lazy Loading Routes]

export const constantRouterMap = [
  { path: '/login', component: Login, hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },
  {
    path: '/',
    component: Layout,
    icon: 'dashboard',
    children: [{
      path: '',
      name: 'Dashboard',
      component: Dashboard,
      meta: { title: 'Dashboard', icon: 'dashboard', noCache: true }
    }]
  }
]

/* 异步挂载的路由
 动态需要根据权限加载的路由表
*/
export const asyncRouterMap = [
  {
    path: '/users',
    component: Layout,
    name: '用户管理',
    meta: { title: '用户管理', icon: 'user', roles: ['account.view_user'] }, // 页面需要的权限
    children: [
      {
        path: 'list',
        component: UserList,
        name: '用户列表',
        meta: { title: '用户列表', icon: 'user', roles: ['account.view_user'] } // 页面需要的权限
      },
      {
        path: 'group',
        component: GroupList,
        name: '角色',
        meta: { title: '角色', icon: 'user', roles: ['auth.add_group'] }
      },
      {
        path: 'group/groupPermission',
        component: GroupPermissionList,
        name: '权限列表',
        meta: { title: '权限列表', icon: 'user', roles: ['auth.add_permission'] },
        hidden: true
      }
    ]
  },
  {
    path: '/assets',
    component: Layout,
    // redirect: '/assets/list',
    name: '资产管理',
    meta: { title: '资产管理', icon: 'documentation', roles: ['cmdb.view_idc'] },
    children: [
      {
        path: 'idc',
        name: '云厂商',
        component: Idc,
        meta: { title: '云厂商', icon: 'list', roles: ['cmdb.view_idc'] }
      },
      {
        path: 'server',
        name: '服务器',
        component: Server,
        meta: { title: '服务器', icon: 'list', roles: ['cmdb.view_server'] }
      },
      {
        path: 'service',
        name: '业务线',
        component: Service,
        meta: { title: '业务线', icon: 'list', roles: ['cmdb.view_product'] }
      }
    ]
  },
  {
    path: '/tasks',
    component: Layout,
    // redirect: '/tasks/list',
    name: '定时任务',
    meta: { title: '定时任务', icon: 'documentation', roles: ['tasks.view_task_profile'] },
    children: [
      {
        path: 'list',
        name: '任务列表',
        component: Task,
        meta: { title: '任务列表', icon: 'list', roles: ['tasks.view_task_profile'] }
      },
      {
        path: 'contabs',
        name: 'crontab',
        component: Crontab,
        meta: { title: 'crontab', icon: 'list', roles: ['django_celery_beat.add_crontabschedule'] }
      },
      {
        path: 'history',
        name: '历史任务',
        component: historyTask,
        meta: { title: '历史任务', icon: 'list', roles: ['tasks.view_task_profile'] }
      }
    ]
  },
  {
    path: '/batch_task',
    component: Layout,
    redirect: '/batch_task/list',
    name: '批量任务',
    meta: { title: '批量任务', icon: 'documentation', roles: ['tasks.view_batchTask'] },
    children: [
      {
        path: 'apply',
        name: '申请任务',
        component: batchTaskApply,
        meta: { title: '申请任务', icon: 'list', roles: ['tasks.view_batchTask'] }
      },
      {
        path: 'list',
        name: '任务列表',
        component: batchTaskList,
        meta: { title: '任务列表', icon: 'list', roles: ['tasks.view_batchTask'] }
      }
    ]
  },
  { path: '*', redirect: '/404', hidden: true }
]

// 实例化vue的时候只挂载constantRouter
export default new Router({
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})

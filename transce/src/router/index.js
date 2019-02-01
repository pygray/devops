import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import Login from '../views/login/'
import Layout from '../views/layout/Layout'
const Dashboard = () => import('@/views/dashboard/dashboard')
const UserList = () => import('@/views/account/user/index')
const GroupList = () => import('@/views/account/group/index')

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

/* release */
const releaseApply = () => import('@/views/release/apply/index')
const releaseList = () => import('@/views/release/list/index')
const releaseHistory = () => import('@/views/release/history/index')

/* sql 作业平台 */
const sqlDbList = () => import('@/views/sqlmng/dbs/index')
const checkSql = () => import('@/views/sqlmng/check/index')
const personalSettings = () => import('@/views/sqlmng/settings/personalSettings')
const dbCluster = () => import('@/views/sqlmng/dbs/cluster')
const platformSettings = () => import('@/views/sqlmng/settings/platformSettings')
const inceptionList = () => import('@/views/sqlmng/inception/inceptionList')
const inceptionDetail = () => import('@/views/sqlmng/inception/inceptionDetail')
const inceptionSettings = () => import('@/views/sqlmng/settings/inceptionSettings')
const optimizeSQL = () => import('@/views/sqlmng/optimize/optimize')

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
    redirect: '/dashboard',
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
      }
      // {
      //   path: 'group/groupPermission',
      //   component: GroupPermissionList,
      //   name: '权限列表',
      //   meta: { title: '权限列表', icon: 'user', roles: ['auth.add_permission'] },
      //   hidden: true
      // }
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
  {
    path: '/deploy',
    component: Layout,
    redirect: '/deploy/apply',
    name: '代码上线',
    meta: { title: '代码上线', icon: 'documentation', roles: ['release.view_deploy'] },
    children: [
      {
        path: 'apply',
        name: '申请上线',
        component: releaseApply,
        meta: { title: '申请上线', icon: 'list', roles: ['release.add_deploy'] }
      },
      {
        path: 'list',
        name: '申请列表',
        component: releaseList,
        meta: { title: '申请列表', icon: 'list', roles: ['release.change_deploy'] }
      },
      {
        path: 'history',
        name: '上线列表',
        component: releaseHistory,
        meta: { title: '上线列表', icon: 'list', roles: ['release.view_deploy'] }
      }
    ]
  },
  {
    path: '/sql_check',
    component: Layout,
    // redirect: '/deploy/apply',
    name: 'sql作业',
    meta: { title: 'SQL作业', icon: 'documentation', roles: [''] },
    children: [
      {
        path: 'sql_check',
        name: 'SQL审核',
        component: checkSql,
        meta: { title: 'SQL审核', icon: 'list', roles: [''] }
      },
      {
        path: 'inception_list',
        name: 'SQL处理',
        component: inceptionList,
        meta: { title: 'SQL处理', icon: 'list', roles: [''] }
      },
      {
        path: 'optimizeSQL',
        name: 'SQL优化',
        component: optimizeSQL,
        meta: { title: 'SQL优化', icon: 'list', roles: [''] }
      },
      {
        path: 'inceptionsql/:id',
        name: 'SQL详情',
        component: inceptionDetail,
        hidden: true,
        meta: { title: 'SQL详情', icon: 'list', roles: [''] }
      },
    ]
  },
  {
    path: '/db_cluster',
    component: Layout,
    // redirect: '/deploy/apply',
    name: '数据库配置',
    meta: { title: '数据库配置', icon: 'documentation', roles: [''] },
    children: [
      {
        path: 'db_cluster',
        name: '集群',
        component: dbCluster,
        meta: { title: '集群', icon: 'list', roles: [''] }
      },
      {
        path: 'dblist',
        name: '数据库',
        component: sqlDbList,
        meta: { title: '数据库', icon: 'list', roles: [''] }
      }
    ]
  },
  {
    path: '/personal_settings',
    component: Layout,
    // redirect: '/deploy/apply',
    name: 'SQL平台设置',
    meta: { title: 'SQL平台设置', icon: 'documentation', roles: [''] },
    children: [
      {
        path: 'personal_settings',
        name: '订阅设置',
        component: personalSettings,
        meta: { title: '订阅设置', icon: 'list', roles: [''] }
      },
      {
        path: 'inception_settings',
        name: 'inception设置',
        component: inceptionSettings,
        meta: { title: 'inception设置', icon: 'list', roles: [''] }
      },
      {
        path: 'platform_settings',
        name: '流程设置',
        component: platformSettings,
        meta: { title: '流程设置', icon: 'list', roles: [''] }
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

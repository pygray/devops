import request from '@/utils/request'

// 任务列表
export function getTaskList(params) {
  return request({
    url: '/tasks/',
    method: 'get',
    params
  })
}

// 修改任务
export function updateTask(id, data) {
  return request({
    url: '/tasks/' + id + '/',
    method: 'put',
    data
  })
}

// 添加任务
export function createTask(data) {
  return request({
    url: '/tasks/',
    method: 'post',
    data
  })
}

// 删除任务
export function deleteTask(id) {
  return request({
    url: '/tasks/' + id + '/',
    method: 'delete'
  })
}

// 任务模板列表
export function taskMbList(params) {
  return request({
    url: '/sys_task_list/',
    method: 'get',
    params
  })
}

// crontab 表达式列表
export function crontabList(params) {
  return request({
    url: '/crontabs/',
    method: 'get',
    params
  })
}

// 删除crontab 表达式
export function deleteCrontabs(id) {
  return request({
    url: '/crontabs/' + id + '/',
    method: 'delete'
  })
}

// 创建crontab 表达式
export function createCrontabs(data) {
  return request({
    url: '/crontabs/',
    method: 'post',
    data
  })
}

// 修改crontab表达式
export function updateCrontabs(id, data) {
  return request({
    url: '/crontabs/' + id + '/',
    method: 'put',
    data
  })
}

// 任务结果列表
export function taskResultList(params) {
  return request({
    url: '/task_result/',
    method: 'get',
    params
  })
}

// 删除任务结果
export function deleteTaskResult(id) {
  return request({
    url: '/task_result/' + id + '/',
    method: 'delete'
  })
}

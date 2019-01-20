import request from '@/utils/request'

// 获取当前用户项目列表
export function getProjectList() {
  return request({
    url: '/projects/',
    method: 'get'
  })
}

// 获取单个项目
export function getOneProject(id) {
  return request({
    url: '/projects/' + id + '/',
    method: 'get'
  })
}

// 获取当前项目tag列表
export function getProjectTag(id) {
  return request({
    url: '/tags/' + id + '/',
    method: 'get'
  })
}

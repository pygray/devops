import request from '@/utils/request'

// 获取发布列表
export function getDeployList(params) {
  return request({
    url: '/deploy/',
    method: 'get',
    params
  })
}

// 创建发布工单
export function createDeploy(data) {
  return request({
    url: '/deploy/',
    method: 'post',
    data
  })
}

// 修改发布工单
export function updateDeploy(id, data) {
  return request({
    url: '/deploy/' + id + '/',
    // method: 'put',
    method: 'patch',
    data
  })
}

// 删除发布工单
export function deleteDeploy(id) {
  return request({
    url: '/deploy/' + id + '/',
    method: 'delete'
  })
}

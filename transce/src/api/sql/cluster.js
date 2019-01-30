import request from '@/utils/request'

export function GetDbList(params) {
  return request({
    url: '/dbconfs/',
    method: 'get',
    params
  })
}

export function GetClusterList(params) {
  return request({
    url: '/dbcluster/',
    method: 'get',
    params
  })
}

export function UpdateCluster(id, data) {
  return request({
    url: '/dbcluster/' + id + '/',
    method: 'put',
    data: data
  })
}

export function CreateCluster(data) {
  return request({
    url: '/dbcluster/',
    method: 'post',
    data: data
  })
}

export function DeleteCluster(id) {
  return request({
    url: '/dbcluster/' + id + '/',
    method: 'delete'
  })
}

import request from '@/utils/request'

export function GetFWList(params) {
  return request({
    url: '/forbiddenwords/',
    method: 'get',
    params
  })
}

export function UpdateFW(id, data) {
  return request({
    url: '/forbiddenwords/' + id + '/',
    method: 'put',
    data: data
  })
}

export function CreateFW(data) {
  return request({
    url: '/forbiddenwords/',
    method: 'post',
    data: data
  })
}

import request from '@/utils/request'

export function GetMailActions(params) {
  return request({
    url: '/mailactions/',
    method: 'get',
    params
  })
}

export function SetMailActions(data) {
  return request({
    url: '/mailactions/',
    method: 'post',
    data: data
  })
}

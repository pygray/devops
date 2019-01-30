import request from '@/utils/request'

export function GetSqlList(params) {
  return request({
    url: '/inceptions/',
    method: 'get',
    params
  })
}

export function GetSqlDetail(id) {
  return request({
    url: '/inceptions/' + id,
    method: 'get'
  })
}

export function SqlAction(id, action) {
  return request({
    url: '/inceptions/' + id + '/' + action,
    method: 'get'
  })
}

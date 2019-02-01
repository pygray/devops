import request from '@/utils/request'

export function GetDbList(params) {
  return request({
    url: '/dbconfs/',
    method: 'get',
    params
  })
}

export function UpdateDb(id, data) {
  return request({
    url: '/dbconfs/' + id + '/',
    method: 'put',
    data: data
  })
}

export function CreateDb(data) {
  return request({
    url: '/dbconfs/',
    method: 'post',
    data: data
  })
}

export function DeleteDb(id) {
  return request({
    url: '/dbconfs/' + id + '/',
    method: 'delete'
  })
}

export function CheckConn(data) {
  return request({
    url: '/inception/conncheck/',
    method: 'post',
    data: data
  })
}

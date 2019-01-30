import request from '@/utils/request'

export function GetInceptionVariables(params) {
  return request({
    url: '/inception/variables/',
    method: 'get',
    params
  })
}

export function SetInceptionVariables(data) {
  return request({
    url: '/inception/variables/',
    method: 'post',
    data: data
  })
}

export function CheckConn(data) {
  return request({
    url: '/inception/connection/',
    method: 'post',
    data: data
  })
}

export function GetInceptionBackup(params) {
  return request({
    url: '/inception/backup/',
    method: 'get',
    params
  })
}

export function GetInceptionConnection(params) {
  return request({
    url: '/inception/conncheck/',
    method: 'get',
    params
  })
}

export function UpdateInceptionConnection(id, data) {
  return request({
    url: '/inception/connection/' + id + '/',
    method: 'put',
    data: data
  })
}

export function CreateInceptionConnection(data) {
  return request({
    url: '/inception/connection/',
    method: 'post',
    data: data
  })
}

import request from '@/utils/request'

const strategy = '/strategy/'

export function GetStrategyList(params) {
  return request({
    url: strategy,
    method: 'get',
    params
  })
}

export function UpdateStrategy(id, data) {
  return request({
    url: strategy + id + '/',
    method: 'put',
    data: data
  })
}

export function CreateStrategy(data) {
  return request({
    url: strategy,
    method: 'post',
    data: data
  })
}

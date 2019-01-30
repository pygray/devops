import request from '@/utils/request'
const sqlsettings = '/sqlsettings/'

export function GetFWList(params) {
  return request({
    url: sqlsettings,
    method: 'get',
    params
  })
}

export function UpdateFW(id, data) {
  return request({
    url: sqlsettings + id + '/',
    method: 'put',
    data: data
  })
}

export function CreateFW(data) {
  return request({
    url: sqlsettings,
    method: 'post',
    data: data
  })
}

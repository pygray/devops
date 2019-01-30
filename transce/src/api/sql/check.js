import request from '@/utils/request'

// 根据用户身份返回check sql时需要的执行人
export function GetSelectData(data) {
  return request({
    url: '/autoselects/',
    method: 'post',
    data: data
  })
}

// SQL语法审核
export function CheckSql(data) {
  return request({
    url: '/inceptioncheck/',
    method: 'post',
    data: data
  })
}

// 获取审核工单的用户个性化设置
export function GetPersonalSettings(params) {
  return request({
    url: '/personalsettings/',
    method: 'get',
    params
  })
}

// 更新审核工单的用户个性化设置
export function CreatePersonalSettings(data) {
  return request({
    url: '/personalsettings/',
    method: 'post',
    data: data
  })
}

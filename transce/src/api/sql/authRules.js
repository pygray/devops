import request from '@/utils/request'

// 获取平台权限
export function GetAuthRules(params) {
  return request({
    url: '/authrules/',
    method: 'get',
    params
  })
}

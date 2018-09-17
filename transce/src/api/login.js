import request from '@/utils/request'

export function login(username, password) {
  return request({
    url: '/api-jwt/',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

export function getInfo() {
  return request({
    url: '/userinfo/',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/api-auth/logout/',
    method: 'post'
  })
}

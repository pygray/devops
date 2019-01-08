import request from '@/utils/request'

// 获取用户列表
export function getUserList(params) {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

// 创建用户
export function createUser(data) {
  return request({
    url: '/users/',
    method: 'post',
    data
  })
}

// 修改用户
export function updateUser(id, data) {
  return request({
    url: '/users/' + id + '/',
    method: 'put',
    data
  })
}

// 删除用户
export function deleteUser(id) {
  return request({
    url: '/users/' + id + '/',
    method: 'delete'
  })
}

// 将用户加入组中
export function updateUserGroup(id, data) {
  return request({
    url: '/usergroup/' + id + '/',
    method: 'put',
    data
  })
}

// 获取组列表
export function getGroupList(params) {
  return request({
    url: '/groups/',
    method: 'get',
    params
  })
}

// 获取某个组的成员
export function getOneGroup(id) {
  return request({
    url: '/groups/' + id + '/',
    method: 'get'
  })
}

// 创建组
export function createGroup(data) {
  return request({
    url: '/groups/',
    method: 'post',
    data
  })
}

// 修改组
export function updateGroup(id, data) {
  return request({
    url: '/groups/' + id + '/',
    method: 'put',
    data
  })
}

// 删除组
export function deleteGroup(id) {
  return request({
    url: '/groups/' + id + '/',
    method: 'delete'
  })
}

// 获取权限列表
export function getPermissionList(params) {
  return request({
    url: '/permission/',
    method: 'get',
    params
  })
}

// 修改角色权限
export function updateGroupPower(id, data) {
  return request({
    url: '/grouppower/' + id + '/',
    method: 'put',
    data
  })
}

// 将指定用户从组里面删除
export function deleteGroupMember(gid, data) {
  return request({
    url: '/groupmembers/' + gid + '/',
    method: 'delete',
    data
  })
}


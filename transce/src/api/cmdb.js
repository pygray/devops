import request from '@/utils/request'

// 厂商列表
export function getIdcsList(params) {
  return request({
    url: '/idcs/',
    method: 'get',
    params
  })
}

// 返回指定厂商下项目列表
export function getIdcProductList(id, params) {
  return request({
    url: '/idc_product/' + id + '/',
    method: 'get',
    params
  })
}

// 添加厂商
export function createIdc(data) {
  return request({
    url: '/idcs/',
    method: 'post',
    data
  })
}

// 编辑厂商信息
export function updateIdc(id, data) {
  return request({
    url: '/idcs/' + id + '/',
    method: 'put',
    data
  })
}

// 删除厂商信息
export function deleteIdc(id) {
  return request({
    url: '/idcs/' + id + '/',
    method: 'delete'
  })
}

// 服务器列表
export function getServerList(params) {
  return request({
    url: '/server/',
    method: 'get',
    params
  })
}

// 添加服务器
export function createServer(data) {
  return request({
    url: '/server/',
    method: 'post',
    data
  })
}

// 更新服务器
export function updateServer(id, data) {
  return request({
    url: '/server_update/' + id + '/',
    method: 'put',
    data
  })
}

// 删除服务器
export function deleteServer(id) {
  return request({
    url: '/server/' + id + '/',
    method: 'delete'
  })
}

// 项目列表
export function getProductLevel(params) {
  return request({
    url: '/product/',
    method: 'get',
    params
  })
}

// 创建项目
export function createProduct(data) {
  return request({
    url: '/product/',
    method: 'post',
    data
  })
}

// 指定项目信息
export function getProductLevelInfo(id) {
  return request({
    url: '/product/' + id + '/',
    method: 'get'
  })
}

// 修改项目信息
export function updateProduct(id, params) {
  return request({
    url: '/product/' + id + '/',
    method: 'put',
    data: params
  })
}

// 删除项目
export function deleteProductLevelInfo(id) {
  return request({
    url: '/product/' + id + '/',
    method: 'delete'
  })
}

// 返回项目对应服务
export function getProductServiceList(id, params) {
  return request({
    url: '/product_service/' + id + '/',
    method: 'get',
    params
  })
}

// tree 数据
export function getProductTree(params) {
  return request({
    url: '/service_tree/',
    method: 'get',
    params
  })
}

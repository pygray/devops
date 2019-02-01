import request from '@/utils/request'

export function GetTableList(id) {
  return request({
    url: '/dbconfs/' + id + '/tables/',
    method: 'get'
  })
}

export function GetTableInfo(id, tableName) {
  return request({
    url: '/dbconfs/' + id + '/table_info/?table_name=' + tableName,
    method: 'get'
  })
}

export function GetSqlAdvisor(id, data) {
  return request({
    url: '/dbconfs/' + id + '/sql_advisor/',
    method: 'post',
    data: data
  })
}

export function GetSqlSOAR(id, data) {
  return request({
    url: '/dbconfs/' + id + '/sql_soar/',
    method: 'post',
    data: data
  })
}

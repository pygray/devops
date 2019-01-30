import axios from '../../libs/http'
import request from '@/utils/request'

export function GetTableList(id) {
  return axios.get('/dbconfs/' + id + '/tables/')
}

export function GetTableInfo(id, tableName) {
  return axios.get('/dbconfs/' + id + '/table_info/?table_name=' + tableName)
}

export function GetSqlAdvisor(id, data) {
  return request({
    url: '/dbconfs/' + id + '/sql_advisor/',
    method: 'post',
    data: data
  });
}

export function GetSqlSOAR(id, data) {
  return request({
    url: '/dbconfs/' + id + '/sql_soar/',
    method: 'post',
    data: data
  });
}

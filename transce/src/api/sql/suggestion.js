import request from '@/utils/request'

const suggestion = '/suggestion/'

export function GetSuggestionList(params) {
  return request({
    url: suggestion,
    method: 'get',
    params
  })
}

export function CreateSuggestion(data) {
  return request({
    url: suggestion,
    method: 'post',
    data: data
  })
}

export function DeleteSuggestion(id) {
  return request({
    url: suggestion + id + '/',
    method: 'delete'
  })
}

import axios from 'axios'

export function getIdcList() {
  return axios.get('/api/idcs/')
}

export function createIdc(value) {
  return axios.post('/api/idcs/', value)
}

export function updateIdc(value) {
  return axios.put(`/api/idcs/${value.id}`, value.params)
}

export function deleteIdc(id) {
  return axios.delete(`/api/idcs/${id}/`)
}

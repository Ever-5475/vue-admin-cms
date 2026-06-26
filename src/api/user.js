import request from '@/utils/request'

export function login(data) {
  return request({ url: '/vue-admin-template/user/login', method: 'post', data })
}

export function getInfo(token) {
  return request({ url: '/vue-admin-template/user/info', method: 'get', params: { token } })
}

export function logout() {
  return request({ url: '/vue-admin-template/user/logout', method: 'post' })
}

export function getUserList(params) {
  return request({ url: '/vue-admin-template/user/list', method: 'get', params })
}

export function getUserDetail(id) {
  return request({ url: `/vue-admin-template/user/${id}`, method: 'get' })
}

export function createUser(data) {
  return request({ url: '/vue-admin-template/user/create', method: 'post', data })
}

export function updateUser(id, data) {
  return request({ url: `/vue-admin-template/user/update`, method: 'post', data: { id, ...data } })
}

export function deleteUser(id) {
  return request({ url: '/vue-admin-template/user/delete', method: 'post', data: { id } })
}

export function register(data) {
  return request({ url: '/vue-admin-template/user/register', method: 'post', data })
}

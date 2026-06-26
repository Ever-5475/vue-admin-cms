import request from '@/utils/request'

export function getArticleList(params) {
  return request({ url: '/vue-admin-template/table/list', method: 'get', params })
}

export function getArticleDetail(id) {
  return request({ url: `/vue-admin-template/table/detail?id=${id}`, method: 'get' })
}

export function createArticle(data) {
  return request({ url: '/vue-admin-template/table/create', method: 'post', data })
}

export function updateArticle(id, data) {
  return request({ url: '/vue-admin-template/table/update', method: 'post', data: { id, ...data } })
}

export function deleteArticle(id) {
  return request({ url: '/vue-admin-template/table/delete', method: 'post', data: { id } })
}

// ============ 评论 API ============
export function getCommentsByArticle(params) {
  return request({ url: '/vue-admin-template/comments/by-article', method: 'get', params })
}

export function getCommentList(params) {
  return request({ url: '/vue-admin-template/comments/list', method: 'get', params })
}

export function createComment(data) {
  return request({ url: '/vue-admin-template/comments/create', method: 'post', data })
}

export function updateComment(data) {
  return request({ url: '/vue-admin-template/comments/update', method: 'post', data })
}

export function approveComment(data) {
  return request({ url: '/vue-admin-template/comments/approve', method: 'post', data })
}

export function deleteComment(id) {
  return request({ url: '/vue-admin-template/comments/delete', method: 'post', data: { id } })
}

export function countComment(params) {
  return request({ url: '/vue-admin-template/comments/count', method: 'get', params })
}

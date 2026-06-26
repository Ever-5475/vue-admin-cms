import request from '@/utils/request'

export function getReportOverview() {
  return request({ url: '/vue-admin-template/report/overview', method: 'get' })
}

export function getReportArticle(days = 30) {
  return request({ url: '/vue-admin-template/report/article', method: 'get', params: { days } })
}

export function getReportComment(days = 30) {
  return request({ url: '/vue-admin-template/report/comment', method: 'get', params: { days } })
}

export function getReportActivity(days = 30) {
  return request({ url: '/vue-admin-template/report/activity', method: 'get', params: { days } })
}

import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['X-Token'] = getToken()
    }
    return config
  },
  error => {
    // do something with request error
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data

    // if the custom code is not 20000, it is judged as an error.
    if (res.code !== 20000) {
      Message({
        message: res.message || 'Error',
        type: 'error',
        duration: 5 * 1000
      })

      // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
        // to re-login
        MessageBox.confirm('You have been logged out, you can cancel to stay on this page, or log in again', 'Confirm logout', {
          confirmButtonText: 'Re-Login',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          store.dispatch('user/resetToken').then(() => {
            location.reload()
          })
        })
      }
      return Promise.reject(new Error(res.message || 'Error'))
    } else {
      return res
    }
  },
  error => {
    // 优先读取后端返回的中文 message（兼容 {message: 'xxx'} / {detail: 'xxx'} / 纯文本）
    let msg = error.message
    let rawData = null
    if (error.response && error.response.data) {
      rawData = error.response.data
      if (typeof rawData === 'object') {
        msg = rawData.message || rawData.detail || rawData.msg || rawData.error || msg
      } else if (typeof rawData === 'string') {
        msg = rawData
      }
    }

    // 登录接口由前端登录页自行控制提示（显示在对应输入框下方，与表单校验一致）
    // 其他接口继续用全局 Message 提示
    const url = (error.config && error.config.url) || ''
    const isLoginApi = /\/user\/login$/.test(url)

    if (!isLoginApi) {
      Message({
        message: msg || '请求失败，请稍后再试',
        type: 'error',
        duration: 5 * 1000
      })
    }

    // 把中文 message 透传给 catch 端，便于登录页做精细化提示
    if (msg !== error.message) {
      error.message = msg
    }
    error.userMessage = msg
    return Promise.reject(error)
  }
)

export default service

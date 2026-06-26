/**
 * Created by PanJiaChen on 16/11/18.
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  // 支持任意用户名，只需满足基本要求：
  // 1. 不为空
  // 2. 长度在2-50个字符之间
  // 3. 只包含字母、数字、下划线、中文
  const trimmed = str.trim()
  if (!trimmed || trimmed.length < 2 || trimmed.length > 50) {
    return false
  }
  // 允许字母、数字、下划线、中文、连字符
  const usernameRegex = /^[a-zA-Z0-9_\u4e00-\u9fa5-]+$/
  return usernameRegex.test(trimmed)
}

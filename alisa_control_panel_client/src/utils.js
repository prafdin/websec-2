export const successCodes = [200, 201]
export const apiUrl = process.env.VUE_APP_API_URL

export default function checkLogging () {
  return document.cookie.replace(/(?:(?:^|.*;\s*)csrf_token\s*=\s*([^;]*).*$)|^.*$/, '$1').length > 0
}

export default function checkLogging () {
  return document.cookie.replace(/(?:(?:^|.*;\s*)login-token\s*=\s*([^;]*).*$)|^.*$/, '$1').length > 0
}

export function checkEmail (email: string) {
  const mail = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
  return mail.test(email)
}

export function checkNickname (nickname: string) {
  if ((nickname.length < 2) || (nickname.length > 32)) return false
  // 检查首字符，检查有无非法字符
  if (!/^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]+$/.test(nickname)) {
    return false
  }
  // 若长度大于4，直接许可
  if (nickname.length >= 4) {
    return true
  }
  // 长度小于4，检查其中汉字数量
  const m = nickname.match(/[\u4e00-\u9fa5]/gi)
  if (m && m.length >= 2) return true
}

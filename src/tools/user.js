let store = null

if (process.browser) {
    window.onNuxtReady(({ $store }) => {
        store = $store
    })
}

let _passwordResultToText = function (keyBuffer, saltUint8, iterations) {
    const keyArray = Array.from(new Uint8Array(keyBuffer)) // key as byte array
    const saltArray = Array.from(new Uint8Array(saltUint8)) // salt as byte array

    const iterHex = ('000000' + iterations.toString(16)).slice(-6) // iter’n count as hex
    const iterArray = iterHex.match(/.{2}/g).map(byte => parseInt(byte, 16)) // iter’ns as byte array

    const compositeArray = [].concat(saltArray, iterArray, keyArray) // combined array
    const compositeStr = compositeArray.map(byte => String.fromCharCode(byte)).join('') // combined as string
    const compositeBase64 = btoa('v01' + compositeStr) // encode as base64

    return compositeBase64 // return composite key
}

$.passwordHashAsmCrypto = async function (password, iterations = 1e5) {
    let asmCryptoLoader = () => import(/* webpackChunkName: "hash-polyfill" */ 'asmcrypto.js/dist_es8/pbkdf2/pbkdf2-hmac-sha512.js')
    let asmCrypto = await asmCryptoLoader()
    let salt = store.getters.BACKEND_CONFIG.USER_SECURE_AUTH_FRONTEND_SALT
    let enc = new TextEncoder()
    const pwUtf8 = enc.encode(password) // encode pw as UTF-8
    const saltUint8 = enc.encode(salt)
    let keyBuffer = asmCrypto.Pbkdf2HmacSha512(pwUtf8, saltUint8, iterations, 32)
    return _passwordResultToText(keyBuffer, saltUint8, iterations)
}

$.passwordHashNative = async function (password, iterations = 1e5) {
    let salt = store.getters.BACKEND_CONFIG.USER_SECURE_AUTH_FRONTEND_SALT
    let crypto = window.crypto || window.msCrypto // for IE 11
    let enc = new TextEncoder()
    const pwUtf8 = enc.encode(password) // encode pw as UTF-8
    const pwKey = await crypto.subtle.importKey('raw', pwUtf8, 'PBKDF2', false, ['deriveBits']) // create pw key
    const saltUint8 = enc.encode(salt)

    const params = { name: 'PBKDF2', hash: 'SHA-512', salt: saltUint8, iterations: iterations } // pbkdf2 params
    const keyBuffer = await crypto.subtle.deriveBits(params, pwKey, 256) // derive key
    return _passwordResultToText(keyBuffer, saltUint8, iterations)
}

$.passwordHash = (function () {
    if (process.browser && crypto.subtle && crypto.subtle.importKey) {
        return $.passwordHashNative
    } else {
        return $.passwordHashAsmCrypto
    }
})()

$.checkEmail = function (email) {
    let mail = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
    return mail.test(email)
}

$.checkNickname = function (nickname) {
    if ((nickname < 2) || (nickname > 32)) return false
    // 检查首字符，检查有无非法字符
    if (!/^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]+$/.test(nickname)) {
        return false
    }
    // 若长度大于4，直接许可
    if (nickname.length >= 4) {
        return true
    }
    // 长度小于4，检查其中汉字数量
    let m = nickname.match(/[\u4e00-\u9fa5]/gi)
    if (m && m.length >= 2) return true
}

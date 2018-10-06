import state from '@/state.js'

$.isAdmin = function () {
    return (state.user) && (state.user.group >= state.misc.USER_GROUP.ADMIN)
}

// 获取用户角色（取当前最高的一个）
$.getRole = function (limit) {
    let role = null
    let roles = [null, 'ban', 'inactive_user', 'user', 'superuser', 'admin']
    let rolesMap = {
        [state.misc.USER_GROUP.BAN]: 'ban',
        [state.misc.USER_GROUP.INACTIVE]: 'inactive_user',
        [state.misc.USER_GROUP.NORMAL]: 'user',
        [state.misc.USER_GROUP.SUPERUSER]: 'superuser',
        [state.misc.USER_GROUP.ADMIN]: 'admin'
    }

    if (state.user) {
        role = rolesMap[state.user.group]
    }

    let iCurrent = roles.indexOf(role)
    let iLimit = roles.indexOf(limit)
    if (iLimit === -1) return null
    return roles[(iCurrent > iLimit) ? iLimit : iCurrent]
}

$.passwordHash = async function (password, iterations = 1e5) {
    if (!state.misc.BACKEND_CONFIG.USER_SECURE_AUTH_ENABLE) {
        return password
    }

    let salt = state.misc.BACKEND_CONFIG.USER_SECURE_AUTH_FRONTEND_SALT
    let crypto = window.crypto || window.msCrypto // for IE 11
    let enc = new TextEncoder()
    const pwUtf8 = enc.encode(password) // encode pw as UTF-8
    const pwKey = await crypto.subtle.importKey('raw', pwUtf8, 'PBKDF2', false, ['deriveBits']) // create pw key
    const saltUint8 = enc.encode(salt)

    const params = { name: 'PBKDF2', hash: 'SHA-512', salt: saltUint8, iterations: iterations } // pbkdf2 params
    const keyBuffer = await crypto.subtle.deriveBits(params, pwKey, 256) // derive key

    const keyArray = Array.from(new Uint8Array(keyBuffer)) // key as byte array
    const saltArray = Array.from(new Uint8Array(saltUint8)) // salt as byte array

    const iterHex = ('000000' + iterations.toString(16)).slice(-6) // iter’n count as hex
    const iterArray = iterHex.match(/.{2}/g).map(byte => parseInt(byte, 16)) // iter’ns as byte array

    const compositeArray = [].concat(saltArray, iterArray, keyArray) // combined array
    const compositeStr = compositeArray.map(byte => String.fromCharCode(byte)).join('') // combined as string
    const compositeBase64 = btoa('v01' + compositeStr) // encode as base64

    return compositeBase64 // return composite key
}

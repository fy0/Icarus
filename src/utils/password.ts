// browser only
let store: any = null

if (process.browser) {
  (window as any).onNuxtReady(({ $store }: any) => {
    store = $store
  })
}

let getSalt = () => {
  return store.getters.BACKEND_CONFIG.USER_SECURE_AUTH_FRONTEND_SALT
}

const _passwordResultToText = function (keyBuffer: ArrayBuffer, saltUint8: ArrayBuffer, iterations: number): string {
  const keyArray = Array.from(new Uint8Array(keyBuffer)) // key as byte array
  const saltArray = Array.from(new Uint8Array(saltUint8)) // salt as byte array

  const iterHex = ('000000' + iterations.toString(16)).slice(-6) // iter’n count as hex
  let ret = iterHex.match(/.{2}/g)
  if (!ret) return ''
  const iterArray = ret.map(byte => parseInt(byte, 16)) // iter’ns as byte array

  const compositeArray = (new Array<number>()).concat(saltArray, iterArray, keyArray) // combined array
  const compositeStr = compositeArray.map((byte: number) => String.fromCharCode(byte)).join('') // combined as string
  const compositeBase64 = btoa('v01' + compositeStr) // encode as base64

  return compositeBase64 // return composite key
}

export async function passwordHashAsmCrypto (password: string, iterations = 1e5): Promise<string> {
  const asmCryptoLoader = () => import(/* webpackChunkName: "hash-polyfill" */ 'asmcrypto.js/dist_es8/pbkdf2/pbkdf2-hmac-sha512.js')
  const asmCrypto = await asmCryptoLoader()
  const enc = new TextEncoder()
  const pwUtf8 = enc.encode(password) // encode pw as UTF-8
  const saltUint8 = enc.encode(getSalt())
  const keyBuffer = asmCrypto.Pbkdf2HmacSha512(pwUtf8, saltUint8, iterations, 32)
  return _passwordResultToText(keyBuffer, saltUint8, iterations)
}

export async function passwordHashNative (password: string, iterations = 1e5): Promise<string> {
  const crypto = window.crypto
  const enc = new TextEncoder()
  const pwUtf8 = enc.encode(password) // encode pw as UTF-8
  const pwKey = await crypto.subtle.importKey('raw', pwUtf8, 'PBKDF2', false, ['deriveBits']) // create pw key
  const saltUint8 = enc.encode(getSalt())

  const params = { name: 'PBKDF2', hash: 'SHA-512', salt: saltUint8, iterations: iterations } // pbkdf2 params
  const keyBuffer = await crypto.subtle.deriveBits(params, pwKey, 256) // derive key
  return _passwordResultToText(keyBuffer, saltUint8, iterations)
}

export async function passwordHash (password: string): Promise<string> {
  // process.browser &&
  if (crypto.subtle && crypto.subtle.importKey) {
    return passwordHashNative(password)
  } else {
    return passwordHashAsmCrypto(password)
  }
}

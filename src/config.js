// let hostname = window.location.hostname
const hostname = 'localhost'

const config = {
    remote: {
        API_SERVER: `http://${hostname}:9999`,
        WS_SERVER: `ws://${hostname}:9999/ws`,
        authMode: 'access_token' // access_token / access_token_in_params / cookie
    }
}

try {
    const pri = require('../private.js')
    for (const k of Object.keys(config.remote)) {
        config.remote[k] = pri.default.remote[k] || config.remote[k]
    }
    config.title = pri.default.title || config.title
} catch (e) {}

export default config

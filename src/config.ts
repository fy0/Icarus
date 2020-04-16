import { ConfigInfo } from "./types/config-info"

// let hostname = window.location.hostname
const hostname = 'localhost'

const config: ConfigInfo = {
    remote: {
        API_SERVER: `http://${hostname}:9999`,
        WS_SERVER: `ws://${hostname}:9999/ws`
    }
}

try {
    const pri = require('../private.js')
    for (const k of Object.keys(config.remote)) {
        (config.remote as any)[k] = pri.default.remote[k] || (config.remote as any)[k]
    }
    config.title = pri.default.title || config.title
} catch (e) {}

export default config

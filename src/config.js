
let config = {
    remote: {
        API_SERVER: 'http://localhost:9999',
        WS_SERVER: 'ws://localhost:9999/ws'
    },
    title: 'test'
}

try {
    let pri = require('../private.js')
    config.remote.API_SERVER = pri.default.remote.API_SERVER || config.remote.API_SERVER
    config.title = pri.default.title || config.title
} catch (e) {}

export default config

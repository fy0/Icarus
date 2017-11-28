import ObjectId from 'objectid-js'
import config from './config.js'

let remote = config.remote
// let timeouts = [5000, 7000, 10000, 15000]

class WebsocketConnection {
    constructor () {
        this.socket = null
        this.callback = {}
    }

    async connect (wsurl) {
        return new Promise((resolve, reject) => {
            // Create WebSocket connection.
            let socket = new WebSocket(wsurl)
            this.wsurl = wsurl
            this.socket = socket

            // Connection opened
            socket.addEventListener('open', (ev) => {
                // 连接已建立
                resolve(true)
            })

            // Listen for messages
            socket.addEventListener('message', (ev) => {
                let [rid, data] = JSON.parse(ev.data)
                if (this.callback[rid]) {
                    if (data.code === 1) {
                        this.callback[rid].done(data.data)
                    } else if (this.callback[rid].func) {
                        this.callback[rid].func(data)
                    }
                }
            })

            socket.addEventListener('close', (ev) => {
                // 重连
                this.connect(wsurl)
            })
        })
    }

    async execute (command, data, onProgress) {
        return new Promise((resolve, reject) => {
            let rid = (new ObjectId()).toString()
            this.callback[rid] = {func: onProgress, done: (data) => { resolve(data) }}
            this.socket.send(JSON.stringify([rid, command, data]))
        })
    }
}

let conn = new WebsocketConnection()
conn.connect(remote.WS_SERVER).then(() => {
    console.log('websocket 已连接')
})

export default {
    conn
}

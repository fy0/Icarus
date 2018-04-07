import ObjectId from 'objectid-js'
import config from './config.js'

let remote = config.remote
// let timeouts = [5000, 7000, 10000, 15000]

function getAccessToken () {
    return localStorage.getItem('t')
}

class WebsocketConnection {
    constructor () {
        this.times = 0
        this.socket = null
        this.registered = false
        this.callback = {}
        this.heartbeatTimer = null
    }

    async connect (wsurl) {
        return new Promise((resolve, reject) => {
            // Create WebSocket connection.
            let socket = new WebSocket(wsurl)
            this.wsurl = wsurl
            this.socket = socket

            // Connection opened
            socket.addEventListener('open', async (ev) => {
                // 连接已建立
                this.heartbeatTimer = setInterval(async () => {
                    await this.socket.send('ws.ping')
                }, 25000)

                let count = localStorage.getItem('c')
                if (!count) {
                    count = (new ObjectId()).toString()
                    localStorage.setItem('c', count)
                }
                await this.execute('count', count)

                this.signin()
                resolve(true)
            })

            // Listen for messages
            socket.addEventListener('message', (ev) => {
                if (ev.data === 'ws.pong') return
                let [rid, data] = JSON.parse(ev.data)
                if (this.callback[rid]) {
                    // 虽然 data 可能是任意类型，但不用担心取 .code 会报错
                    if (data.code === 1) { // WS_DONE
                        this.callback[rid].done(data.data)
                    } else if (this.callback[rid].func) {
                        this.callback[rid].func(data)
                    }
                }
            })

            socket.addEventListener('close', (ev) => {
                // 重连
                clearInterval(this.heartbeatTimer)
                if (this.times > 100) return
                this.times++
                this.registered = false
                console.log('websocket 自动重连')
                this.connect(wsurl)
            })
        })
    }

    async signin () {
        // 设置 access token
        let authMode = config.remote.authMode
        if ((authMode === 'access_token') || (authMode === 'access_token_in_params')) {
            let token = getAccessToken()
            let ret = await this.execute('signin', {'access_token': token})
            if (ret === 0) {
                // 登录成功
            }
        }
    }

    async signout () {
        await this.execute('signout')
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

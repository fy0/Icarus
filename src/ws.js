import ObjectId from 'bson-objectid'
import config from './config.js'

const remote = config.remote
let reconnectTimeout = 3000

function getAccessToken () {
  return localStorage.getItem('t')
}

class WebsocketConnection {
  constructor () {
    this.times = 0
    this.socket = null
    this.registered = false
    this.callback = {}
    this.rid_callback = {}
    this.heartbeatTimer = null
  }

  async connect (wsurl) {
    return new Promise((resolve, reject) => {
      // Create WebSocket connection.
      const socket = new WebSocket(wsurl)
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
        const [rid, data] = JSON.parse(ev.data)
        if (this.rid_callback[rid]) {
          // 虽然 data 可能是任意类型，但不用担心取 .code 会报错
          if (data.code === 1) { // WS_DONE
            this.rid_callback[rid].done(data.data)
          } else if (this.rid_callback[rid].func) {
            this.rid_callback[rid].func(data)
          }
        } else if (this.callback[rid]) {
          this.callback[rid](data)
        }
      })

      socket.addEventListener('close', (ev) => {
        // 重连
        clearInterval(this.heartbeatTimer)
        this.registered = false

        setTimeout(() => {
          console.log(`websocket 自动重连，间隔 ${reconnectTimeout}ms`)
          this.connect(wsurl)
        }, reconnectTimeout)

        if (this.times > 30) reconnectTimeout = 30000
        else reconnectTimeout += 1000
        this.times++
      })
    })
  }

  async signin () {
    // 设置 access token
    const authMode = config.remote.authMode
    if ((authMode === 'access_token') || (authMode === 'access_token_in_params')) {
      const token = getAccessToken()
      const ret = await this.execute('signin', { access_token: token })
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
      const rid = (new ObjectId()).toString()
      this.rid_callback[rid] = { func: onProgress, done: (data) => { resolve(data) } }
      this.socket.send(JSON.stringify([rid, command, data]))
    })
  }
}

const conn = new WebsocketConnection()
if (config.ws.enable) {
  conn.connect(remote.WS_SERVER).then(() => {
    console.log('websocket 已连接')
  })
}

export default {
  conn
}

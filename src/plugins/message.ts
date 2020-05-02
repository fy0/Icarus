import { MessageType } from "../types/message-type"
import { retcode, retinfo_cn } from "slim-tools"
import { Context } from "@nuxt/types"

class MessageBoard {
  ctx: Context

  constructor (ctx: Context) {
    this.ctx = ctx
  }

  text (text: string | null, type = MessageType.default, timeout = 3000) {
    let ctx = this.ctx
    const convert = {
      default: '',
      secondary: 'am-alert-secondary',
      success: 'am-alert-success',
      warning: 'am-alert-warning',
      error: 'am-alert-danger'
    }
    const data = { type, text, class: convert[type] }
    if (ctx.store) {
      ctx.store.commit('MESSAGE_PUSH', data)
      if (process.browser) {
        _.delay(() => {
          ctx.store.commit('MESSAGE_REMOVE', data)
        }, timeout)
      }
    }
  }

  secondary (text: string | null, timeout = 3000) {
    this.text(text, MessageType.secondary, timeout) // 灰色白字，很不明显
  }

  success (text: string | null, timeout = 3000) {
    this.text(text, MessageType.success, timeout) // 绿色
  }

  warn (text: string | null, timeout = 3000) {
    this.text(text, MessageType.warning, timeout) // 黄色
  }

  error (text: string | null, timeout = 3000) {
    this.text(text, MessageType.error, timeout) // 红色
  }

  byCode (code: number, data: any = null, text: string | null = null, timeout = 3000) {
    text = text || (retinfo_cn as any)[code]
    if (code === retcode.SUCCESS) this.success(text, timeout)
    else if (code === retcode.TOO_FREQUENT && data) {
      this.error(`${text}，尚需等待 ${data} 秒`, timeout)
    } else this.error(text, timeout)
  }

  byForm (code: number, data: any, alias: any, timeout = 6000) {
    if (code) {
      for (const [k, errs] of Object.entries(data)) {
        for (const err of (errs as Array<string>)) {
          const name = alias[k] || k
          this.byCode(code, data, `${name}：${err}`, timeout)
        }
      }
    } else {
      this.byCode(code, data, null, timeout)
    }
  }
}

declare module 'vue/types/vue' {
  interface Vue {
    $message: MessageBoard
  }
}

declare module 'vuex' {
  interface Store<S> {
    $message: MessageBoard
  }
}

declare module 'vuex-module-decorators' {
  interface VuexModule<S, R> {
    $message: MessageBoard
  }
}

if (process.browser) {
  (window as any).onNuxtReady(async (ctx: any) => {
    // 等浏览器端加载完毕后，延时关闭信息
    const store = ctx.$store
    for (const i of store.state.msgs) {
      _.delay(() => {
        store.commit('MESSAGE_REMOVE', i)
      }, 3000)
    }
  })
}

export default (ctx: Context, inject: any) => {
  inject('message', new MessageBoard(ctx))
}

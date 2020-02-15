
if (process.browser) {
    window.onNuxtReady(async (ctx) => {
        // 等浏览器端加载完毕后，延时关闭信息
        const store = ctx.$store
        for (const i of store.state.msgs) {
            _.delay(() => {
                store.commit('MESSAGE_REMOVE', i)
            }, 3000)
        }
    })
}

function createMessageBoard (ctx) {
    class MessageBoard {
        text (text, type = 'default', timeout = 3000) {
            // type: default, secondary, success, warning, error
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

        secondary (text, timeout = 3000) {
            this.text(text, 'secondary', timeout) // 灰色白字，很不明显
        }

        success (text, timeout = 3000) {
            this.text(text, 'success', timeout) // 绿色
        }

        warn (text, timeout = 3000) {
            this.text(text, 'warning', timeout) // 黄色
        }

        error (text, timeout = 3000) {
            this.text(text, 'error', timeout) // 红色
        }

        byCode (code, data, text = null, timeout = 3000) {
            text = text || ctx.store.state.misc.retinfo_cn[code]
            if (code === ctx.store.state.misc.retcode.SUCCESS) this.success(text, timeout)
            else if (code === ctx.store.state.misc.retcode.TOO_FREQUENT && data) {
                this.error(`${text}，尚需等待 ${data} 秒`, timeout)
            } else this.error(text, timeout)
        }

        byForm (code, data, alias, timeout = 6000) {
            if (code) {
                for (const [k, errs] of Object.entries(data)) {
                    for (const err of errs) {
                        const name = alias[k] || k
                        this.byCode(code, data, `${name}：${err}`, timeout)
                    }
                }
            } else {
                this.byCode(code, data, null, timeout)
            }
        }
    }

    return new MessageBoard()
}

export default (ctx, inject) => {
    inject('message', createMessageBoard(ctx))
}

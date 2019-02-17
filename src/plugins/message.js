
function createMessageBoard (ctx) {
    let messageId = 1

    class MessageBoard {
        text (text, type = 'default', timeout = 3000) {
            // type: default, secondary, success, warning, error
            let convert = {
                'default': '',
                'secondary': 'am-alert-secondary',
                'success': 'am-alert-success',
                'warning': 'am-alert-warning',
                'error': 'am-alert-danger'
            }
            let data = { type, text, class: convert[type], id: messageId++ }
            if (ctx.store) {
                ctx.store.commit('MESSAGE_PUSH', data)
                _.delay(() => {
                    ctx.store.commit('MESSAGE_REMOVE', data)
                }, timeout)
            }
        }

        secondary (text, timeout = 3000) {
            this.text(text, 'secondary', timeout) // 灰色白字，很不明显
        }

        success (text, timeout = 3000) {
            this.text(text, 'success', timeout) // 绿色
        }

        warn (text, timeout = 3000) {
            this.message(text, 'success', timeout) // 绿色
        }

        error (text, timeout = 3000) {
            this.message(text, 'success', timeout) // 绿色
        }
    }

    return new MessageBoard()
}

export default (ctx, inject) => {
    inject('message', createMessageBoard(ctx))
}

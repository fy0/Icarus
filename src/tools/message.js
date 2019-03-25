let store = null

if (process.browser) {
    window.onNuxtReady(({ $store }) => {
        store = $store
    })
}

let messageId = 1

// 这个模块先不动吧，暂且如此
$.message = function (type, text, timeout = 3000) {
    // type: default, secondary, success, warning, error
    let convert = {
        'default': '',
        'secondary': 'am-alert-secondary',
        'success': 'am-alert-success',
        'warning': 'am-alert-warning',
        'error': 'am-alert-danger'
    }
    let data = { type, text, class: convert[type], id: messageId++ }
    // TODO: 暂时无法解决
    if (store) {
        store.commit('MESSAGE_PUSH', data)
        _.delay(() => {
            store.commit('MESSAGE_REMOVE', data)
        }, timeout)
    }
}

this.$message.text = function (text, timeout = 3000) {
    $.message('default', text, timeout) // 蓝色
}

this.$message.secondary = function (text, timeout = 3000) {
    $.message('secondary', text, timeout) // 灰色白字，很不明显
}

this.$message.success = function (text, timeout = 3000) {
    $.message('success', text, timeout) // 绿色
}

this.$message.warning = function (text, timeout = 3000) {
    $.message('warning', text, timeout) // 黄色
}

this.$message.error = function (text, timeout = 3000) {
    $.message('error', text, timeout) // 红色
}

this.$message.byCode = function (code, data, text = null, timeout = 3000) {
    text = text || store.state.misc.retinfo_cn[code]
    if (code === store.state.misc.retcode.SUCCESS) this.$message.success(text, timeout)
    else if (code === store.state.misc.retcode.TOO_FREQUENT && data) {
        this.$message.error(`${text}，尚需等待 ${data} 秒`, timeout)
    } else this.$message.error(text, timeout)
}

this.$message.by_form = function (code, data, alias, timeout = 6000) {
    if (code) {
        for (let [k, errs] of Object.entries(data)) {
            for (let err of errs) {
                let name = alias[k] || k
                this.$message.byCode(code, data, `${name}：${err}`, timeout)
            }
        }
    } else {
        this.$message.byCode(code, data, null, timeout)
    }
}

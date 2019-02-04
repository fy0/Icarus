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

$.message_text = function (text, timeout = 3000) {
    $.message('default', text, timeout) // 蓝色
}

$.message_secondary = function (text, timeout = 3000) {
    $.message('secondary', text, timeout) // 灰色白字，很不明显
}

$.message_success = function (text, timeout = 3000) {
    $.message('success', text, timeout) // 绿色
}

$.message_warning = function (text, timeout = 3000) {
    $.message('warning', text, timeout) // 黄色
}

$.message_error = function (text, timeout = 3000) {
    $.message('error', text, timeout) // 红色
}

$.message_by_code = function (code, data, text = null, timeout = 3000) {
    text = text || store.state.misc.retinfo_cn[code]
    if (code === store.state.misc.retcode.SUCCESS) $.message_success(text, timeout)
    else if (code === store.state.misc.retcode.TOO_FREQUENT && data) {
        $.message_error(`${text}，尚需等待 ${data} 秒`, timeout)
    } else $.message_error(text, timeout)
}

$.message_by_form = function (code, data, alias, timeout = 6000) {
    if (code) {
        for (let [k, errs] of Object.entries(data)) {
            for (let err of errs) {
                let name = alias[k] || k
                $.message_by_code(code, data, `${name}：${err}`, timeout)
            }
        }
    } else {
        $.message_by_code(code, data, null, timeout)
    }
}

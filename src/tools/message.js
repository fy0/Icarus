import state from '@/state.js'

let messageId = 1

$.message = function (type, text, timeout = 3000) {
    // type: default, secondary, success, warning, error
    let convert = {
        'default': '',
        'secondary': 'am-alert-secondary',
        'success': 'am-alert-success',
        'warning': 'am-alert-warning',
        'error': 'am-alert-danger'
    }
    let data = {type, text, class: convert[type], id: messageId++}
    state.msgs.push(data)
    _.delay(() => {
        state.msgs.splice(state.msgs.indexOf(data), 1)
    }, timeout)
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

$.message_by_code = function (code, text = null, timeout = 3000) {
    text = text || state.misc.retinfo_cn[code]
    if (code === state.misc.retcode.SUCCESS) $.message_success(text, timeout)
    else $.message_error(text, timeout)
}

$.message_by_form = function (code, data, alias, timeout = 6000) {
    if (code) {
        for (let [k, errs] of Object.entries(data)) {
            for (let err of errs) {
                let name = alias[k] || k
                $.message_by_code(code, `${name}：${err}`, timeout)
            }
        }
    } else {
        $.message_by_code(code, timeout)
    }
}

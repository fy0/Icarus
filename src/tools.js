import _ from 'lodash'
import state from '@/state.js'
import murmurhash from 'murmurhash'

let messageId = 1

$.media = {
    xs: {maxWidth: '35.5em'},
    sm: {minWidth: '35.5em'},
    md: {minWidth: '48em'},
    lg: {minWidth: '64em'},
    xl: {minWidth: '80em'}
}

$.lineStyle = function (board, key = 'border-left-color') {
    let bgColor = murmurhash.v3(board.name).toString(16).slice(0, 6)
    return {
        [key]: '#' + bgColor
    }
}

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
    $.message('default', text, timeout)
}

$.message_secondary = function (text, timeout = 3000) {
    $.message('secondary', text, timeout)
}

$.message_success = function (text, timeout = 3000) {
    $.message('success', text, timeout)
}

$.message_warning = function (text, timeout = 3000) {
    $.message('warning', text, timeout)
}

$.message_error = function (text, timeout = 3000) {
    $.message('error', text, timeout)
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

$.tpReg = function (name, func) {
    state.test.items.push([name, func])
}

$.tpRemove = function () {
    ;
}

$.tpClear = function () {
    state.test.items = []
}

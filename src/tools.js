
import _ from 'lodash'
import state from '@/state.js'

$.media = {
    xs: {maxWidth: '35.5em'},
    sm: {minWidth: '35.5em'},
    md: {minWidth: '48em'},
    lg: {minWidth: '64em'},
    xl: {minWidth: '80em'}
}

$.message = function (type, text) {
    // type: default, secondary, success, warning, error
    let convert = {
        'default': '',
        'secondary': 'am-alert-secondary',
        'success': 'am-alert-success',
        'warning': 'am-alert-warning',
        'error': 'am-alert-danger'
    }
    let data = {type, text, class: convert[type]}
    state.msgs.push(data)
    _.delay(() => {
        state.msgs.splice(state.msgs.indexOf(data), 1)
    }, 3000)
}

$.message_text = function (text) {
    $.message('default', text)
}

$.message_secondary = function (text) {
    $.message('secondary', text)
}

$.message_success = function (text) {
    $.message('success', text)
}

$.message_warning = function (text) {
    $.message('warning', text)
}

$.message_error = function (text) {
    $.message('error', text)
}

$.message_by_code = function (code, text = null) {
    text = text || state.misc.retinfo_cn[code]
    if (code === state.misc.retcode.SUCCESS) $.message_success(text)
    else $.message_error(text)
}

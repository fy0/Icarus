import _ from 'lodash'
import state from '@/state.js'
import murmurhash from 'murmurhash'
import Tweezer from 'tweezer.js'
import Vue from 'vue'
import api from './netapi.js'
import ws from './ws.js'

let messageId = 1
let scroller = null

$.scrollTo = function (el) {
    if (scroller) scroller.stop()
    scroller = new Tweezer({
        start: window.pageYOffset,
        end: el.getBoundingClientRect().top + window.pageYOffset,
        duration: 500
    })
        .on('tick', v => window.scrollTo(0, v))
        .on('done', () => {
            scroller = null
        })
        .begin()
}

$.dateFormat = function (d, format) {
    var date, k
    date = {
        'M+': d.getMonth() + 1,
        'd+': d.getDate(),
        'h+': d.getHours(),
        'm+': d.getMinutes(),
        's+': d.getSeconds(),
        'q+': Math.floor((d.getMonth() + 3) / 3),
        'S+': d.getMilliseconds()
    }
    if (/(y+)/i.test(format)) {
        format = format.replace(RegExp.$1, (d.getFullYear() + '').substr(4 - RegExp.$1.length))
    }
    for (k in date) {
        if (new RegExp('(' + k + ')').test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length === 1 ? date[k] : ('00' + date[k]).substr(('' + date[k]).length))
        }
    }
    return format
}

/**
 * Deep diff between two object, using lodash
 * @param  {Object} object Object compared
 * @param  {Object} base   Object to compare with
 * @return {Object}        Return a new object who represent the diff
 */
$.objDiff = function (object, base) {
    let changes = function (object, base) {
        return _.transform(object, (result, value, key) => {
            if (!_.isEqual(value, base[key])) {
                result[key] = (_.isObject(value) && _.isObject(base[key])) ? changes(value, base[key]) : value
            }
        })
    }
    return changes(object, base)
}

let notifSign = false

$.isAdmin = function () {
    return (state.user) && (state.user.group >= state.misc.USER_GROUP.ADMIN)
}

$.notifLoopOn = async () => {
    let fetchNotif = async () => {
        if (ws.conn) return
        if (state.user) {
            let ret = await api.notif.refresh()
            if (ret.code === api.retcode.SUCCESS) {
                if (ret.data) {
                    Vue.set(state, 'unread', ret.data)
                }
            }
        }
    }

    if (!notifSign) {
        setInterval(fetchNotif, 15000)
        notifSign = true
    }

    await fetchNotif()
}

$.media = {
    xs: {maxWidth: '35.5em'},
    sm: {minWidth: '35.5em'},
    md: {minWidth: '48em'},
    lg: {minWidth: '64em'},
    xl: {minWidth: '80em'}
}

$.lineStyle = function (board, key = 'border-left-color') {
    if (board.color) {
        return { [key]: '#' + board.color }
    }
    let bgColor = murmurhash.v3(board.name).toString(16).slice(0, 6)
    return { [key]: '#' + bgColor }
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

$.tpReg = function (name, func) {
    state.test.items.push([name, func])
}

$.tpRemove = function () {
    ;
}

$.tpClear = function () {
    state.test.items = []
}

$.regex = {
    id: /[a-fA-F0-9]+/,
    email: /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/,
    nickname: /^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]+$/
}

import Vue from 'vue'
import ws from '../ws.js'
import api from '../netapi.js'
import state from '@/state.js'

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

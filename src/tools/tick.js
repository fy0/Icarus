import Vue from 'vue'
import api from '../netapi.js'
import state from '@/state.js'

$.tickStart = async () => {
    let tickHttp = async () => {
        let auid = localStorage.getItem('auid')
        let ret = await api.tick(auid)
        if (ret.code === api.retcode.SUCCESS) {
            if (state.user) {
                Vue.set(state, 'unread', ret.data['notif_count'])
            } else {
                if (ret.data.auid) {
                    localStorage.setItem('auid', ret.data.auid)
                }
            }
        }
        state.userOnline = ret.data.online
    }

    setInterval(tickHttp, 15000)
    await tickHttp()
}

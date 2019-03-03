let api = null
let store = null

if (process.browser) {
    window.onNuxtReady((ctx) => {
        store = ctx.store
        api = ctx.$store.app.$api
    })
}

$.tickStart = async () => {
    if (process.server) return
    let tickHttp = async () => {
        let auid = localStorage.getItem('auid')
        let ret = await api.tick(auid)
        if (ret.code === api.retcode.SUCCESS) {
            if (store.state.user.userData) {
                store.commit('user/SET_UNREAD', ret.data['notif_count'])
            } else {
                if (ret.data.auid) {
                    localStorage.setItem('auid', ret.data.auid)
                }
            }
        }
        store.commit('user/SET_UNREAD', ret.data['notif_count'])
        store.commit('SET_ONLINE', ret.data.online)
    }

    setInterval(tickHttp, 15000)
    await tickHttp()
}

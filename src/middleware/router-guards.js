export default async function ({ store, route, redirect, req }) {
    // 重置对话框
    store.commit('dialog/CLOSE_ALL')
    // 试图初始化全局数据
    await store.dispatch('tryInitLoad')

    if (!store.state.misc) {
        // let ret = await api.misc()
        // store.commit('SET_MISC', ret.data)

        // if (process.browser) {
        //     ret = await api.userInfo()
        //     if (ret.code === 0) {
        //         store.commit('SET_USERDATA', ret.data)
        //     }
        // }
    }
}

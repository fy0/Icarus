
export default async function ({ store, route, redirect, req }: any) {
    // 重置对话框
    store.commit('dialog/CLOSE_ALL')
    // 试图初始化全局数据
    await store.dispatch('tryInitLoad')
}

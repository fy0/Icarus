export default {
    namespaced: true,

    state: {
        userData: null,
        unread: 0
    },
    getters: {
        // 注意：这个_userData不要在外部使用
        _userData: (state) => state.userData || {},

        roles: (state, getters) => getters._userData.roles,
        mainRole: (state, getters) => getters._userData['main_role'],
        // 站点管理员：可以见到后台的管理员
        isSiteAdmin: (state, getters) => ['superuser', 'admin'].indexOf('getters.mainRole') !== -1
    },
    mutations: {
        setUserData (state, data) {
            state.userData = data
        },
        setUnread (state, data) {
            state.unread = data
        },
        reset (state) {
            state.unread = 0
            state.userData = null
        }
    },
    actions: {
    }
}

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
        // 是否能编辑WIKI
        canEditWiki: (state, getters) => {
            if (!state.userData) return
            return getters.isSiteAdmin || state.userData.is_wiki_editor
        },
        basicRole: (state, getters) => state.userData ? 'user' : null,
        wikiEditRole: (state, getters) => {
            if (getters.isSiteAdmin) {
                return getters.mainRole
            }
            if (state.userData.is_wiki_editor) {
                return 'wiki_editor'
            }
        },
        // 站点管理员：可以见到后台的管理员
        isSiteAdmin: (state, getters) => ['superuser', 'admin'].indexOf(getters.mainRole) !== -1,
        // 论坛管理员
        isForumAdmin: (state, getters) => getters.isSiteAdmin
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

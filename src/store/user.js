export const state = () => ({
    userData: null,
    unread: 0
})

export const getters = {
    // 注意：这个_userData不要在外部使用
    _userData: (state) => state.userData || {},

    // 是否新注册用户
    isNewUser: (state, getters) => {
        if (!state.userData) return
        const ts = new Date().getTime() / 1000
        if ((state.userData.is_new_user) && (ts - state.userData.time < 24 * 60 * 60)) {
            return true
        }
    },

    roles: (state, getters) => getters._userData.roles,
    basicRole: (state, getters) => state.userData ? 'user' : null,
    mainRole: (state, getters) => getters._userData.main_role,
    forumAdminRole: (state, getters) => {
        if (getters.isSiteAdmin) {
            return getters.mainRole
        }
    },
    wikiEditRole: (state, getters) => {
        if (getters.isSiteAdmin) {
            return getters.mainRole
        }
        if (getters._userData.is_wiki_editor) {
            return 'wiki_editor'
        }
    },
    // 是否能编辑WIKI
    isWikiAdmin: (state, getters) => {
        if (!state.userData) return
        return getters.isSiteAdmin || state.userData.is_wiki_editor
    },
    // 站点管理员：可以见到后台的管理员
    isSiteAdmin: (state, getters) => ['superuser', 'admin'].indexOf(getters.mainRole) !== -1,
    // 论坛管理员
    isForumAdmin: (state, getters) => getters.isSiteAdmin
}

export const mutations = {
    SET_USER_DATA (state, data) {
        state.userData = data
    },
    SET_UNREAD (state, data) {
        state.unread = data
    },
    RESET (state) {
        state.unread = 0
        state.userData = null
    }
}

export const actions = {
    // 退出登录
    async apiSignout ({ dispatch }) {
        const ret = await this.$api.user.signout()
        if (ret.code === this.$api.retcode.SUCCESS || ret.code === this.$api.retcode.FAILED) {
            await dispatch('initLoad', null, { root: true })
            this.$message.success('登出成功')
        }
    },
    // 获取当前用户信息
    async apiGetUserData ({ state, getters, commit }, uid) {
        if (!uid) uid = getters._userData.id
        if (!uid) return

        const userInfo = await this.$api.user.get({ id: uid }, { role: 'user' })
        if (userInfo.code === this.$api.retcode.SUCCESS) {
            commit('SET_USER_DATA', userInfo.data)
            this.$api.getDefaultRole = () => {
                return this.$user.mainRole
            }
        } else {
            this.$message.error('获取用户信息失败，可能是网络问题或者服务器无响应')
        }
    },
    // 设置当前用户信息
    async apiSetUserData ({ state, getters, dispatch }, newData) {
        const oldData = state.userData
        const updateData = $.objDiff(newData, oldData)
        delete updateData.avatar // 头像的更新是独立的，参见BUG12
        if (Object.keys(updateData).length === 0) return
        const ret = await this.$api.user.set({ id: oldData.id }, updateData, { role: 'user' })
        if (ret.code === this.$api.retcode.SUCCESS) {
            await dispatch('apiGetUserData')
            this.$message.success('信息修改成功！')
        }
    }
}

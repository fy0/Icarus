import config from '@/config.js'

const debug = process.env.NODE_ENV !== 'production'
export const strict = debug

export const state = () => ({
    misc: null,
    loading: 0,
    msgs: [],
    messageId: 1,
    online: 0,
    _initing: false,

    config: {
        remote: config.remote,
        ws: { enable: false },

        siteName: 'Icarus',
        title: 'Icarus',
        logoText: 'Icarus'
    }
})

export const getters = {
    misc: (state) => state.misc || {},
    BACKEND_CONFIG: (state, getters) => getters.misc.BACKEND_CONFIG || {},
    POST_TYPES: (state, getters) => getters.misc.POST_TYPES || {},
    POST_TYPES_TXT: (state, getters) => getters.misc.POST_TYPES_TXT || {},
    POST_STATE: (state, getters) => getters.misc.POST_STATE || {},
    POST_STATE_TXT: (state, getters) => getters.misc.POST_STATE_TXT || {},
    POST_VISIBLE: (state, getters) => getters.misc.POST_VISIBLE || {},
    POST_VISIBLE_TXT: (state, getters) => getters.misc.POST_VISIBLE_TXT || {},
    MANAGE_OPERATION: (state, getters) => getters.misc.MANAGE_OPERATION || {},
    MANAGE_OPERATION_TXT: (state, getters) => getters.misc.MANAGE_OPERATION_TXT || {},
    USER_GROUP: (state, getters) => getters.misc.USER_GROUP || {},
    USER_GROUP_TXT: (state, getters) => getters.misc.USER_GROUP_TXT || {},
    USER_GROUP_TO_ROLE: (state, getters) => getters.misc.USER_GROUP_TO_ROLE || {},
    NOTIF_TYPE: (state, getters) => getters.misc.NOTIF_TYPE || {},

    isInited: (state) => (!state._initing) && (state.misc),
    isAboutPageEnable: (state, getters) => getters.BACKEND_CONFIG.ABOUT_PAGE_ENABLE,
    isSearchEnable: (state, getters) => getters.BACKEND_CONFIG.SEARCH_ENABLE
}

export const mutations = {
    SET_INITING (state, data) {
        state._initing = data
    },
    // 设置
    SET_MISC (state, data) {
        state.misc = data
        state.config.siteName = data.BACKEND_CONFIG.SITE_NAME
        state.config.title = data.BACKEND_CONFIG.SITE_TITLE_TEXT
        state.config.logoText = data.BACKEND_CONFIG.SITE_LOGO_TEXT
        this.$api.retcode = data.retcode
        this.$api.retinfo = data.retinfo_cn
    },
    // 全局加载动画相关
    LOADING_INC (state, num = 1) {
        if (process.browser) {
            state.loading += num
        }
    },
    LOADING_DEC (state, num = 1) {
        if (process.browser) {
            state.loading -= num
        }
    },
    LOADING_SET (state, num = 0) {
        if (process.browser) {
            state.loading = num
        }
    },
    // MESSAGE
    MESSAGE_PUSH (state, info) {
        info.id = state.messageId++
        state.msgs.push(info)
    },
    MESSAGE_REMOVE (state, info) {
        state.msgs.splice(state.msgs.indexOf(info), 1)
    },
    SET_ONLINE (state, num) {
        state.online = num
    }
}

export const actions = {
    // 初始化加载
    async initLoad ({ state, commit, dispatch }, payload) {
        if (state._initing) return
        commit('SET_INITING', true)
        // 获取MISC信息
        const ret = await this.$api.misc()
        if (ret.code !== this.$api.retcode.SUCCESS) {
            this.$message.error('服务器的返回异常，请刷新重试。', 5000)
            commit('SET_INITING', false)
            return
        }
        commit('SET_MISC', ret.data)

        if (ret.data.user) {
            // 若为登录用户，试图获取用户信息
            const miscUser = ret.data.user
            await dispatch('user/apiGetUserData', miscUser.id)

            if (miscUser.daily_reward) {
                this.$message.success(`每日登陆，获得经验 ${miscUser.daily_reward.exp} 点`, 5000)
            }
        } else {
            // 未登录，清除现有信息（用于退出登录等场景）
            commit('user/RESET')
        }
        // TODO: 需要替代方案
        // $.tickStart()
        commit('SET_INITING', false)
    },
    // 若未初始化，进行初始化
    async tryInitLoad ({ state, dispatch }) {
        if (!(state.misc || state._initing)) {
            await dispatch('initLoad')
        }
    },
    async nuxtServerInit ({ commit, dispatch }, { req, app }) {
        // 设置初始 access token
        // this.$api.accessToken = this.$storage.getUniversal('t')
        // 尝试加载
        await dispatch('tryInitLoad')
        // let ret = await this.$api.misc()
        // commit('SET_MISC', ret.data)

        // console.log(111, req.headers.cookie)
        // ret = await this.$api.userInfo2(req.headers)
        // if (ret.code === 0) {
        //     commit('SET_USERDATA', ret.data)
        // }
    }
}

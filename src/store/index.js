import Vue from 'vue'
import Vuex from 'vuex'
import api from '../netapi'
import dialog from './modules/dialog'
import forum from './modules/forum'

Vue.use(Vuex)
const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
    strict: debug,
    modules: {
        dialog,
        forum
    },
    state: {
        misc: null,
        userData: null,
        loading: 0,

        _initing: false
    },
    getters: {
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
        NOTIF_TYPE: (state, getters) => getters.misc.NOTIF_TYPE || {}
    },
    mutations: {
        SET_INITING (state, data) {
            state._initing = data
        },
        // 设置
        SET_MISC (state, data) {
            state.misc = data
            api.retcode = data.retcode
            api.retinfo = data.retinfo_cn
        },
        SET_USER_DATA (state, data) {
            state.userData = data
        },
        // 全局加载动画相关
        LOADING_INC (state, num = 1) {
            state.loading += num
        },
        LOADING_DEC (state, num = 1) {
            state.loading -= num
        },
        LOADING_SET (state, num = 0) {
            state.loading = num
        }
    },
    actions: {
        // 初始化加载
        async initLoad ({ state, commit, dispatch }, payload) {
            if (state._initing) return
            commit('SET_INITING', true)
            // 获取MISC信息
            let ret = await $.retryUntilSuccess(api.misc)
            if (ret.code !== api.retcode.SUCCESS) {
                $.message_error(`服务器的返回异常，请刷新重试。`, 5000)
                commit('SET_INITING', false)
                return
            }
            commit('SET_MISC', ret.data)

            // 若为登录用户，试图获取用户信息
            if (ret.data.user) {
                let miscUser = ret.data.user
                let userInfo = await api.user.get({ id: miscUser.id }, 'user')
                if (userInfo.code === api.retcode.SUCCESS) {
                    // 获取成功
                    if (miscUser.daily_reward) {
                        $.message_success(`每日登陆，获得经验 ${miscUser.daily_reward['exp']} 点`, 5000)
                    }

                    commit('SET_USER_DATA', userInfo.data)
                } else {
                    $.message_error('获取用户信息失败，可能是网络问题或者服务器无响应')
                }
            }
            $.tickStart()
            commit('SET_INITING', false)
        },
        // 若未初始化，进行初始化
        async tryInitLoad ({ state, dispatch }) {
            if (!(state.misc || state._initing)) {
                await dispatch('initLoad')
            }
        }
    }
})

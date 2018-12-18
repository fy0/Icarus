import Vue from 'vue'
import Vuex from 'vuex'
import api from '../netapi'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        misc: null,
        userData: null,
        loading: 0
    },
    modules: {

    },
    mutations: {
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
        LOADING_RESET (state) {
            state.loading = 0
        }
    },
    actions: {
        // 初始化加载
        async initLoad ({ state, commit, dispatch }, payload) {
            // 获取MISC信息
            let ret = $.retryUntilSuccess(api.misc)
            commit('SET_MISC', ret.data)
            ret = await api.user.getUserId()
            if (ret.code === api.retcode.SUCCESS) {
                // 若有结果（已登录）
                ret = await api.user.get({ id: ret.data.id }, 'user')
                if (ret.code !== api.retcode.SUCCESS) {
                    // 获取失败
                    $.message_error('获取用户信息失败，可能是网络问题或者服务器无响应')
                    if (payload.failed) payload.failed()
                } else {
                    // 登录成功
                    if (state.misc.extra.daily_reward) {
                        $.message_success(`每日登陆，获得经验 ${state.misc.extra.daily_reward['exp']} 点`, 5000)
                        ret.data.exp += state.misc.extra.daily_reward['exp']
                    }

                    commit('SET_USER_DATA', ret.data)
                }
            }
        },
        // 若未初始化，进行初始化
        async tryInitLoad ({ state, dispatch }) {
            if (!state.misc) {
                await dispatch('initLoad')
            }
        }
    },
    getters: {
        // 获取后端配置
        backendConfig: (state) => {
            return (state.misc && state.misc.BACKEND_CONFIG) ? state.misc.BACKEND_CONFIG : {}
        }
    }
})

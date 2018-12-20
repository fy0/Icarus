import Vuex from 'vuex'

export default new Vuex.Store({
    namespaced: true,

    state: {
        userData: null,
        unread: 0
    },
    getters: {
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
})

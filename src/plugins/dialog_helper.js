import store from '../store/index.js'

class DialogsHelperGetters {
    setBoardManage (val, data) {
        store.commit('dialog/SET_BOARD_MANAGE', { val, data })
    }
    setCommentManage (val, data) {
        store.commit('dialog/SET_COMMENT_MANAGE', { val, data })
    }
    setTopicManage (val, data) {
        store.commit('dialog/SET_TOPIC_MANAGE', { val, data })
    }
    setUserManage (val, data) {
        store.commit('dialog/SET_USER_MANAGE', { val, data })
    }
    setUserNickname (val) {
        store.commit('dialog/SET_USER_NICKANME', { val })
    }
    setUserInactive (val) {
        store.commit('dialog/SET_USER_INACTIVE', { val })
    }
    setUserSignout (val) {
        store.commit('dialog/SET_USER_SIGNOUT', { val })
    }
}

let dhg = new DialogsHelperGetters()

export default {
    install (Vue, options) {
        Object.defineProperty(Vue.prototype, '$dialogs', {
            get () {
                return dhg
            }
        })
    }
}

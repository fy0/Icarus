import store from '../store/index.js'

class DialogsHelperGetters {
    setTopicManage (val, data) {
        store.commit('dialog/SET_TOPIC_MANAGE', { val, data })
    }
    setUserNickname (val) {
        store.commit('dialog/SET_USER_NICKANME', { val })
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

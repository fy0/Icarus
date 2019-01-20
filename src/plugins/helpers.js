let store = null
let user = null
let getters = null

class UserHelperGetters {
    get data () { return user.userData }
    get unread () { return user.unread }

    get isNewUser () { return getters['user/isNewUser'] }

    get roles () { return getters['user/roles'] }
    get basicRole () { return getters['user/basicRole'] }
    get mainRole () { return getters['user/mainRole'] }
    get forumAdminRole () { return getters['user/forumAdminRole'] }
    get wikiEditRole () { return getters['user/wikiEditRole'] }

    get isWikiAdmin () { return getters['user/isWikiAdmin'] }
    get isSiteAdmin () { return getters['user/isSiteAdmin'] }
    get isForumAdmin () { return getters['user/isForumAdmin'] }
}

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
    setUserAvatar (val, data) {
        store.commit('dialog/SET_USER_AVATAR', { val, data })
    }
    setSiteNew (val) {
        store.commit('dialog/SET_SITE_NEW', { val })
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

let uhg = new UserHelperGetters()
let dhg = new DialogsHelperGetters()

export default ({ app }, inject) => {
    store = app.store
    user = store.state.user
    getters = store.getters

    app.$config = {
        get () { return this.$store.state.config }
    }
    app.$misc = {
        get () { return this.$store.state.misc }
    }
    app.$user = {
        get () { return uhg }
    }
    app.$dialogs = {
        get () { return dhg }
    }
}

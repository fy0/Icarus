/* eslint-disable no-new-wrappers */

class UserHelperGetters {
    get data () { return this._user.userData }
    get unread () { return this._user.unread }

    get isNewUser () { return this._getters['user/isNewUser'] }

    get roles () { return this._getters['user/roles'] }
    get basicRole () { return this._getters['user/basicRole'] }
    get mainRole () { return this._getters['user/mainRole'] }
    get forumAdminRole () { return this._getters['user/forumAdminRole'] }
    get wikiEditRole () { return this._getters['user/wikiEditRole'] }

    get isWikiAdmin () { return this._getters['user/isWikiAdmin'] }
    get isSiteAdmin () { return this._getters['user/isSiteAdmin'] }
    get isForumAdmin () { return this._getters['user/isForumAdmin'] }
}

class DialogsHelperGetters {
    setBoardManage (val, data) {
        this._store.commit('dialog/SET_BOARD_MANAGE', { val, data })
    }
    setCommentManage (val, data) {
        this._store.commit('dialog/SET_COMMENT_MANAGE', { val, data })
    }
    setTopicManage (val, data) {
        this._store.commit('dialog/SET_TOPIC_MANAGE', { val, data })
    }
    setUserAvatar (val, data) {
        this._store.commit('dialog/SET_USER_AVATAR', { val, data })
    }
    setSiteNew (val) {
        this._store.commit('dialog/SET_SITE_NEW', { val })
    }
    setUserManage (val, data) {
        this._store.commit('dialog/SET_USER_MANAGE', { val, data })
    }
    setUserNickname (val) {
        this._store.commit('dialog/SET_USER_NICKANME', { val })
    }
    setUserInactive (val) {
        this._store.commit('dialog/SET_USER_INACTIVE', { val })
    }
    setUserSignout (val) {
        this._store.commit('dialog/SET_USER_SIGNOUT', { val })
    }
}

export default (ctx, inject) => {
    let uhg = new UserHelperGetters()
    let dhg = new DialogsHelperGetters()

    dhg._store = ctx.store
    uhg._user = ctx.store.state.user
    uhg._getters = ctx.store.getters

    inject('misc', new Proxy(new String('state.misc proxy'), {
        get: (target, name) => ctx.store.state.misc[name]
    }))
    inject('config', new Proxy(new String('state.config proxy'), {
        get: (target, name) => ctx.store.state.config[name]
    }))

    inject('user', uhg)
    inject('dialogs', dhg)
}

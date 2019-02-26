// import Vue from 'vue'

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

    // if (process.browser) {
    //     // 浏览器端
    //     let setUp = (ctx) => {
    //         dhg._store = ctx.store
    //         uhg._user = ctx.store.state.user
    //         uhg._getters = ctx.store.getters
    //     }

    //     Object.defineProperty(Vue.prototype, '$config', {
    //         get () { return this.$store.state.config }
    //     })

    //     Object.defineProperty(Vue.prototype, '$misc', {
    //         get () { return this.$store.state.misc }
    //     })

    //     Object.defineProperty(Vue.prototype, '$user', {
    //         get () { setUp(this); return uhg }
    //     })

    //     Object.defineProperty(Vue.prototype, '$dialogs', {
    //         get () { setUp(this); return dhg }
    //     })
    // } else {
    //     // 服务器端
    //     if (!Vue.prototype.$misc === undefined) {
    //         Object.defineProperty(Vue.prototype, '$misc', {
    //             get () { return ctx.store.state.misc }
    //         })
    //     }

    //     if (!Vue.prototype.$config === undefined) {
    //         Object.defineProperty(Vue.prototype, '$config', {
    //             get () { return ctx.store.state.config }
    //         })
    //     }

    //     if (!Vue.prototype.$user === undefined) {
    //         Object.defineProperty(Vue.prototype, '$user', {
    //             get () { return uhg }
    //         })
    //     }

    //     if (!Vue.prototype.$dialogs === undefined) {
    //         Object.defineProperty(Vue.prototype, '$dialogs', {
    //             get () { return dhg }
    //         })
    //     }
    // }

    inject('misc', ctx.store.state.misc)
    inject('config', ctx.store.state.config)

    inject('user', uhg)
    inject('dialogs', dhg)
}

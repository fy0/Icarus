import { Store, GetterTree } from "vuex/types/index"

/* eslint-disable no-new-wrappers */

declare module 'vue/types/vue' {
  interface Vue {
    $misc: any
    $config: any
    $user: any
    $dialogs: any
  }
}

declare module 'vuex' {
  interface Store<S> {
    $misc: any
    $config: any
    $user: any
    $dialogs: any
  }
}

declare module 'vuex-module-decorators' {
  interface VuexModule<S, R> {
    $misc: any
    $config: any
    $user: any
    $dialogs: any
  }
}

class UserHelperGetters {
  _user: any
  _getters: GetterTree<any, any>

  constructor (store: Store<any>) {
    this._user = store.state.user
    this._getters = store.getters
  }

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
  _store: Store<any>

  constructor (store: Store<any>) {
    this._store = store
  }

  setBoardManage (val: any, data: any) {
    this._store.commit('dialog/SET_BOARD_MANAGE', { val, data })
  }

  setCommentManage (val: any, data: any) {
    this._store.commit('dialog/SET_COMMENT_MANAGE', { val, data })
  }

  setTopicManage (val: any, data: any) {
    this._store.commit('dialog/SET_TOPIC_MANAGE', { val, data })
  }

  setUserAvatar (val: any, data: any) {
    this._store.commit('dialog/SET_USER_AVATAR', { val, data })
  }

  setSiteNew (val: any) {
    this._store.commit('dialog/SET_SITE_NEW', { val })
  }

  setUserManage (val: any, data: any) {
    this._store.commit('dialog/SET_USER_MANAGE', { val, data })
  }

  setUserNickname (val: any) {
    this._store.commit('dialog/SET_USER_NICKANME', { val })
  }

  setUserInactive (val: any) {
    this._store.commit('dialog/SET_USER_INACTIVE', { val })
  }

  setUserSignout (val: any) {
    this._store.commit('dialog/SET_USER_SIGNOUT', { val })
  }
}

export default (ctx: any, inject: any) => {
  const uhg = new UserHelperGetters(ctx.store)
  const dhg = new DialogsHelperGetters(ctx.store)

  inject('misc', new Proxy(new String('state.misc proxy'), {
    get: (target, name) => ctx.store.state.misc[name]
  }))
  inject('config', new Proxy(new String('state.config proxy'), {
    get: (target, name) => ctx.store.state.config[name]
  }))

  inject('user', uhg)
  inject('dialogs', dhg)
}

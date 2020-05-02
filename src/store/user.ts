import { retcode } from 'slim-tools'
import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { $api } from '../plugins/api'

@Module({
  // name: 'user',
  stateFactory: true,
  namespaced: true
})
export default class UserModule extends VuexModule {
  userData: any = null
  unread = 0

  get _userData (): any {
    return this.userData || {}
  }

  // 是否新注册用户
  get isNewUser () {
    if (!this.userData) return
    const ts = new Date().getTime() / 1000
    if ((this.userData.is_new_user) && (ts - this.userData.time < 24 * 60 * 60)) {
      return true
    }
  }

  get roles () {
    return this._userData.roles
  }

  get basicRole () {
    return this.userData ? 'user' : null
  }

  get mainRole () {
    return this.userData ? this.userData.main_role : null
  }

  // 是否能编辑WIKI
  get isWikiAdmin () {
    if (!this.userData) return
    return this.isSiteAdmin || this.userData.is_wiki_editor
  }

  // 站点管理员：可以见到后台的管理员
  get isSiteAdmin () {
    return ['superuser', 'admin'].indexOf(this.mainRole) !== -1
  }

  // 论坛管理员
  get isForumAdmin () {
    return this.isSiteAdmin
  }

  get forumAdminRole () {
    if (this.isSiteAdmin) {
      return this.mainRole
    }
  }

  get wikiEditRole () {
    if (this.isSiteAdmin) {
      return this.mainRole
    }
    if (this._userData.is_wiki_editor) {
      return 'wiki_editor'
    }
  }

  @Mutation
  SET_USER_DATA (data: any) {
    this.userData = data
  }

  @Mutation
  SET_UNREAD (data: any) {
    this.unread = data
  }

  @Mutation
  RESET () {
    this.unread = 0
    this.userData = null
  }

  // 退出登录
  @Action
  async apiSignout () {
    const ret = await $api.user.signout()
    if (ret.code === retcode.SUCCESS || ret.code === retcode.FAILED) {
      await this.context.dispatch('initLoad', null, { root: true })
      this.$message.success('登出成功')
    }
  }

  // 获取当前用户信息
  @Action
  async apiGetUserData (uid: any) {
    let { commit } = this.context
    if (!uid) uid = this._userData.id
    if (!uid) return

    const userInfo = await $api.user.get({ id: uid }, { role: 'user' })
    if (userInfo.code === retcode.SUCCESS) {
      commit('SET_USER_DATA', userInfo.data)
      $api.getDefaultRole = () => {
        return this.mainRole
      }
    } else {
      this.$message.error('获取用户信息失败，可能是网络问题或者服务器无响应')
    }
  }

  // 设置当前用户信息
  async apiSetUserData (newData: any) {
    let { dispatch } = this.context

    const oldData = this.userData
    const updateData = $.objDiff(newData, oldData)
    delete updateData.avatar // 头像的更新是独立的，参见BUG12
    if (Object.keys(updateData).length === 0) return
    const ret = await $api.user.set({ id: oldData.id }, updateData, { role: 'user' })
    if (ret.code === retcode.SUCCESS) {
      await dispatch('apiGetUserData')
      this.$message.success('信息修改成功！')
    }
  }
}

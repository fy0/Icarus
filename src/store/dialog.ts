import { Module, VuexModule, Mutation } from 'vuex-module-decorators'

@Module({
  // name: 'dialog',
  stateFactory: true,
  namespaced: true
})
export default class DialogModule extends VuexModule {
  // 主题管理
  topicManage = false
  topicManageData = null
  // 板块管理
  boardManage = false
  boardManageData = null
  // 用户管理
  userManage = false
  userManageData = null
  // 评论管理
  commentManage = false
  commentManageData = null
  // 新站点指引
  siteNew = false
  // 设置头像
  userSetAvatar = false
  userSetAvatarData = null
  // 用户未邮件激活提示框
  userInactive = false
  // 设置昵称
  userSetNickname = false
  // 用户登出确认
  userSignout = false

  // 主题管理
  @Mutation
  SET_TOPIC_MANAGE ({ val, data }: any) {
    this.topicManage = val
    this.topicManageData = data
  }

  // 板块管理
  @Mutation
  SET_BOARD_MANAGE ({ val, data }: any) {
    this.boardManage = val
    this.boardManageData = data
  }

  // 用户管理
  @Mutation
  SET_USER_MANAGE ({ val, data }: any) {
    this.userManage = val
    this.userManageData = data
  }

  // 评论管理
  @Mutation
  SET_COMMENT_MANAGE ({ val, data }: any) {
    this.commentManage = val
    this.commentManageData = data
  }

  // 设置头像对话框
  @Mutation
  SET_USER_AVATAR ({ val, data }: any) {
    this.userSetAvatar = val
    this.userSetAvatarData = data
  }

  // 新站点提示对话框
  @Mutation
  SET_SITE_NEW ({ val }: any) {
    this.siteNew = val
  }

  // 未激活提示
  @Mutation
  SET_USER_INACTIVE ({ val }: any) {
    this.userInactive = val
  }

  // 设置用户昵称
  @Mutation
  SET_USER_NICKANME ({ val }: any) {
    this.userSetNickname = val
  }

  // 用户登出确认
  @Mutation
  SET_USER_SIGNOUT ({ val }: any) {
    this.userSignout = val
  }

  // 写入板块信息
  @Mutation
  WRITE_BOARD_MANAGE_DATA (data: any) {
    if (this.boardManageData) {
      Object.assign(this.boardManageData, data)
    }
  }

  // 写入板块信息
  @Mutation
  WRITE_USER_MANAGE_DATA (data: any) {
    if (this.userManageData) {
      Object.assign(this.userManageData, data)
    }
  }

  // 关闭所有
  @Mutation
  CLOSE_ALL () {
    this.topicManage = false
    this.boardManage = false
    this.userManage = false
    this.commentManage = false
    this.siteNew = false
    this.userSetAvatar = false
    this.userInactive = false
    this.userSetNickname = false
    this.userSignout = false
  }
}

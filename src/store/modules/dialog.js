export default {
    namespaced: true,

    state: {
        // 主题管理
        topicManage: null,
        topicManageData: null,
        // 板块管理
        boardManage: null,
        boardManageData: null,
        // 用户管理
        userManage: null,
        userManageData: null,
        // 评论管理
        commentManage: null,
        commentManageData: null,
        // 新站点指引
        siteNew: false,
        // 设置头像
        userSetAvatar: false,
        userSetAvatarData: null,
        // 用户未邮件激活提示框
        userInactive: false,
        // 设置昵称
        userSetNickname: false,
        // 用户登出确认
        userSignout: false
    },
    getters: {
    },
    mutations: {
        SET_TOPIC_MANAGE: (state, { val, data }) => {
            state.topicManage = val
            state.topicManageData = data
        }
    },
    actions: {
    }
}

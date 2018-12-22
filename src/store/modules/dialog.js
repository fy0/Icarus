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
        // 主题管理
        SET_TOPIC_MANAGE: (state, { val, data }) => {
            state.topicManage = val
            state.topicManageData = data
        },
        // 板块管理
        SET_BOARD_MANAGE: (state, { val, data }) => {
            state.boardManage = val
            state.boardManageData = data
        },
        // 用户管理
        SET_USER_MANAGE: (state, { val, data }) => {
            state.userManage = val
            state.userManageData = data
        },
        // 评论管理
        SET_COMMENT_MANAGE: (state, { val, data }) => {
            state.commentManage = val
            state.commentManageData = data
        },
        // 设置头像对话框
        SET_USER_AVATAR: (state, { val, data }) => {
            state.userSetAvatar = val
            state.userSetAvatarData = data
        },
        // 新站点提示对话框
        SET_SITE_NEW: (state, { val }) => {
            state.siteNew = val
        },
        // 未激活提示
        SET_USER_INACTIVE: (state, { val }) => {
            state.userInactive = val
        },
        // 设置用户昵称
        SET_USER_NICKANME: (state, { val }) => {
            state.userSetNickname = val
        },
        // 用户登出确认
        SET_USER_SIGNOUT: (state, { val }) => {
            state.userSignout = val
        },
        // 写入板块信息
        WRITE_BOARD_MANAGE_DATA: (state, data) => {
            if (state.boardManageData) {
                Object.assign(state.boardManageData, data)
            }
        },
        // 写入板块信息
        WRITE_USER_MANAGE_DATA: (state, data) => {
            if (state.userManageData) {
                Object.assign(state.userManageData, data)
            }
        },
        // 关闭所有
        CLOSE_ALL: (state) => {
            state.topicManage = false
            state.boardManage = false
            state.userManage = false
            state.commentManage = false
            state.siteNew = false
            state.userSetAvatar = false
            state.userInactive = false
            state.userSetNickname = false
            state.userSignout = false
        }
    },
    actions: {
    }
}

import config from '@/config.js'
// import tools from "./tools.js"

let loadingGetKey = (route) => {
    // 直接这样做会有bug，不知道为什么，所以使用替代方案
    // import router from './router'
    // return router.currentRoute.fullPath
    return route.fullPath
}

let state = {
    /* 实际内容动态获取
    misc: {
        USER_LEVEL: {
            'DEL': 0,
            'NORMAL': 50,
        },
        USER_LEVEL_TXT: {
            0: '删除',
            50: '正常'
        },
        POST_STATE: { ... },
        POST_STATE_TXT: { ... },
        BACKEND_CONFIG: {
            ...
        }
    },
    */
    config,
    msgs: [],
    // 对话框开关
    dialog: {
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
        // 设置头像
        userSetAvatar: false,
        userSetAvatarData: null,
        // 用户未邮件激活提示框
        userInactive: false,
        // 用户登出确认
        userSignout: false
    },
    boards: { // 板块信息
        loaded: false,
        lst: [], // 带层级的折叠列表
        rawLst: [], // 不带层级的平铺列表
        infoMap: {}, // 从服务器获取的信息
        exInfoMap: {} // 自行计算总结的信息
    },
    unread: 0,
    unreadAlerted: false,
    reset: () => {
        state.unread = 0
        state.unreadAlerted = false
        state.user = null
    },
    // 当前用户
    user: null,
    // 正在加载标记
    loading: 1,
    // 全局加载动画，应用于多重加载的情况，例如A页加载，计数器+1，A中有B组件，B再将计数器+1
    // 这样计数器归零的时候不再显示加载动画
    loadingGetKey,
    loadingInc: (route, key) => {
        if (key === loadingGetKey(route)) state.loading++
    },
    loadingDec: (route, key) => {
        if (key === loadingGetKey(route)) state.loading--
    },
    // 当前用户是否为未激活帐户
    isInactiveUser: function () {
        return state.getRole('user') === 'inactive_user'
    },
    // 获取用户角色（取当前最高的一个）
    getRole: (limit) => {
        let role = null
        let roles = [null, 'ban', 'inactive_user', 'user', 'superuser', 'admin']
        let rolesMap = {
            [state.misc.USER_GROUP.BAN]: 'ban',
            [state.misc.USER_GROUP.INACTIVE]: 'inactive_user',
            [state.misc.USER_GROUP.NORMAL]: 'user',
            [state.misc.USER_GROUP.SUPERUSER]: 'superuser',
            [state.misc.USER_GROUP.ADMIN]: 'admin'
        }

        if (state.user) {
            role = rolesMap[state.user.group]
        }

        let iCurrent = roles.indexOf(role)
        let iLimit = roles.indexOf(limit)
        if (iLimit === -1) return null
        return roles[(iCurrent > iLimit) ? iLimit : iCurrent]
    },
    // 用户在线数量
    userOnline: '?',
    // 初始加载完成
    initLoadDone: false,
    init: () => {
        ;
    }
}

export default state

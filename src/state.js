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
    test: {
        items: []
    },
    dialog: {
        topicManage: null,
        topicManageData: null,
        boardManage: null,
        boardManageData: null,
        userManage: null,
        userManageData: null,
        commentManage: null,
        commentManageData: null,
        userSetAvatar: false,
        userSetAvatarData: null,
        // 用户未邮件激活提示框
        userInactive: false
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
    user: null,
    loading: 1,
    loadingGetKey,
    loadingInc: (route, key) => {
        if (key === loadingGetKey(route)) state.loading++
    },
    loadingDec: (route, key) => {
        if (key === loadingGetKey(route)) state.loading--
    },
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
    userOnline: '?',
    initLoadDone: false,
    init: () => {
        ;
    }
}

export default state

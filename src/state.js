
// import tools from "./tools.js"

export default {
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
        TOPIC_STATE: { ... },
        TOPIC_STATE_TXT: { ... }
    },
    */
    msgs: [],
    test: {
        items: []
    },
    dialog: {
        topicManage: null,
        topicManageData: null
    },
    unread: 0,
    user: null,
    loading: 1,
    initLoadDone: false,
    init: () => {
        ;
    }
}

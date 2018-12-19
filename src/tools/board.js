import Color from 'color'
import store from '@/store/index'
import murmurhash from 'murmurhash'

$.boardColor = function (board) {
    if (board.color) {
        try {
            return Color(board.color).string()
        } catch (error) {
            try {
                let c = '#' + board.color
                return Color(c).string()
            } catch (error) {}
        }
    }
    let bgColor = murmurhash.v3(board.name).toString(16).slice(0, 6)
    return '#' + bgColor
}

$.lineStyle = function (board, key = 'border-left-color') {
    return { [key]: $.boardColor(board) }
}

$.lineStyleById = function (boardId, key = 'border-left-color') {
    let exInfo = $.getBoardExInfoById(boardId)
    if (exInfo) {
        return { [key]: exInfo.color }
    }
    return {}
}

$.getBoardInfoById = function (id) {
    // 因为要在 computed 中使用，所以不能为 async
    // if (!state.boards.loaded) await $.getBoardsInfo()
    return store.state.forum.infoMap[id]
}

$.getBoardExInfoById = function (id) {
    // if (!state.boards.loaded) await $.getBoardsInfo()
    return store.state.forum.exInfoMap[id]
}

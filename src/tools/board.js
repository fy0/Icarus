import Color from 'color'
import state from '@/state.js'
import api from '../netapi.js'
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

$.getBoardChainById = function (curBoardId, forceRefresh = false) {
    // 获取当前板块的所有父节点（包括自己）
    if (!state.boards.loaded) {
        return []
    }
    if (!forceRefresh) {
        let exi = state.boards.exInfoMap[curBoardId]
        if (exi) return exi.chain
        return []
    }
    let lst = [curBoardId]
    if (!curBoardId) return lst
    let infoMap = state.boards.infoMap
    if (!Object.keys(infoMap).length) return lst
    while (true) {
        let pid = infoMap[curBoardId].parent_id
        if (!pid) break
        lst.push(pid)
        curBoardId = pid
    }
    return lst
}

$.getBoardInfoById = function (id) {
    // 因为要在 computed 中使用，所以不能为 async
    // if (!state.boards.loaded) await $.getBoardsInfo()
    return state.boards.infoMap[id]
}

$.getBoardExInfoById = function (id) {
    // if (!state.boards.loaded) await $.getBoardsInfo()
    return state.boards.exInfoMap[id]
}

$.getBoardsInfo = async function (forceRefresh = false) {
    if (state.boards.loaded && (!forceRefresh)) return
    let boards = await api.board.list({
        order: 'parent_id.desc,weight.desc,time.asc' // 权重从高到低，时间从先到后
    })

    if (boards.code === api.retcode.SUCCESS) {
        let lst = []
        let infoMap = {}

        for (let i of boards.data.items) {
            let subboards = []
            for (let j of boards.data.items) {
                if (j.parent_id === i.id) subboards.push(j)
            }

            infoMap[i.id] = i
            if (!i.parent_id) {
                lst.push(i)
            }

            let color = $.boardColor(i)
            state.boards.exInfoMap[i.id] = {
                'subboards': subboards,
                'subboardsAll': [],
                'color': color,
                // darken 10% when hover
                'colorHover': Color(color).darken(0.1).string()
            }
        }

        state.boards.lst = lst
        state.boards.rawLst = boards.data.items
        state.boards.infoMap = infoMap

        state.boards.loaded = true
        for (let i of boards.data.items) {
            let exInfo = state.boards.exInfoMap[i.id]
            // 构造 subboardsAll
            let func = (subboards) => {
                for (let j of subboards) {
                    exInfo.subboardsAll.push(j)
                    func(state.boards.exInfoMap[j.id].subboards)
                }
            }
            func(exInfo.subboards)
            // 构造 chain
            exInfo.chain = $.getBoardChainById(i.id, true)
        }
    }
}

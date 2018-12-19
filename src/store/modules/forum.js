import Color from 'color'
import api from '../../netapi.js'

export default {
    namespaced: true,

    state: {
        // 暂时没有能力修改这些了
        loaded: false,
        lst: [], // 带层级的折叠列表
        rawLst: [], // 不带层级的平铺列表
        infoMap: {}, // 从服务器获取的信息
        exInfoMap: {} // 自行计算总结的信息
    },
    getters: {
        isNewSite: (state) => state.rawLst.length === 0
    },
    mutations: {
    },
    actions: {
        fetchBoardChain ({ state }, { boardId, forceRefresh = false }) {
            // 获取当前板块的所有父节点（包括自己）
            if (!state.loaded) {
                return []
            }
            if (!forceRefresh) {
                let exi = state.exInfoMap[boardId]
                if (exi) return exi.chain
                return []
            }
            let lst = [boardId]
            if (!boardId) return lst
            let infoMap = state.infoMap
            if (!Object.keys(infoMap).length) return lst
            while (true) {
                let pid = infoMap[boardId].parent_id
                if (!pid) break
                lst.push(pid)
                boardId = pid
            }
            state.exInfoMap[boardId].chain = lst
        },
        async load ({ state, dispatch }, forceRefresh = false) {
            if (state.loaded && (!forceRefresh)) return
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
                    state.exInfoMap[i.id] = {
                        'subboards': subboards,
                        'subboardsAll': [],
                        'color': color,
                        // darken 10% when hover
                        'colorHover': Color(color).darken(0.1).string()
                    }
                }

                state.lst = lst
                state.rawLst = boards.data.items
                state.infoMap = infoMap

                state.loaded = true
                for (let i of boards.data.items) {
                    let exInfo = state.exInfoMap[i.id]
                    // 构造 subboardsAll
                    let func = (subboards) => {
                        for (let j of subboards) {
                            exInfo.subboardsAll.push(j)
                            func(state.exInfoMap[j.id].subboards)
                        }
                    }
                    func(exInfo.subboards)

                    // 构造 chain
                    dispatch('fetchBoardChain', { boardId: i.id })
                }
            }
        }
    }
}

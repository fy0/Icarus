import Color from 'color'

export const state = () => ({
    // 暂时没有能力修改这些了
    loaded: false,
    lst: [], // 带层级的折叠列表
    rawLst: [], // 不带层级的平铺列表
    infoMap: {}, // 从服务器获取的信息
    exInfoMap: {} // 自行计算总结的信息
})

export const getters = {
    isSiteNew: (state) => state.rawLst.length === 0
}

export const mutations = {
    SET_BOARD_MANY_INFO (state, { lst, rawLst, infoMap }) {
        state.lst = lst
        state.rawLst = rawLst
        state.infoMap = infoMap
    },
    SET_BOARD_EXINFO (state, { id, data }) {
        state.exInfoMap[id] = data
    },
    SET_BOARD_EXINFO_CHAIN (state, { id, data }) {
        if (!state.exInfoMap[id]) {
            state.exInfoMap[id] = {}
        }
        state.exInfoMap[id].chain = data
    },
    SET_LOADED (state, val) {
        state.loaded = val
    }
}

export const actions = {
    fetchBoardChain ({ state, commit }, { boardId }) {
        // 获取当前板块的所有父节点（包括自己）
        if (!state.loaded) {
            return []
        }

        const theLst = ((boardId) => {
            const lst = [boardId]
            if (!boardId) return lst
            const infoMap = state.infoMap
            if (!Object.keys(infoMap).length) return lst
            while (true) {
                if (!infoMap[boardId]) {
                    // 板块父级因权限原因不可见，斩断计算链就行了
                    return []
                }
                const pid = infoMap[boardId].parent_id
                if (!pid) break
                lst.push(pid)
                boardId = pid
            }
            return lst
        })(boardId)

        commit('SET_BOARD_EXINFO_CHAIN', { id: boardId, data: theLst })
    },
    async load ({ state, commit, dispatch }, forceRefresh = false) {
        if (state.loaded && (!forceRefresh)) return
        const boards = await this.$api.board.list({
            order: 'parent_id.desc,weight.desc,time.asc' // 权重从高到低，时间从先到后
        })

        if (boards.code === this.$api.retcode.SUCCESS) {
            const lst = []
            const infoMap = {}

            for (const i of boards.data.items) {
                const subboards = []
                for (const j of boards.data.items) {
                    if (j.parent_id === i.id) subboards.push(j)
                }

                infoMap[i.id] = i
                if (!i.parent_id) {
                    lst.push(i)
                }

                const color = $.boardColor(i)
                commit('SET_BOARD_EXINFO', {
                    id: i.id,
                    data: {
                        subboards: subboards,
                        subboardsAll: [],
                        color: color,
                        // darken 10% when hover
                        colorHover: Color(color).darken(0.1).string()
                    }
                })
            }

            commit('SET_BOARD_MANY_INFO', { lst, infoMap, rawLst: boards.data.items })
            commit('SET_LOADED', true)

            for (const i of boards.data.items) {
                const exInfo = state.exInfoMap[i.id]
                // 构造 subboardsAll
                const func = (subboards) => {
                    for (const j of subboards) {
                        exInfo.subboardsAll.push(j)
                        func(state.exInfoMap[j.id].subboards)
                    }
                }
                func(exInfo.subboards)

                // 构造 chain
                dispatch('fetchBoardChain', { boardId: i.id })
            }

            dispatch('fetchBoardChain', { boardId: undefined })
        }
    }
}

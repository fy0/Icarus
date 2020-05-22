import Color from 'color'
import { retcode } from 'slim-tools'
import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { $api } from '../plugins/api'
import { boardColor } from '@/utils/style'

@Module({
  // name: 'forum',
  stateFactory: true,
  namespaced: true
})
export default class ForumModule extends VuexModule {
  loaded = false
  lst = [] // 带层级的折叠列表
  rawLst = [] // 不带层级的平铺列表
  infoMap: any = {} // 从服务器获取的信息
  exInfoMap: any = {} // 自行计算总结的信息

  get isSiteNew () {
    return this.rawLst.length === 0
  }

  @Mutation
  SET_BOARD_MANY_INFO ({ lst, rawLst, infoMap }: any) {
    this.lst = lst
    this.rawLst = rawLst
    this.infoMap = infoMap
  }

  @Mutation
  SET_BOARD_EXINFO ({ id, data }: any) {
    this.exInfoMap[id] = data
  }

  @Mutation
  SET_BOARD_EXINFO_CHAIN ({ id, data }: any) {
    if (!this.exInfoMap[id]) {
      this.exInfoMap[id] = {}
    }
    this.exInfoMap[id].chain = data
  }

  @Mutation
  SET_LOADED (val: boolean) {
    this.loaded = val
  }

  @Action
  fetchBoardChain ({ boardId }: any) {
    // 获取当前板块的所有父节点（包括自己）
    if (!this.loaded) {
      return []
    }

    const theLst = ((boardId) => {
      const lst = [boardId]
      if (!boardId) return lst
      const infoMap = this.infoMap
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

    this.context.commit('SET_BOARD_EXINFO_CHAIN', { id: boardId, data: theLst })
  }

  @Action({ rawError: true })
  async load (forceRefresh = false) {
    const { commit, dispatch } = this.context
    if (this.loaded && (!forceRefresh)) return

    const boards = await $api.board.list({
      order: 'parent_id.desc,weight.desc,time.asc' // 权重从高到低，时间从先到后
    }, 1)

    if (boards.code === retcode.SUCCESS) {
      const lst = []
      const infoMap: any = {}

      if (!boards.data) return
      for (const i of boards.data.items) {
        const subboards = []
        for (const j of boards.data.items) {
          if (j.parent_id === i.id) subboards.push(j)
        }

        infoMap[i.id] = i
        if (!i.parent_id) {
          lst.push(i)
        }

        const color = boardColor(i)
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
        const exInfo = this.exInfoMap[i.id]
        // 构造 subboardsAll
        const func = (subboards: any) => {
          for (const j of subboards) {
            exInfo.subboardsAll.push(j)
            func(this.exInfoMap[j.id].subboards)
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

<template>
  <admin-base>
    <h3 class="ic-header">板块管理</h3>

    <table class="pure-table pure-table-horizontal" style="width: 100%">
        <thead>
            <tr>
                <th>#</th>
                <th style="min-width:4.1em">名称</th>
                <th>介绍</th>
                <th>父级</th>
                <th style="min-width:2.1em">权重</th>
                <th style="min-width:2.1em">状态</th>
                <th style="min-width:141px">操作</th>
            </tr>
        </thead>

        <tbody>
            <tr class="board-tr" v-for="(i, _) in boardInfo.items" :key="_">
                <td>{{_+1}}</td>
                <td>{{i.name}}</td>
                <td>{{i.brief}}</td>
                <td>{{boardsInfoDict[i.parent_id] ? boardsInfoDict[i.parent_id].name : '无'}}</td>
                <td>{{i.weight}}</td>
                <td>{{$misc.POST_STATE_TXT[i.state]}}</td>
                <td>
                    <a href="javascript:void(0)" @click="$dialogs.setBoardManage(true, i)">编辑</a>
                </td>
            </tr>
        </tbody>
    </table>
    <div class="board-add">
        <div class="board_name">
            <input type="text" class="ic-input" v-model="boardNewInfo.name" placeholder="板块名">
        </div>
        <div class="board_brief">
            <input class="ic-input" name="board_brief" v-model="boardNewInfo.brief" type="text" placeholder="简介">
        </div>
        <div class="btn">
            <button class="ic-btn success" @click="boardNew">新建板块</button>
        </div>
    </div>
    <dialog-board-manage />
  </admin-base>
</template>

<style scoped>
.board-add {
  display: flex;
  margin-top: 5px;
  justify-content: space-between;
}

.board-add > .board_name {
  flex: 6 0 0%;
  margin-right: 10px;
}

.board-add > .board_brief {
  flex: 13 0 0%;
  margin-right: 10px;
}

.board-add > .btn {
  flex: 5 0 0%;
}

.board-add > div > * {
  display: block;
  height: 100%;
  width: 100%;
}

.board-tr > td {
  overflow: hidden;
}

table {
  table-layout: fixed;
  word-break: break-all;
  word-wrap: break-word;
}
</style>

<script>
import { retcode } from 'slim-tools'
import AdminBase from '../base/base.vue'
import DialogBoardManage from '@/components/dialogs/board-manage.vue'

export default {
  data () {
    return {
      boardNewInfo: {
        name: '',
        brief: ''
      },
      boardInfo: {},
      boardsInfoDict: {}
    }
  },
  head () {
    return {
      title: '板块管理 - 管理界面',
      meta: [
        { hid: 'description', name: 'description', content: '板块管理 - 管理界面' }
      ]
    }
  },
  methods: {
    boardNew: async function () {
      let ret = await this.$api.board.new(this.boardNewInfo)
      this.$message.byCode(ret.code)
      if (ret.code === retcode.SUCCESS) {
        this.fetchData()
      }
    },
    fetchData: async function () {
      let ret = await this.$api.board.list({
        order: 'weight.desc,time.asc',
        loadfk: { 'user_id': null }
        // select: 'id, time, user_id, board_id, title, state',
      }, 1, { role: this.$user.forumAdminRole })

      if (ret.code === retcode.SUCCESS) {
        this.boardInfo = ret.data
        for (let i of ret.data.items) {
          this.boardsInfoDict[i.id] = i
        }
      } else {
        // this.$message.byCode(ret.code)
      }
    }
  },
  created: async function () {
    this.$store.commit('LOADING_INC', 1)
    await this.fetchData()
    this.$store.commit('LOADING_DEC', 1)
  },
  components: {
    AdminBase,
    DialogBoardManage
  }
}
</script>

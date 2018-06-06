<template>
<admin-base>
    <div v-title>版块管理 - 管理界面 - {{state.config.title}}</div>
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
                <td>{{state.misc.POST_STATE_TXT[i.state]}}</td>
                <td>
                    <a href="javascript:void(0)" @click="setBoardManage(i)">编辑</a>
                </td>
            </tr>
        </tbody>
    </table>
    <div class="board-add">
        <div class="board_name">
            <input type="text" v-model="boardNewInfo.name" placeholder="板块名">
        </div>
        <div class="board_brief">
            <input name="board_brief" v-model="boardNewInfo.brief" type="text" placeholder="简介">
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
    border: 0;
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
import api from '@/netapi.js'
import state from '@/state.js'
import AdminBase from '../base/base.vue'
import DialogBoardManage from '../../utils/dialogs/board-manage.vue'

export default {
    data () {
        return {
            state,
            boardNewInfo: {
                name: '',
                brief: ''
            },
            boardInfo: {},
            boardsInfoDict: {}
        }
    },
    methods: {
        setBoardManage: function (board) {
            state.dialog.boardManageData = board
            state.dialog.boardManage = true
        },
        boardNew: async function () {
            let ret = await api.board.new(this.boardNewInfo, 'admin')
            $.message_by_code(ret.code)
            if (ret.code === api.retcode.SUCCESS) {
                this.fetchData()
            }
        },
        fetchData: async function () {
            let ret = await api.board.list({
                order: 'weight.desc,time.asc',
                loadfk: {'user_id': null}
                // select: 'id, time, user_id, board_id, title, state',
            }, 1, null, 'admin')

            if (ret.code === api.retcode.SUCCESS) {
                this.boardInfo = ret.data
                for (let i of ret.data.items) {
                    this.boardsInfoDict[i.id] = i
                }
            } else {
                $.message_by_code(ret.code)
            }
        }
    },
    created: async function () {
        let key = state.loadingGetKey(this.$route)
        this.state.loadingInc(this.$route, key)
        await this.fetchData()
        this.state.loadingDec(this.$route, key)
    },
    components: {
        AdminBase,
        DialogBoardManage
    }
}
</script>

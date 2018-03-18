<template>
<admin-base>
    <div v-title>版块管理 - 管理界面 - {{state.config.title}}</div>
    <table class="pure-table pure-table-horizontal" style="width: 100%">
        <thead>
            <tr>
                <th>#</th>
                <th style="min-width:4.1em">名称</th>
                <th>介绍</th>
                <th style="min-width:2.1em">权重</th>
                <th style="min-width:2.1em">状态</th>
                <th style="min-width:141px">操作</th>
            </tr>
        </thead>

        <tbody>
            <tr v-for="i, _ in boardInfo.items">
                <td>{{_+1}}</td>
                <td>{{i.name}}</td>
                <td>{{i.brief}}</td>
                <td>{{i.weight}}</td>
                <td>{{state.misc.BOARD_STATE_TXT[i.state]}}</td>
                <td>
                    <a item-id="${i.id}" class="btn-edit pure-u-12-24 pure-button button-secondary">编辑</a>
                </td>
            </tr>
        </tbody>
    </table>
    <div class="board-add">
        <div class="board_name">
            <input type="text" v-model="boardNewInfo.name" placeholder="版块名">
        </div>
        <div class="board_brief">
            <input name="board_brief" v-model="boardNewInfo.brief" type="text" placeholder="简介">
        </div>
        <div class="btn">
            <button class="ic-btn click blue" @click="boardNew">新建版块</button>
        </div>
    </div>
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
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import AdminBase from '../base/base.vue'

export default {
    data () {
        return {
            state,
            boardNewInfo: {
                name: '',
                brief: ''
            },
            boardInfo: {}
        }
    },
    methods: {
        reloadInfo: async function () {
        },
        boardNew: async function () {
            let ret = await api.board.new(this.boardNewInfo)
            $.message_by_code(ret.code)
            if (ret.code === api.retcode.SUCCESS) {
                this.reloadInfo()
            }
        },
        fetchData: async function () {
            let ret = await api.board.list({
                order: 'weight.desc,time.desc'
                // select: 'id, time, user_id, board_id, title, state',
            }, 1, null, 'admin')

            if (ret.code === api.retcode.SUCCESS) {
                this.boardInfo = ret.data
            } else {
                $.message_by_code(ret.code)
            }
        }
    },
    created: async function () {
        this.state.loading++
        await this.fetchData()
        this.state.loading--
    },
    components: {
        AdminBase
    }
}
</script>

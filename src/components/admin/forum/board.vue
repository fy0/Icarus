<template>
<admin-base>
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
            <tr v-for="i in test">
                <td>{{i.id}}</td>
                <td>{{i.title}}</td>
                <td>{{i.brief}}</td>
                <td>{{i.weight}}</td>
                <td>{{i.state}}</td>
                <td>
                    <div class="pure-g">
                        <a item-id="${i.id}" class="btn-edit pure-u-12-24 pure-button button-secondary">编辑</a>
                        <a item-id="${i.id}" class="btn-del pure-u-12-24 pure-button button-error">删除</a>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
    <div class="board-add">
        <div class="board_title">
            <input type="text" placeholder="版块名">
        </div>
        <div class="board_brief">
            <input name="board_brief" type="text" placeholder="简介">
        </div>
        <div class="btn">
            <button class="ic-btn click blue">新建版块</button>
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

.board-add > .board_title {
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
import AdminBase from '../base/base.vue'

export default {
    data () {
        return {
            test: [
                {
                    id: 1,
                    title: '水区',
                    brief: '社区的哪一个大佬我没有见过？我跟他们谈笑风生！',
                    weight: 0,
                    state: 10
                },
                {
                    id: 2,
                    title: '水区',
                    brief: '社区的哪一个大佬我没有见过？我跟他们谈笑风生！',
                    weight: 0,
                    state: 10
                }
            ]
        }
    },
    components: {
        AdminBase
    }
}
</script>

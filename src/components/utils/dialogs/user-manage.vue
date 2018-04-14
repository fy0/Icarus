<template>
<mu-dialog :open="state.dialog.userManage" :title="`对用户 ${user.nickname} 进行管理操作`" @close="close" scrollable>
    <div class="topic-manage-item" style="margin-top: 30px;">
        <span class="label">ID</span>
        <div class="right">{{user.id}}</div>
    </div>
    <div class="topic-manage-item">
        <span class="label">Email</span>
        <div class="right">
            <div>{{user.email}}</div>
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">昵称</span>
        <div class="right">
            <div>{{user.nickname}}</div>
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">注册时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.reg_time" />
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">简介</span>
        <div class="right">
            <mu-text-field v-model="user.biology" :maxLength="255"/>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">上级板块</span>
        <div class="right">
            <mu-dropDown-menu :labelClass="'no-left-padding'" :underlineClass="'no-left-padding'" :value="value" @change="handleChange">
                <mu-menu-item value="1" title="星期一"/>
                <mu-menu-item value="2" title="星期二"/>
                <mu-menu-item value="3" title="星期三"/>
                <mu-menu-item value="4" title="星期四"/>
                <mu-menu-item value="5" title="星期五"/>
                <mu-menu-item value="6" title="星期六"/>
                <mu-menu-item value="7" title="星期日"/>
            </mu-dropDown-menu>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">状态</span>
        <div class="right" style="display: flex">
            <mu-radio name="state" :label="i" :nativeValue="j.toString()" v-model="user.state" v-for="i, j in state.misc.POST_STATE_TXT" :key="j" class="demo-radio"/>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">用户组</span>
        <div class="right" style="display: flex">
            <mu-radio name="group" :label="i" :nativeValue="j.toString()" v-model="user.group" v-for="i, j in state.misc.USER_GROUP_TXT" :key="j" class="demo-radio"/>
        </div>
    </div>

    <mu-flat-button slot="actions" @click="close" primary label="取消"/>
    <mu-flat-button slot="actions" primary @click="ok" label="确定"/>
</mu-dialog>
</template>

<style>
.no-left-padding {
    padding-left: 0;
    margin-left: 0;
}
</style>


<style scoped>
.topic-manage-item {
    display: flex;
    align-items: baseline;
    min-height: 56px;
}

.topic-manage-item > .label {
    flex: 1 0 0;
}

.topic-manage-item > .right {
    flex: 4 0 0;
}

.demo-radio {
    margin-right: 15px;
}

.demo-slider {
    margin-bottom: 0;
}

.hl {
    color: red
}
</style>

<script>
import state from '@/state.js'
import api from '@/netapi.js'

export default {
    data () {
        return {
            state,
            user: {name: ''},
            save: {},
            value: '1'
        }
    },
    methods: {
        handleChange (value) {
            this.value = value
        },
        ok: async function () {
            let data = {}
            let keys = new Set(['brief', 'category', 'desc', 'name', 'state', 'weight'])
            for (let i of Object.keys(this.board)) {
                if (keys.has(i)) {
                    // 注意 post 上去的时候 null 会变成 'null'
                    // 所以直接移除了
                    if (this.board[i] !== null) {
                        data[i] = this.board[i]
                    }
                }
            }

            if (data.state) data.state = Number(data.state)
            if (data.weight) data.weight = Number(data.weight)

            let ret = await api.board.set({id: this.board.id}, data, 'admin')
            if (ret.code === 0) $.message_success('板块信息设置成功')
            else $.message_by_code(ret.code)

            state.dialog.userManage = null
        },
        close () {
            state.dialog.userManage = null
        }
    },
    watch: {
        'state.dialog.userManage': async function (val) {
            if (val) {
                let info = await api.user.get({id: state.dialog.userManageData.id}, 'admin')
                if (info.code === api.retcode.SUCCESS) {
                    this.user = info.data
                    this.user.state = this.user.state.toString()
                } else {
                    $.message_by_code(info.code)
                }
            }
        }
    }
}
</script>

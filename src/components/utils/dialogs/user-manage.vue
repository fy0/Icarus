<template>
<ic-dialog v-model="state.dialog.userManage" :title="`对用户 ${user.nickname} 进行管理操作`" @close="close" scrollable>
    <div class="manage-form-item" style="margin-top: 30px;">
        <span class="label">ID</span>
        <div class="right">{{user.id}}</div>
    </div>
    <div class="manage-form-item">
        <span class="label">Email</span>
        <div class="right">
            <div>{{user.email}}</div>
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">昵称</span>
        <div class="right">
            <div>{{user.nickname}}</div>
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">注册时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.time" />
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">最后登录时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.key_time" />
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">简介</span>
        <div class="right">
            <input type="text" class="ic-input" v-model="user.biology" />
        </div>
    </div>
    <div class="manage-form-item" style="align-items: center">
        <span class="label">状态</span>
        <div class="right" style="display: flex">
            <span style="margin-right: 10px" v-for="(i, j) in state.misc.POST_STATE_TXT" :key="j">
                <label :for="'radio-state-'+i">
                    <input class="ic-input" type="radio" name="state" :value="j" :id="'radio-state-'+i" v-model="user.state" />
                    <span>{{i}}</span>
                </label>
            </span>
        </div>
    </div>
    <div class="manage-form-item" style="align-items: center">
        <span class="label">用户组</span>
        <div class="right" style="display: flex">
            <span style="margin-right: 10px" v-for="(i, j) in state.misc.USER_GROUP_TXT" :key="j">
                <label :for="'radio-group-'+i">
                    <input class="ic-input" type="radio" name="group" :value="j" :id="'radio-group-'+i" v-model="user.group" />
                    <span>{{i}}</span>
                </label>
            </span>
        </div>
    </div>

    <div class="bottom">
        <span class="ic-btn primary" @click="ok">确定</span>
        <span class="ic-btn secondary" @click="close">取消</span>
    </div>
</ic-dialog>
</template>

<style lang="scss" scoped>
.bottom {
    text-align: right;

    .ic-btn {
        padding-left: 30px;
        padding-right: 30px;
        margin-left: 10px;
    }
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
            save: {}
        }
    },
    methods: {
        ok: async function () {
            let data = $.objDiff(this.user, this.save)
            if (data.state) data.state = Number(data.state)
            if (data.group) data.group = Number(data.group)

            let ret = await api.user.set({id: this.user.id}, data, 'admin')
            if (ret.code === 0) {
                if (state.dialog.userManageData) {
                    _.assign(state.dialog.userManageData, data)
                }
                $.message_success('用户信息设置成功')
            } else $.message_by_code(ret.code)

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
                    this.user.group = this.user.group.toString()
                    this.save = _.clone(this.user)
                } else {
                    $.message_by_code(info.code)
                }
            }
        }
    }
}
</script>

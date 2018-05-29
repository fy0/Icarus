<template>
<ic-dialog v-if="state.dialog.commentManage">
    123
</ic-dialog>
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
import ICDialog from './_dialog.vue'

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
    components: {
        'ic-dialog': ICDialog
    },
    watch: {
        'state.dialog.commentManage': async function (val) {
            // if (val) {
            //     let info = await api.user.get({id: state.dialog.userManageData.id}, 'admin')
            //     if (info.code === api.retcode.SUCCESS) {
            //         this.user = info.data
            //         this.user.state = this.user.state.toString()
            //         this.user.group = this.user.group.toString()
            //         this.save = _.clone(this.user)
            //     } else {
            //         $.message_by_code(info.code)
            //     }
            // }
        }
    }
}
</script>

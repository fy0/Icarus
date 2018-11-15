<template>
<span class="detail" style="margin-left: .5em">
    <template v-if="getOP(item) === MOP.POST_STATE_CHANGE">
        <span v-if="simple">-> {{postStateTxt(item.value[1])}}</span>
        <span v-else>({{item.value.map(postStateTxt).join(' -> ')}})</span>
    </template>
    <template v-else-if="getOP(item) === MOP.TOPIC_AWESOME_CHANGE">
        <span v-if="item.value[1] === 0">-> 撤销</span>
        <span v-else></span>
    </template>
    <span v-else-if="getOP(item) === MOP.POST_VISIBLE_CHANGE">({{item.value.map(postVisibleTxt).join(' -> ')}})</span>
    <span v-else-if="getOP(item) === MOP.USER_GROUP_CHANGE">({{item.value.map(postGroupTxt).join(' -> ')}})</span>
    <span v-else-if="simpleChangeOP.indexOf(getOP(item)) != -1">({{item.value.join(' -> ')}})</span>
</span>
</template>

<style scoped>
</style>

<script>
import state from '@/state.js'

export default {
    props: {
        item: {},
        simple: false
    },
    data () {
        return {
            state,
            MOP: state.misc.MANAGE_OPERATION,
            MOPT: state.misc.MANAGE_OPERATION_TXT
        }
    },
    computed: {
        simpleChangeOP: function () {
            let MOP = this.MOP
            return [
                MOP.POST_TITLE_CHANGE,
                MOP.USER_CREDIT_CHANGE,
                MOP.USER_REPUTE_CHANGE,
                MOP.USER_EXP_CHANGE,
                MOP.USER_NICKNAME_CHANGE,
                MOP.TOPIC_BOARD_MOVE,
                MOP.TOPIC_AWESOME_CHANGE,
                MOP.TOPIC_STICKY_WEIGHT_CHANGE
            ]
        }
    },
    methods: {
        postStateTxt: function (postState) {
            return state.misc.POST_STATE_TXT[postState]
        },
        postVisibleTxt: function (i) {
            return state.misc.POST_VISIBLE_TXT[i]
        },
        postGroupTxt: function (i) {
            return state.misc.USER_GROUP_TXT[i]
        },
        getOP: function (item) {
            return item.operation || item.op
        }
    }
}
</script>

<template>
    <mu-dialog :open="state.dialog.topicManage" :title="`对文章 ${topic.title} 进行管理操作`" @close="close">
        <div class="topic-manage-item">
            <span class="label">置顶</span>
            <div class="right">
                <mu-radio name="sticky" :label="i.toString()" :nativeValue="i.toString()" v-model="vSticky" class="demo-radio" v-for="i in [0, 1, 2, 3, 4, 5]" :key="i" />
            </div>
        </div>
        <div class="topic-manage-item">
            <span class="label">提升/下沉</span>
            <div class="right" style="display: flex; align-items: center;">
                <mu-slider v-model="vWeight" :step="1" :min="-100" :max="100" class="demo-slider"/>
                <span style="min-width: 40px; text-align: center">{{vWeight}}</span>
            </div>
        </div>
        <div class="topic-manage-item">
            <span class="label">评分</span>
            <div class="right" style="display: flex; align-items: center;">
                <mu-slider v-model="vCredit" :step="1" :min="-100" :max="100"  class="demo-slider"/>
                <span style="min-width: 40px; text-align: center">{{vCredit}}</span>
            </div>
        </div>
        <div class="topic-manage-item">
            <span class="label">声望</span>
            <div class="right" style="display: flex; align-items: center;">
                <mu-slider v-model="vReputation" :step="1" :min="-100" :max="100"  class="demo-slider"/>
                <span style="min-width: 40px; text-align: center">{{vReputation}}</span>
            </div>
        </div>
        <div class="topic-manage-item">
            <span class="label">状态</span>
            <div class="right">
                <mu-radio name="state" :label="i" :nativeValue="j.toString()" v-model="vState" v-for="i, j in state.misc.TOPIC_STATE_TXT" :key="j" class="demo-radio"/>
            </div>
        </div>
        <div class="topic-manage-item">
            <span class="label">精华</span>
            <div class="right">
                <mu-switch v-model="vAwesome" class="demo-switch" />
            </div>
        </div>

        <mu-flat-button slot="actions" @click="close" primary label="取消"/>
        <mu-flat-button slot="actions" primary @click="close" label="确定"/>
    </mu-dialog>
</template>

<style scoped>
.topic-manage-item {
    display: flex;
    align-items: center;
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
</style>

<script>
import state from '@/state.js'

export default {
    data () {
        return {
            state,
            vSticky: '0',
            vWeight: 0,
            vCredit: 0,
            vState: '0',
            vReputation: 0,
            vAwesome: false
        }
    },
    computed: {
        topic: function () {
            let ret = state.dialog.topicManageData
            if (!ret) return {title: ''}
            return ret
        }
    },
    methods: {
        close () {
            state.dialog.topicManage = null
        }
    }
}
</script>

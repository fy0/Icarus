<template>
<mu-dialog :open="state.dialog.boardManage" :title="`对板块 ${board.name} 进行管理操作`" @close="close" scrollable>
    <div class="topic-manage-item" style="margin-top: 30px;">
        <span class="label">ID</span>
        <div class="right">{{board.id}}</div>
    </div>
    <div class="topic-manage-item">
        <span class="label">创建者</span>
        <div class="right">
            <user-link v-if="board.user_id" :user="board.user_id" />
            <div v-else>系统</div>
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">板块名</span>
        <div class="right">
            <mu-text-field v-model="board.name" :maxLength="30"/>
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">简介</span>
        <div class="right">
            <mu-text-field v-model="board.brief" :maxLength="255"/>
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">权重</span>
        <div class="right">
            <mu-text-field type="number" v-model="board.weight" />
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">色彩</span>
        <div class="right">
            <mu-text-field hintText="需为十六进制颜色" v-model="board.color" :maxLength="8"/>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">上级板块</span>
        <div class="right">
            <multiselect v-model="board.parent_id" :allow-empty="true" :options="boardList" :custom-label="getSelectOptionName" placeholder="选择一个板块" style="z-index: 2; width: 85%;" open-direction="bottom"></multiselect>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">状态</span>
        <div class="right" style="display: flex">
            <mu-radio name="state" :label="i" :nativeValue="j.toString()" v-model="board.state" v-for="i, j in state.misc.POST_STATE_TXT" :key="j" class="demo-radio"/>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">可见性</span>
        <div class="right" style="display: flex">
            <mu-radio name="visible" :label="i" :nativeValue="j.toString()" v-model="board.visible" v-for="i, j in state.misc.POST_VISIBLE_TXT" :key="j" class="demo-radio"/>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">公告</span>
        <div class="right">
            <mu-text-field hintText="" multiLine :rows="3" v-model="board.desc" fullWidth :maxLength="1024"/>
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
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

export default {
    data () {
        return {
            state,
            value: 1,
            save: {},
            board: {name: ''},
            boardList: [],
            boardsInfoDict: {}
        }
    },
    computed: {
    },
    methods: {
        getSelectOptionName (id) {
            if (!this.boardsInfoDict[id]) return '无'
            let { name, brief } = this.boardsInfoDict[id]
            return `${name} — [${brief}]`
        },
        handleChange (value) {
            this.value = value
        },
        ok: async function () {
            let data = $.objDiff(this.board, this.save)
            if (data.state) data.state = Number(data.state)
            if (data.weight) data.weight = Number(data.weight)
            if (data.visible) data.visible = Number(data.visible)

            let keys = new Set(['brief', 'category', 'desc', 'name', 'state', 'weight', 'color', 'parent_id'])
            let ret = await api.board.set({id: this.board.id}, data, 'admin', keys)

            if (ret.code === 0) {
                if (state.dialog.boardManageData) {
                    _.assign(state.dialog.boardManageData, data)
                }
                $.message_success('板块信息设置成功')
            } else $.message_by_code(ret.code)

            state.dialog.boardManage = null
        },
        close () {
            state.dialog.boardManage = null
        }
    },
    watch: {
        'state.dialog.boardManage': async function (val) {
            if (val) {
                let info = await api.board.get({
                    id: state.dialog.boardManageData.id,
                    loadfk: {'user_id': null}
                }, 'admin')
                if (info.code === api.retcode.SUCCESS) {
                    this.board = info.data
                    this.board.state = this.board.state.toString()
                    this.save = _.clone(this.board)

                    let ret = await api.board.list({
                        order: 'weight.desc,time.asc'
                    }, 1, null, 'admin')
                    if (ret.code === api.retcode.SUCCESS) {
                        // vue-select 目前不允许写 null，要再等一等
                        this.boardList = []
                        this.boardsInfoDict = {}
                        for (let i of ret.data.items) {
                            if (i.id !== this.board.id) {
                                this.boardList.push(i.id)
                                this.boardsInfoDict[i.id] = i
                            }
                        }
                    }
                } else {
                    $.message_by_code(info.code)
                }
            }
        }
    },
    components: {
        Multiselect
    }
}
</script>

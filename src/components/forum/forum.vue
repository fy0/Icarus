<template>
<div class="ic-container forum-box">
    <top-btns></top-btns>
    <div id="board-list">
        <div class="board-item" v-for="i, _ in boardInfo.items">
            <div class="title">
                <h2><router-link :to="{ name: 'forum_board', params: {id: i.id} }">{{i.name}}</router-link></h2>
                <p>{{i.brief}}</p>
            </div>
            <div class="detail ic-xs-hidden">
                <div class="count">
                    <span class="tip">24h</span>
                    <p class="num">1</p>
                    <p class="txt">主题</p>
                </div>
                <div class="count">
                    <span class="tip">24h</span>
                    <p class="num">2</p>
                    <p class="txt">回复</p>
                </div>
                <div class="recent ic-xs-hidden ic-sm-hidden">
                    <span class="line"></span>
                    <strong><a href="#">root</a></strong>
                    <div class="post-content">前三十个文本</div>
                    <a href="#">...</a>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>

</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import '@/assets/css/forum.css'
import TopBtns from './topbtns.vue'

export default {
    data () {
        return {
            state,
            boardInfo: {}
        }
    },
    components: {
        TopBtns
    },
    beforeRouteEnter: async (to, from, next) => {
        let ret = await api.board.list()

        if (ret.code === api.retcode.SUCCESS) {
            return next(vm => {
                vm.boardInfo = ret.data
            })
        }

        $.message_by_code(ret.code)
        return next('/')
    },
    beforeRouteUpdate: async function (to, from, next) {
        let ret = await api.board.list()

        if (ret.code === api.retcode.SUCCESS) {
            this.boardInfo = ret.data
            return next()
        }

        $.message_by_code(ret.code)
        return next('/')
    }
}
</script>

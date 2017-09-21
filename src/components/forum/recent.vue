<template>
<div class="ic-container forum-box">
    <top-btns></top-btns>
    <div id="board-list">
        <div class="board-item" v-for="i in [1,2]">
            <div class="title" style="flex: 13 0 0%">
                <h2><a href="#">AAAA</a></h2>
                <p><a href="/user/root">root</a> 发布于 <time timestamp="1446111343">2年前</time></p>
            </div>
            <div class="detail ic-xs-hidden" style="flex: 11 0 0%">
                <div class="count">
                    <p class="board"><a href="/board/1">谈笑风生</a></p>
                    <p class="txt">版块</p>
                </div>
                <div class="count">
                    <p class="num">1</p>
                    <p class="txt">点击</p>
                </div>
                <div class="count">
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
import '@/assets/css/forum.css'
import TopBtns from './topbtns.vue'

export default {
    data () {
        return {
        }
    },
    components: {
        TopBtns
    }
}
</script>

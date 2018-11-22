<template>
<div class="ic-container">
    <div v-title>搜索 - {{state.config.title}}</div>
    <div>以下为“abc”的搜索结果，共123条</div>
    <div class="results">
        <div class="item">
            <h3 class="title">测试一下</h3>
            <div class="info">
                <span class="link">http://localhost:8080/search</span>
                <!-- <span>1234个回复，5678次查看</span> -->
            </div>
            <div class="brief">这是一篇测试文章</div>
            <div>
                <span>2018-11-11</span>
                <span> - </span>
                <span>木落</span>
                <span> - </span>
                <span>论坛</span>
            </div>
        </div>

        <div class="item">
            <h3 class="title">测试一下</h3>
            <div class="info">
                <span class="link">http://localhost:8080/search</span>
                <!-- <span>1234个回复，5678次查看</span> -->
            </div>
            <div class="brief">这是一篇测试文章</div>
            <div>
                <span>2018-11-11</span>
                <span> - </span>
                <span>木落</span>
                <span> - </span>
                <span>论坛</span>
            </div>
        </div>
    </div>
</div>
</template>

<style lang="scss" scoped>
.results {
    margin-top: 20px;
    > .item {
        .title {}
        margin-bottom: 20px;
    }
}
</style>

<script>
import state from '@/state.js'

export default {
    data () {
        return {
            state
        }
    }
}
</script>

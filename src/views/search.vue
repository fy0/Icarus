<template>
<div class="ic-container">
    <div v-title>搜索 - {{state.config.title}}</div>
    <template v-if="queryText">
        <div>以下为“{{queryText}}”的搜索结果，共123条</div>
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
    </template>
    <template v-else>没有指定搜索的关键字</template>
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
import api from '@/netapi.js'

export default {
    data () {
        return {
            state
        }
    },
    computed: {
        queryText: function () {
            return this.$route.query.q
        }
    },
    methods: {
        fetchData: async function () {
            let key = state.loadingGetKey(this.$route)
            this.state.loadingInc(this.$route, key)
            let query = this.$route.query
            console.log(111, query)
            let ret = await api.search.search(this.queryText)
            console.log(222, ret)
            this.state.loadingDec(this.$route, key)
        }
    },
    created: async function () {
        await this.fetchData()
    },
    watch: {
        '$route.query.q': async function (val) {
            await this.fetchData()
        }
    }
}
</script>

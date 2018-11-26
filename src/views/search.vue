<template>
<div class="ic-container">
    <div v-title>搜索 - {{state.config.title}}</div>
    <template v-if="queryText">
        <div>以下为<b>“{{queryText}}”</b>的搜索结果，共{{info.hits.total}}条</div>
        <div class="results" v-if="info.hits.hits">
            <div class="item" v-for="(v, k) in info.hits.hits" :key="k">
                <h3 class="title">
                    <post-link :type="v._source.type" :item="v._source" :use-slot="v.highlight.title">
                        <span v-if="v.highlight.title" v-html="v.highlight.title[0]" />
                    </post-link>
                    <span class="suffix">
                        <template v-if="v._source.main_category == 'forum'">论坛</template>
                        <template v-else-if="v._source.main_category == 'wiki'">百科</template>
                    </span>
                </h3>
                <div class="link">
                    <!-- <span class="link">http://localhost:8080/search</span> -->
                    <!-- <span>1234个回复，5678次查看</span> -->
                </div>
                <div class="brief" v-if="v.highlight.content" v-html="v.highlight.content[0]"></div>
                <div>
                    <ic-time :timestamp="v._source.time / 1000" :ago="false" />
                    <span> - </span>
                    <post-link :type="state.misc.POST_TYPES.USER" :item="{id: v._source.user_id, nickname: v._source.user_nickname}" />
                </div>
            </div>
        </div>
    </template>
    <template v-else>没有指定搜索的关键字</template>
</div>
</template>

<style lang="scss">
.results {
    > .item {
        > .title {
            em {
                font-style: normal; // 移除斜体效果
                color: $red !important;
            }
        }
        > .brief {
            em {
                font-style: normal; // 移除斜体效果
                color: darken($red, .5) !important;
            }
        }
    }
}
</style>

<style lang="scss" scoped>
.results {
    margin-top: 20px;
    > .item {
        > .title {
            em {
                color: $red !important;
            }

            > .suffix {
                font-size: 16px;
                margin-left: .5em;
                color: #b53b78;
            }
        }
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
            state,
            info: {
                hits: {}
            }
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
            this.info = ret.data
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

<template>
<wiki-base v-if="item">
    <article class="box article ic-paper ic-z1">
        <h1>{{item.title}}</h1>
        <div class="content" v-html="marked(item.content || '')"></div>
    </article>
    <div style="margin-left: 10px; font-size: 14px; color: #777">
        <span>最后更新时间：</span><ic-time :timestamp="item.time"/>
    </div>
</wiki-base>
<page-not-found v-else />
</template>

<style lang="scss" scoped>
article h1 {
    text-align: center;
}

.box {
    background: $white;
    padding: 10px;
    height: 100%;
    height: calc(100% - 15px);
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import { marked } from '@/md.js'
import WikiBase from './_base.vue'

export default {
    data () {
        return {
            state,
            marked,
            loading: true,
            item: null
        }
    },
    methods: {
        fetchData: async function () {
            let wrong = false
            let params = this.$route.params

            let ret = await api.wiki.get({
                id: params.id
            })

            if (ret.code === api.retcode.SUCCESS) {
                this.item = ret.data
            } else if (ret.code === api.retcode.NOT_FOUND) {
            } else {
                wrong = ret
            }

            if (wrong) {
                $.message_by_code(wrong.code)
            }
        }
    },
    created: async function () {
        let key = state.loadingGetKey(this.$route)
        this.state.loadingInc(this.$route, key)
        await this.fetchData()
        this.state.loadingDec(this.$route, key)
    },
    components: {
        WikiBase
    }
}
</script>

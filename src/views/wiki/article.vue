<template>
<wiki-base v-if="item">
    <div v-title>{{ item.title }} - 百科 - {{state.config.title}}</div>
    <article class="box article ic-paper ic-z1">
        <div class="title">
            <span>
                <h1>{{item.title}}</h1>
            </span>
            <span style="font-size: 14px; float: right; text-align: right; flex-shrink: 0;">
                <span class="stat">
                    <span class="item" title="阅读次数">
                        <i class="icarus icon-eye-outline" />
                        <template>{{item.s.click_count}}</template>
                    </span>
                    <span class="item" title="编辑次数">
                        <i class="icarus icon-zidingyi" />
                        <template>{{item.s.edit_count}}</template>
                    </span>
                    <span class="item" title="最后更新时间">
                        <i class="icarus icon-time1" />
                        <ic-time :timestamp="item.s.update_time"/>
                    </span>
                </span>
                <div>
                    <router-link v-if="canEditWiki()" :to="{ name: 'wiki_article_edit', params: {id: item.id}, query: { manage: true } }">[编辑]</router-link>
                    <router-link :to="{ name: 'wiki_history', params: {id: item.id} }" style="margin-left: 5px">[历史]</router-link>
                </div>
            </span>
        </div>
        <div class="ic-hr" style="margin: 10px 0;"></div>
        <div class="content" v-html="marked(item.content || '')"></div>
    </article>
    <div style="margin-left: 10px; font-size: 14px; color: #777">
    </div>
</wiki-base>
<page-not-found v-else />
</template>

<style lang="scss" scoped>
.sup {
    font-size: smaller;
    vertical-align: super;
}

.stat > .item {
    margin-left: 15px;

    > i {
        margin-right: 3px;
    }
}

article > .title {
    display: flex;
    position: relative;
    justify-content: space-between;
}

.box {
    background: $white;
    padding: 10px;
    height: 100%;
    height: 100%;
}

.ic-hr {
    margin: 10px 0;
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
        canEditWiki: $.canEditWiki,
        fetchData: async function () {
            let wrong = false
            let params = this.$route.params

            let ret = await api.wiki.get(Object.assign({
                loadfk: { 'id': {as: 's'} }
            }, params))
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

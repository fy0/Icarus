<template>
<wiki-base>
    <div v-title>[历史记录]{{ article.title }} - 百科 - {{state.config.title}}</div>
    <div class="box ic-paper ic-z1">
        <div class="title">
            <h1>[历史记录]{{article.title}}</h1>
            <span style="font-size: 14px; float: right; text-align: right; flex-shrink: 0;">
                <div v-if="article.ref">
                    <router-link :to="{ name: 'wiki_article_by_ref', params: {ref: article.ref} }" style="margin-left: 5px">[返回原文]</router-link>
                </div>
            </span>
        </div>
        <div class="ic-hr" style="margin: 10px 0;"></div>
        <ul v-if="page.items && page.items.length">
            <li v-for="i in page.items" :key="i.id">
                <span>
                    <user-link :user="i.user_id" /> 对此文章进行了<b>{{state.misc.MANAGE_OPERATION_TXT[i.operation]}}</b>操作 - <ic-time :timestamp="i.time" />
                </span>
            </li>
        </ul>
        <div v-else>尚无历史记录</div>
        <page-not-found v-if="notFound" />
    </div>
</wiki-base>
</template>

<style lang="scss" scoped>
.box {
    background: $white;
    padding: 10px;
    height: 100%;
}

.title {
    display: flex;
    position: relative;
    justify-content: space-between;
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
            notFound: false,
            loading: true,
            article: {},
            page: {
                items: []
            }
        }
    },
    methods: {
        canEditWiki: $.canEditWiki,
        fetchData: async function () {
            let wrong = false
            let params = this.$route.params
            let pageNumber = params.page || 1

            let getArticle = async () => {
                let ret = await api.wiki.get({
                    id: params.id,
                    select: ['id', 'title', 'ref']
                }, $.getRole('user'))
                if (ret.code === api.retcode.SUCCESS) {
                    this.article = ret.data
                } else if (ret.code === api.retcode.NOT_FOUND) {
                    this.notFound = true
                } else {
                    wrong = ret
                }
            }

            let getHistory = async () => {
                let ret = await api.logManage.list({
                    related_id: params.id,
                    order: 'time.desc',
                    loadfk: { 'user_id': null }
                }, pageNumber, null, $.getRole('user'))

                if (ret.code === api.retcode.SUCCESS) {
                    this.page = ret.data
                } else if (ret.code === api.retcode.NOT_FOUND) {
                    this.page.items = []
                } else {
                    wrong = ret
                }
            }

            await Promise.all([getHistory(), getArticle()])
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

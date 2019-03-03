<template>
<div>
    <wiki-base>
        <!-- <div v-title>[历史记录]{{ article.title }} - 百科 - {{config.title}}</div> -->
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
                        <user-link :user="i.user_id" /> 对此文章进行了<b>{{MANAGE_OPERATION_TXT[i.operation]}}</b>操作 - <ic-time :timestamp="i.time" />
                        <!-- <pre>{{i.value}}</pre> -->
                    </span>
                </li>
            </ul>
            <div v-else>尚无历史记录</div>
            <page-not-found v-if="notFound" />
        </div>
    </wiki-base>
</div>
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
import { mapState, mapGetters } from 'vuex'
import { marked } from '@/md.js'
import WikiBase from './_base.vue'

export default {
    data () {
        return {
            marked,
            notFound: false,
            article: {},
            page: {
                items: []
            }
        }
    },
    computed: {
        ...mapState(['config']),
        ...mapGetters(['MANAGE_OPERATION_TXT']),
        ...mapGetters('user', ['basicRole'])
    },
    methods: {
        fetchData: async function () {
            let wrong = false
            let params = this.$route.params
            let pageNumber = params.page || 1

            let getArticle = async () => {
                let ret = await this.$api.wiki.get({
                    id: params.id,
                    select: ['id', 'title', 'ref']
                }, this.basicRole)
                if (ret.code === this.$api.retcode.SUCCESS) {
                    this.article = ret.data
                } else if (ret.code === this.$api.retcode.NOT_FOUND) {
                    this.notFound = true
                } else {
                    wrong = ret
                }
            }

            let getHistory = async () => {
                console.log(1111, this.$api.logManage, this.$api.user)
                let ret = await this.$api.logManage.list({
                    related_id: params.id,
                    order: 'time.desc',
                    loadfk: { 'user_id': null }
                }, pageNumber, null, this.basicRole)

                if (ret.code === this.$api.retcode.SUCCESS) {
                    this.page = ret.data
                } else if (ret.code === this.$api.retcode.NOT_FOUND) {
                    this.page.items = []
                } else {
                    wrong = ret
                }
            }

            await Promise.all([getHistory(), getArticle()])
            if (wrong) {
                this.$message.byCode(wrong.code)
            }
        }
    },
    created: async function () {
        this.$store.commit('LOADING_INC', 1)
        await this.fetchData()
        this.$store.commit('LOADING_DEC', 1)
    },
    components: {
        WikiBase
    }
}
</script>

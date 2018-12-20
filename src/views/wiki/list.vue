<template>
<wiki-base>
    <div v-title>全部文章 - 百科 - {{state.config.title}}</div>
    <div class="box ic-paper ic-z1">
        <template v-if="page.items.length === 0">尚无文章</template>
        <template v-else>
            <ul>
                <li v-for="i in page.items" :key="i.id">
                    <router-link :to="{ name: 'wiki_article_by_ref', params: {'ref': i.ref } }">{{i.title}}</router-link>
                    <router-link v-if="canEditWiki()" :to="{ name: 'wiki_article_edit', params: {'id': i.id }, query: { manage: true } }" style="margin-left: 10px">[编辑]</router-link>
                </li>
            </ul>
        </template>
    </div>
</wiki-base>
</template>

<style lang="scss" scoped>
.box {
    background: $white;
    padding: 10px;
    height: 100%;
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

            let ret = await api.wiki.list({
                flag: null,
                order: 'title.asc'
            }, pageNumber, null, $.getRole('user'))

            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
            } else if (ret.code === api.retcode.NOT_FOUND) {
                this.page.items = []
            } else {
                wrong = ret
            }

            if (wrong) {
                $.message_by_code(wrong.code)
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

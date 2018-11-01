<template>
<wiki-base>
    <div class="box ic-paper ic-z1">
        <h3>历史记录</h3>
        <!-- <div class="ic-hr" style="margin: 10px 0;"></div> -->
        <ul>
            <li v-for="i in page.items" :key="i.id">
                <router-link :to="{ name: 'wiki_article_by_id', params: {'id': i.id } }">{{i.title}}</router-link>
                <template> - </template>
                <ic-time :timestamp="i.time" />
                <template>, </template>
                <user-link class="author limit l2" :user="i.user_id" />
            </li>
        </ul>
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
                root_id: params.id,
                minor_ver: 0,
                order: 'major_ver.desc',
                loadfk: { 'user_id': null }
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

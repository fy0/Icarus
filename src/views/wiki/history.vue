<template>
<wiki-base>
    <div class="box ic-paper ic-z1">
        <h3>历史记录</h3>
        <!-- <div class="ic-hr" style="margin: 10px 0;"></div> -->
        <ul>
            <li v-for="(i, _) in page.items" :key="i.id">
                <template>版本{{i.major_ver}} - </template>
                <router-link :to="{ name: 'wiki_article_by_id', params: {'id': i.id } }">{{i.title}}</router-link>
                <template> - </template>
                <ic-time :timestamp="i.time" />
                <template>, </template>
                <user-link class="author limit l2" :user="i.user_id" />
                <ul v-if="_ === 0">
                    <!-- <li style="list-style: none;margin-left: -1em;font-weight: bold;">候选列表</li> -->
                    <li v-for="j in pageCandidate.items" :key="j.id">
                        <template>候选{{j.major_ver}}.{{j.minor_ver}}</template>
                        <template> - </template>
                        <router-link :to="{ name: 'wiki_article_by_id', params: {'id': j.id } }">{{j.title}}</router-link>
                        <template> - </template>
                        <ic-time :timestamp="j.time" />
                        <template>, </template>
                        <user-link class="author limit l2" :user="j.user_id" />
                        <button class="ic-btn primary small" style="margin-left: 10px">选为新版</button>
                    </li>
                </ul>
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
            },
            pageCandidate: {
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

            let getHistory = async () => {
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
            }

            let getCandidate = async () => {
                let ret = await api.wiki.get({
                    root_id: params.id,
                    is_current: true
                }, $.getRole('user'))

                let ret2 = await api.wiki.list({
                    root_id: params.id,
                    major_ver: ret.data.major_ver,
                    'minor_ver.ne': 0,
                    order: 'minor_ver.desc',
                    loadfk: { 'user_id': null }
                }, pageNumber, null, $.getRole('user'))

                if (ret2.code === api.retcode.SUCCESS) {
                    this.pageCandidate = ret2.data
                } else if (ret2.code === api.retcode.NOT_FOUND) {
                    this.pageCandidate.items = []
                } else {
                    wrong = ret2
                }
            }

            await Promise.all([getHistory(), getCandidate()])
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

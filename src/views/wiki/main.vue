<template>
<wiki-base>
    <div class="box ic-paper ic-z1">
        <div class="content" v-html="marked(mainpage.content || '')"></div>
    </div>
</wiki-base>
</template>

<style lang="scss" scoped>
.box {
    background: $white;
    height: 100%;
    padding: 10px;
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import { marked } from '@/md.js'
import WikiBase from './base.vue'

export default {
    data () {
        return {
            state,
            marked,
            loading: true,
            mainpage: {}
        }
    },
    methods: {
        fetchData: async function () {
            let wrong = false

            let ret = await api.wiki.get({
                flag: 2,
                is_current: true
            }, $.getRole('user'))

            if (ret.code === api.retcode.SUCCESS) {
                this.mainpage = ret.data
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

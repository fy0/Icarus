<template>
<wiki-base>
    <div class="box ic-paper ic-z1">
        <template v-if="page.items.length === 0">尚无文章</template>
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
import WikiBase from './base.vue'

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
        fetchData: async function () {
            let wrong = false
            let params = this.$route.params
            let pageNumber = params.page || 1

            let ret = await api.wiki.list({
                flag: null,
                is_current: true
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

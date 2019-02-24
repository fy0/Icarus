<template>
<wiki-base>
    <article class="box article ic-paper ic-z1">
        <div class="content" v-html="marked(mainpage.content || '')"></div>
    </article>
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
import { mapState } from 'vuex'
import { marked } from '@/md.js'
import WikiBase from './_base.vue'

export default {
    data () {
        return {
            marked,
            mainpage: {}
        }
    },
    computed: {
        ...mapState(['config'])
    },
    methods: {
        fetchData: async function () {
            let wrong = false

            let ret = await this.$api.wiki.get({
                flag: 2
            }, this.$user.basicRole)

            if (ret.code === this.$api.retcode.SUCCESS) {
                this.mainpage = ret.data
            } else {
                wrong = ret
            }

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

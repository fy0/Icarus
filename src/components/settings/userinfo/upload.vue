<template>
<setting-base>
    <div v-title>我的上传 - 用户设置 - {{state.config.title}}</div>
    <h3 class="ic-header">我的上传</h3>
    <div class="list">
        <div class="item" v-for="item in page.items" :key="item.id">
            <div class="wrap ic-paper round ic-z1">
                <img :src="staticUrl(item.key)" />
            </div>
        </div>
    </div>
</setting-base>
</template>

<style lang="scss" scoped>
.list {
    display: flex;
    flex-wrap: wrap;
    align-content: space-between;
    margin: 0 -5px; // 与横向向外突出白边相抵消

    .item {
        flex: 0 0 25%;

        .wrap {
            margin: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 190px;

            img {
                width: 100%;
            }
        }
    }
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import SettingBase from '../base/base.vue'

export default {
    data () {
        return {
            state,
            page: []
        }
    },
    created: async function () {
        let key = state.loadingGetKey(this.$route)
        this.state.loadingInc(this.$route, key)
        await this.fetchData()
        this.state.loadingDec(this.$route, key)
    },
    methods: {
        staticUrl: $.staticUrl,
        fetchData: async function () {
            let key = state.loadingGetKey(this.$route)
            this.state.loadingInc(this.$route, key)
            // let params = this.$route.query
            // this.page.curPage = params.page
            // let ret = await api.upload.token('user')

            let ret = await api.upload.list({
                'type_name.is': null
            }, 1, null, state.getRole('user'))

            console.log(111, ret)

            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
            //     // let pageNumber = this.$route.query.page
            //     // if (pageNumber) this.commentPage = parseInt(pageNumber)
            } else {
                $.message_by_code(ret.code)
            }
            this.state.loadingDec(this.$route, key)
        }
    },
    watch: {
        // 如果路由有变化，会再次执行该方法
        '$route': 'fetchData'
    },
    components: {
        SettingBase
    }
}
</script>

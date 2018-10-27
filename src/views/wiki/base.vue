<template>
<div class="ic-container">
    <div class="wrapper">
        <div class="left-nav">
            <div class="box ic-paper ic-z1">
                <div class="sidebar-content" v-html="marked(sidebar.content || '')">
                    <h1 id="til-1"><a href="#">模拟一些标题</a></h1>
                    <h1 id="til-2" class="active">模拟标题2</h1>
                    <h2 id="til-3">模拟标题33</h2>
                    <h2 id="til-4">模拟标题4</h2>
                    <h1 id="til-5">模拟标题5</h1>
                </div>
                <div>
                    <div>全部文章</div>
                    <div>添加文章</div>
                    <div>随机页面</div>
                </div>
            </div>
        </div>
        <div class="right" slot="right">
            <slot />
        </div>
    </div>
</div>
</template>

<style lang="scss" scoped>
.main {
    background-color: $gray-200;
}

$title-text-color:#777;
$title-text-active-color: darken(#373434, 0);

.wrapper {
    display: flex;
    height: 100%;
    flex: 1;

    .left-nav {
        flex: 5 1 0%;
        max-width: $page-left-max-width;
        height: 100%;
    }

    .left-nav > .box {
        // background-color: #373434;
        height: 100%;
        margin-right: 20px;
        font-size: 14px;

        a {
            color: $title-text-color;
        }

        > * {
            font-size: 14px;
            padding: 10px;
            color: $title-text-color;
            background-color: $white;

            &.active {
                color: $title-text-active-color;
                border-left: 1px solid $title-text-active-color;
            }
        }

        h1, h2, h3, h4, h5, h6 {
            // font-size: 14px;
        }
    }

    .right {
        flex: 19 1 0%;
    }
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import { marked } from '@/md.js'

export default {
    data () {
        return {
            state,
            marked,
            loading: true,
            sidebar: {}
        }
    },
    methods: {
        fetchData: async function () {
            let wrong = false

            let getSidebar = async () => {
                let ret = await api.wiki.get({
                    flag: 1,
                    is_current: true
                }, $.getRole('user'))

                if (ret.code === api.retcode.SUCCESS) {
                    this.sidebar = ret.data
                } else {
                    wrong = ret
                }
            }
            await Promise.all([getSidebar()])

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
    }
}
</script>

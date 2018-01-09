<!-- 评论 -->
<template>
<div class="ic-comment-list">
    <paginator :page-info='page' :route-name='"forum_topic"' :link-method="'query'" />
    <div v-for="i, _ in page.items" :key="i.id" class="ic-comment">
        <avatar :user="i.user_id" class="avatar"></avatar>
        <mu-paper class="content" :zDepth="1">
            <div class="head">
                <span>#{{(curPage - 1) * page.info.page_size + _ + 1}}</span>
                <b><router-link :to="{ name: 'account_userpage', params: {id: i.user_id.id} }">{{i.user_id.nickname}}</router-link></b>
                <span><ic-time :timestamp="i.time" /></span>
            </div>
            <div class="post">{{i.content}}</div>
        </mu-paper>
    </div>
</div>
</template>

<style>
/* 注意：评论样式不在 scope 之内，故意为之 */
.ic-comment {
    display: flex;
    margin-bottom: 1em;
}

.ic-comment .content > .head {
    font-size: .8em;
    padding-bottom: .6em;
}

.ic-comment .content > .post {
}

.ic-comment .content {
    flex: 1 0 0%;
    margin-left: 15px;

    border-radius: 3px;
    background: #fff;
    padding: 1px;
    position: relative;
    padding: .6em;
}

.ic-comment .content:before, .ic-comment .content:after {
    content:" ";
    border-top-color:transparent !important; 
    border-bottom-color:transparent !important; 
    border-left-color:transparent !important;
    border-style:solid;
    border-width:8px;
    height:0; 
    width:0; 
    left:-16px; 
    top:12px;
    color: #ccc;
    position:absolute
}

.ic-comment .content:after {
    float:left;
    left:-15px;
    border-color: #fff;
}
</style>

<script>
import api from '@/netapi.js'

export default {
    props: {
        item: {
            type: Object
        },
        curPage: {
            type: Number,
            default: 1
        },
        withPost: {
            default: false
        },
        postType: {},
        onSuccess: Function
    },
    data () {
        return {
            page: { info: {}, items: [] }
        }
    },
    created: async function () {
        // this.addTest()
    },
    mounted: async function () {
    },
    methods: {
        addTest: function () {
            let func = () => {
                this.page.items.push({
                    user_id: {
                        id: 'asdasd',
                        nickname: 'John Doe'
                    }
                })
            }
            $.tpReg('一条评论', func)
        },
        removeTest: function () {
            ;
        },
        fetchData: async function () {
            let ret = await api.comment.list({related_id: this.item.id, loadfk: {user_id: null}}, this.curPage)
            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
            } else if (ret.code === api.retcode.NOT_FOUND) {
                ;
            } else {
                ;
            }
        }
    },
    watch: {
        'item': async function (val) {
            // 似乎 mounted 和 created 中都读不到 item.id
            this.fetchData()
        },
        'curPage': async function (val) {
            this.fetchData()
        }
    },
    components: {
    }
}
</script>

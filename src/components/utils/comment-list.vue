<!-- 评论 -->
<template>
<div>
    <div class="ic-comment-list">
        <paginator :page-info='page' :route-name='"forum_topic"' :link-method="'query'" />
        <loading v-if="loading"/>
        <div v-else-if="page.items.length === 0" class="no-comment">目前尚未有评论</div>
        <div v-else v-for="i, _ in page.items" :key="i.id" class="ic-comment">
            <avatar :user="i.user_id" class="avatar"></avatar>
            <mu-paper class="content" :zDepth="1">
                <div class="head">
                    <span>#{{(page.cur_page - 1) * page.info.page_size + _ + 1}}</span>
                    <b><user-link :user="i.user_id" /></b>
                    <span v-if="i.reply_to_cmt_id">
                        <span>回复</span>
                        <b><user-link :user="i.reply_to_cmt_id.user_id" /></b>
                    </span>
                    <span><ic-time :timestamp="i.time" /></span>
                    <a style="float: right" @click="replyTo(i)" href="javascript:void(0)">回复</a>
                </div>
                <div class="post" v-html="marked(i.content || '')"></div>
            </mu-paper>
        </div>
    </div>
    <comment-post @on-commented="commented" :item="item" :post-type="postType" ref="post"></comment-post>
</div>
</template>

<style>
/* 注意：评论样式不在 scope 之内，故意为之 */
.ic-comment-list > .no-comment {
    padding: 20px 0;
    text-align: center;
}

.ic-comment {
    display: flex;
    margin-bottom: 1em;
}

.ic-comment .content > .head {
    font-size: .8em;
    /* padding-bottom: .6em; */
}

.ic-comment .content > .post {
    padding: 0px 6px;
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
import marked from 'marked'
import api from '@/netapi.js'
import CommentPost from '../utils/comment-post.vue'

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
        postType: {}
    },
    data () {
        return {
            marked,
            loading: true,
            page: { info: {}, items: [] }
        }
    },
    created: async function () {
        // 如果控件加载时即有数据，那么加载数据
        if (this.item.id) {
            this.fetchData()
        }
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
        commented: function () {
            let info = this.page.info
            let newPage = Math.ceil((info.items_count + 1) / info.page_size)
            this.fetchData(newPage)
        },
        replyTo: function (item) {
            $.scrollTo(document.getElementById('ic-comment-post'))
            document.getElementById('ic-comment-editor').focus()
            this.$refs.post.setReplyTo(item)
        },
        fetchData: async function (thePage) {
            this.loading = true
            thePage = thePage || this.curPage
            this.page.cur_page = thePage
            let ret = await api.comment.list({
                related_id: this.item.id,
                loadfk: {user_id: null, reply_to_cmt_id: {loadfk: {'user_id': null}}}
            }, thePage)
            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
            } else if (ret.code === api.retcode.NOT_FOUND) {
                ;
            } else {
                ;
            }
            this.loading = false
        }
    },
    watch: {
        'item': async function (val) {
            // 如果控件加载时无数据，后续出现数据，那么刷新
            this.fetchData()
        },
        'curPage': async function (val) {
            this.fetchData()
        }
    },
    components: {
        CommentPost
    }
}
</script>

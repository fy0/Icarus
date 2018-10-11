<template>
<div class="ic-container" v-if="topic.user_id">
    <div v-title>{{ topic.title }} - {{topic.board_id.name}} - {{state.config.title}}</div>

    <div class="nav">
        <span>
            <router-link :to="{ name: 'forum' }">社区</router-link>
        </span>
        <span class="item-separator">/</span>
        <span>
            <router-link :to="{ name: 'forum_board', params: {id: topic.board_id.id} }">{{topic.board_id.name}}</router-link>
        </span>
        <span class="item-separator">/</span>
        <span>
            <span>{{topic.title}}</span>
            <span v-if="topic.state === state.misc.POST_STATE.CLOSE">[关闭]</span>
        </span>
    </div>

    <div class="ic-hidden ic-xs" style="display: flex;align-items: center;">
        <user-link style="display: flex; padding: 10px 0;" class="user-link" :nickname="false" :user="topic.user_id">
            <avatar style="margin-right: 10px;" :user="topic.user_id" :size="28" class="avatar"></avatar>
            <span>{{topic.user_id.nickname}}</span>
        </user-link>
        <div style="margin-left: 10px">发布于 <ic-time :timestamp="topic.time" /></div>
    </div>

    <div class="topic-box">
        <div class="main">
            <div class="article typo">
                <!--<h1>{{topic.title}}</h1>-->
                <div class="content" v-if="topic.state === state.misc.POST_STATE.CONTENT_IF_LOGIN">
                    <p>登陆后可见正文</p>
                </div>
                <div class="content" v-else v-html="marked(topic.content || '')"></div>
                <div v-if="mlog && mlog.items" class="post-manage-log">
                    <div class="post-manage-log-item" v-for="i in mlog.items.slice(0, 5)" :key="i.id">
                        <span>🛠️<user-link :user="i.user_id" /> 对此主题进行了<b>{{state.misc.MANAGE_OPERATION_TXT[i.operation]}}</b>操作 - <ic-time :timestamp="i.time" /></span>
                    </div>
                    <div v-if="mlog.items.length > 5">...</div>
                </div>

                <div style="display: flex; align-items: center;">
                    <span>分享：</span>
                    <div ref="share" class="share-component" data-disabled="douban,tencent,linkedin,diandian,google,qq,facebook,twitter"></div>
                </div>

                <p class="ic-hr"></p>
                <comment-list :item="topic" :cur-page="commentPage" :post-type="POST_TYPES.TOPIC"/>
            </div>
        </div>

        <div class="info ic-xs-hidden">
            <div class="box">
                <div class="author">
                    <div style="display: flex; align-items: center;">
                        <avatar :user="topic.user_id" :size="60" class="avatar"></avatar>
                        <div style="margin-left: 6px; line-height: 1.3em;">
                            <user-link :user="topic.user_id" />
                            <div>{{state.misc.USER_GROUP_TXT[topic.user_id.group]}}</div>
                        </div>
                    </div>
                </div>
                <div class="other">
                    <div class="txt3">
                        <div>发布时间：<ic-time :timestamp="topic.time" /></div>
                        <div>最后修改：<ic-time :timestamp="topic.edit_time" /></div>
                        <div>阅读次数：<span>{{topic.s.click_count}}</span></div>
                    </div>

                    <div v-if="false">
                        <a  class="furbtn furbtn-s furbtn-blue"><i class="fa fa-star-o"></i> 关注作者</a>
                        <a class="furbtn furbtn-s furbtn-green"><i class="fa fa-heart-o"></i> 收藏主题</a>
                        <a class="furbtn furbtn-s furbtn-green" fav="1"><i class="fa fa-heart"></i> 取消收藏</a>
                        <a class="furbtn furbtn-s furbtn-blue" follow="1"><i class="fa fa-star"></i> 取消关注</a>
                    </div>

                    <p><router-link v-if="state.user && (topic.user_id.id == state.user.id)" :to="{ name: 'forum_topic_edit', params: {id: topic.id} }">编辑文章</router-link></p>
                    <div class="last-edit" v-if="topic.edit_time" style="font-size: 0.8em">
                        <p>此文章由 <user-link :user="topic.last_edit_user_id" /> 最后编辑于 <ic-time :timestamp="topic.edit_time" /></p>
                        <p>历史编辑次数 {{topic.edit_count}} 次</p>
                    </div>
                    <div class="topic-manage" v-if="isAdmin">
                        <i class="icarus icon-sword-cross" title="管理" style="color: #71c1ef; cursor: pointer" @click="setTopicManage(topic)"></i>
                    </div>

                    <div v-if="topicIndex && topicIndex.length" class="topic-index-container" ref="index" :class="{'sticky': indexSticky}">
                        <h2>目录</h2>
                        <ul class="topic-index">
                            <li v-for="(i, _) in topicIndex" :key="_">
                                <a :class="[indexActive == _ ? 'active' : '', `h${i.depth}`]" :href="`#til-${_+1}`" @click.prevent.stop="scrollTo(`til-${_+1}`)">{{i.text}}</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <dialog-topic-manage />
</div>
<page-not-found v-else />
</template>

<style>
.topic-box {
    margin-top: 25px;
}

/* 列表靠左对齐：不行，这会毁灭多级列表，子级会失去相对父级的缩进 */
/* .topic-box .article > .content ul {
    padding-left: 0;
    list-style-position: inside;
}

.topic-box .article > .content ol {
    padding-left: 0;
    list-style-position: inside;
} */
</style>

<style lang="scss" scoped>
.nav {
    width: 65%;
    overflow: hidden;
    text-overflow: ellipsis;
    /* word-break: break-all; */
    white-space: nowrap;
    font-size: 18px;
}

.post-manage-log {
    padding: 5px 0;
    .post-manage-log-item {
        color: $gray-500;
    }
}

.item-separator {
    margin: 0 8px;
    color: #d7dde4;
}

.topic-manage > .group {
    display: flex;
}

.topic-manage > .group > a {
    padding: 5px 10px;
}

.topic-box {
    display: flex;
}

.topic-box > .main {
    flex: 18 0 0%;
}

.info > .box {
    padding: 0 20px;
}

.info > .box > .other {
    padding-top: 30px;
}

.other > .txt3 {
    font-size: 14px;
}

.info > .author {
    display: flex;
    flex-direction: column;
    font-size: 16px;
}

.main > .article > h1 {
    font-size: 28px;
    line-height: 48px;
    text-align: center;
}

.topic-box > .info {
    flex: 6 0 0%;
}

.topic-index-container {
    &.sticky {
        position: fixed;
        top: 0;
    }

    > h2 {
        font-size: 16px;
        margin-top: 10px;
    }
}

.topic-index {
    font-size: 14px;
    padding-left: 0;
    margin-top: 0;
    list-style-position: inside;

    li {
        font-size: 14px;
        list-style: none;
        font-weight: bolder;
        margin-bottom: 5px;
        margin-left: 0;

        a {
            color: $gray-600;
            margin-left: 3em;
        }

        a.active {
            font-weight: bold;
            color: $gray-700;
        }

        .h1, .h2 { margin-left: 1em; }
        .h3, .h4 { margin-left: 2em; }
        .h2::before { content:"∎ "; }
        .h3::before { content:"> "; }
        .h4::before { content:"⎔ "; }
        .h5::before { content:"○ "; }
        .h6::before { content:"⋄ "; }
    }
}
</style>

<script>
import { marked, mdGetIndex } from '@/md.js'
import api from '@/netapi.js'
import state from '@/state.js'
import '@/assets/css/_forum.scss'
import CommentList from '@/components/misc/comment-list.vue'

export default {
    data () {
        return {
            state,
            commentPage: 1,
            loading: true,
            POST_TYPES: state.misc.POST_TYPES,
            topic: { board_id: { id: 1 } },
            topicIndex: [],
            indexActive: -1,
            indexSticky: false,
            mlog: null
        }
    },
    computed: {
        isAdmin: $.isAdmin
    },
    methods: {
        marked,
        scrollTo: function (id) {
            let el = document.getElementById(id)
            $.scrollTo(el)
        },
        setTopicManage: function (topic) {
            state.dialog.topicManageData = topic
            state.dialog.topicManage = true
        },
        fetchData: async function () {
            let params = this.$route.params
            let ret = await api.topic.get({
                id: params.id,
                loadfk: { user_id: null, board_id: null, last_edit_user_id: null, 'id': { 'as': 's' } }
            }, $.getRole('user'))

            if (ret.code === api.retcode.SUCCESS) {
                let mlog = await api.logManage.list({
                    related_id: ret.data.id,
                    order: 'time.desc',
                    loadfk: { 'user_id': null }
                })
                if (mlog.code === api.retcode.SUCCESS) {
                    this.mlog = mlog.data
                }

                let pageNumber = this.$route.query.page
                if (pageNumber) this.commentPage = parseInt(pageNumber)
                this.topic = ret.data
                this.topicIndex = mdGetIndex(ret.data.content)
            } else {
                if (ret.code !== api.retcode.NOT_FOUND) {
                    $.message_by_code(ret.code)
                }
            }
        }
    },
    watch: {
        '$route.query.page': async function (val) {
            this.commentPage = val
        }
    },
    created: async function () {
        // 注意：从这里观察出一个现象：
        // created 会比 mounted 早触发，但并不一定更早完成
        // await 占用时间的时候，挂载流程仍将继续
        let key = state.loadingGetKey(this.$route)
        this.state.loadingInc(this.$route, key)
        await this.fetchData()
        this.$nextTick(() => {
            window.socialShare(this.$refs.share, {
                title: `${this.topic.title} - ${state.config.title}`
            })

            // 右侧目录跟随滚动
            let elTop = 0
            let loop = () => {
                let el = this.$refs.index
                if (!el) return
                elTop = Math.max(el.offsetTop, elTop)
                let scrollTop = document.documentElement.scrollTop
                this.indexSticky = scrollTop > elTop

                for (let i = 0; i < this.topicIndex.length; i++) {
                    let el = document.getElementById(`til-${i + 1}`)
                    if (el.offsetTop >= (scrollTop - 5)) {
                        this.indexActive = i
                        break
                    }
                }
                setTimeout(loop, 100)
            }
            setTimeout(loop, 100)
        })

        this.state.loadingDec(this.$route, key)
    },
    mounted: function () {
    },
    components: {
        CommentList
    }
}
</script>

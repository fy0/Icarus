<!-- 评论 -->
<template>
<div class="ic-comment-post" id="ic-comment-post">
    <div class="ic-comment" v-if="isInactiveUser">
        <avatar :user="state.user" class="avatar"></avatar>
        <div class="right-box">
            <div class="ic-paper round ic-z1 not-signin-content">你的账号需要激活后才能发言，请检查邮箱</div>
        </div>
    </div>

    <div class="ic-comment" v-else-if="state.user">
        <avatar :depth="editing ? 3 : 1" :user="state.user" class="avatar"></avatar>
        <div class="right-box" v-if="isClosed()">
            <div class="ic-paper round ic-z1 not-signin-content">评论已关闭</div>
        </div>
        <div class="right-box content" v-else>
            <textarea :class="[editing ? 'ic-z3' : 'ic-z1']" id="ic-comment-editor" @focus="onEditorFocus" @blur="onEditorBlur"
                class="ic-input ic-paper round" rows="5" v-model="commentInfo.content"
                :placeholder="'此处填写评论内容。\n可使用 markdown 语法。\n请理性讨论，友善发言，共同维护社区秩序。'">
            </textarea>
            <div style="display: flex; justify-content: space-between;" class="postBtnBox">
                <div v-if="!replyTo"></div>
                <div style="align-items: center; display: flex;" v-else>
                    <a href="javascript:void(0)" @click="setReplyTo(null)">×</a>
                    <div style="margin-left: 10px">正在回复：{{replyTo.user_id.nickname}}</div>
                </div>
                <div class="ic-paper round" :class="[editing ? 'ic-z3' : 'ic-z1']">
                    <button class="postBtn ic-btn primary" @click="commentPost">发表</button>
                </div>
            </div>
        </div>
    </div>

    <div class="ic-comment" v-else>
        <avatar :anonymous="true" class="avatar"></avatar>
        <div class="right-box">
            <div class="not-signin-content">
                需要 <router-link :to="{ name: `account_signin` }">登录</router-link> 后方可回复, 如果你还没有账号，那么可以 <router-link :to="{ name: `account_signup` }">注册</router-link> 一个帐号。
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
.ic-comment-post {
    margin-top: 20px
}

.ic-comment .not-signin-content {
    margin-left: 20px;
    min-height: 50px;
    padding: 10px 20px;
}

.ic-comment .content {
    min-height: 50px;
}

.ic-comment-post > .ic-comment {
    padding: 20px 0;
    border-bottom: none;
}

.right-box {
    flex: 1 0 0%;
    /* 视觉误差吧，总之加上之后舒服了一些*/
    margin-top: 1px;
}

#ic-comment-editor {
    width: 100%;
}

.postBtnBox {
    margin-top: 15px;
    margin-left: 15px;
}

.postBtn {
    padding-left: 20px;
    padding-right: 20px;
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'

export default {
    props: {
        item: Object,
        postType: {}
    },
    data () {
        return {
            state,
            loading: false,
            replyTo: null,
            editing: false,
            commentInfo: {
                related_id: null,
                related_type: null,
                content: ''
            }
        }
    },
    computed: {
        isInactiveUser: function () {
            return state.getRole('user') === 'inactive_user'
        }
    },
    created: function () {
    },
    mounted: function () {
        ;
    },
    methods: {
        isClosed () {
            if (this.postType === state.misc.POST_TYPES.TOPIC) {
                return this.item.state <= state.misc.POST_STATE.CLOSE
            }
            return false
        },
        setReplyTo: function (val) {
            this.replyTo = val
        },
        onEditorFocus: async function () {
            this.editing = true
        },
        onEditorBlur: async function () {
            this.editing = false
        },
        commentPost: async function () {
            if (this.loading) return
            this.loading = true
            this.commentInfo.related_id = this.item.id
            this.commentInfo.related_type = this.postType
            if (this.replyTo) this.commentInfo.reply_to_cmt_id = this.replyTo.id
            let ret = await api.comment.new(this.commentInfo, 'user')
            $.message_by_code(ret.code)
            if (ret.code === 0) {
                this.editing = false
                this.replyTo = null
                this.commentInfo.content = ''
            }
            this.$emit('on-commented')
            this.loading = false
        }
    },
    components: {
    }
}
</script>

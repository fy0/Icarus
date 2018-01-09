<!-- 评论 -->
<template>
<div class="ic-comment-post">
    <div class="ic-comment" v-if="state.user">
        <avatar :user="state.user" class="avatar"></avatar>
        <div class="right-box">
            <mu-paper :zDepth="editing ? 2 : 1" class="content">
                <textarea @focus="onEditorFocus" @blur="onEditorBlur" class="commentArea" rows="5" placeholder="" v-model="commentInfo.content"></textarea>
            </mu-paper>
            <mu-paper :zDepth="editing ? 2 : 1" class="postBtnBox">
                <mu-raised-button label="发表" class="postBtn" @click="commentPost" primary />
            </mu-paper>
        </div>
    </div>

    <div class="ic-comment" v-else>
        <avatar :anonymous="true" class="avatar"></avatar>
        <div class="right-box">
            <mu-paper :zDepth="editing ? 2 : 1" class="content">
                需要 <router-link :to="{ name: `account_signin` }">登录</router-link> 后方可回复, 如果你还没有账号你可以 <router-link :to="{ name: `account_signup` }">注册</router-link> 一个帐号。
            </mu-paper>
        </div>
    </div>
</div>
</template>

<style scoped>
.ic-comment-post {
    margin-top: 20px
}

.ic-comment .content {
    min-height: 50px;
}

.right-box {
    flex: 1 0 0%;
    /* 视觉误差吧，总之加上之后舒服了一些*/
    margin-top: 1px;
}

.commentArea {
    resize: none;
    border: none;
    outline:none;
    width: 100%;
}

.postBtnBox {
    margin-top: 15px;
    float: right;
}

.postBtn {
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'

export default {
    props: {
        item: Object,
        postType: {},
        onSuccess: Function
    },
    data () {
        return {
            state,
            editing: false,
            commentInfo: {
                related_id: null,
                related_type: null,
                content: ''
            }
        }
    },
    created: function () {
    },
    mounted: function () {
        ;
    },
    methods: {
        onEditorFocus: async function () {
            this.editing = true
        },
        onEditorBlur: async function () {
            this.editing = false
        },
        commentPost: async function () {
            this.commentInfo.related_id = this.item.id
            this.commentInfo.related_type = this.postType
            let ret = await api.comment.new(this.commentInfo)
            $.message_by_code(ret.code)
            if (ret.code === 0) {
                this.editing = false
                this.commentInfo.content = ''
            }
            if (this.onSuccess) this.onSuccess()
        }
    },
    components: {
    }
}
</script>

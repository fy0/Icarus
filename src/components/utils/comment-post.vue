<!-- 评论 -->
<template>
<div class="ic-comment-post">
    <div class="ic-comment" v-if="state.user">
        <avatar :user="state.user" class="avatar"></avatar>
        <div class="right-box">
            <mu-paper :zDepth="editing ? 2 : 1" class="content">
                <textarea @focus="onEditorFocus" @blur="onEditorBlur" class="commentArea" rows="5" placeholder="" v-model="commentText"></textarea>
            </mu-paper>
            <mu-paper :zDepth="editing ? 2 : 1" class="postBtnBox">
                <mu-raised-button class="postBtn" @click="commentPost">发表</mu-raised-button>
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
import Avatar from './avatar.vue'

export default {
    props: {
        item: Object
    },
    data () {
        return {
            state,
            editing: false,
            commentText: ''
        }
    },
    mounted: function () {
        this.addTest()
    },
    methods: {
        onEditorFocus: async function () {
            this.editing = true
        },
        onEditorBlur: async function () {
            this.editing = false
        },
        commentPost: async function () {
            let ret = await api.comment.new(this.topicInfo)
            console.log(ret)
        },
        addTest: function () {
            /*
            let func = () => {
                this.items.push({
                    user: {
                        id: 'asdasd',
                        name: 'John Doe'
                    }
                })
            }
            $.tpReg('发表', func)
            */
        },
        removeTest: function () {
            ;
        }
    },
    components: {
        Avatar
    }
}
</script>

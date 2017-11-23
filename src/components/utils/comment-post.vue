<!-- 评论 -->
<template>
<div class="ic-comment-post" v-if="state.user" style="margin-top: 20px">
    <div class="ic-comment">
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
</div>
<div style="padding: 20px" v-else>
    需要 <router-link :to="{ path: `/signin` }">登录</router-link> 后方可回复, 如果你还没有账号你可以 <router-link :to="{ path: `/signup` }">注册</router-link> 一个帐号。
</div>
</template>

<style scoped>
.right-box {
    flex: 1 0 0%;
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

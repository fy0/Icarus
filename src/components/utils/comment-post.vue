<!-- 评论 -->
<template>
<div class="ic-comment-post" v-if="state.user" style="margin-top: 20px">
    <div class="ic-comment">
        <avatar :user="state.user" class="avatar"></avatar>
        <mu-paper class="content" :zDepth="1">
            <textarea name="content" rows="5" placeholder="" style="width:100%;border-color:#d9d9d9" v-model="commentText"></textarea>
            <mu-raised-button @click="commentPost">发表</mu-raised-button>
            <span style="margin-left:10px" id="reply_msg"></span>
        </mu-paper>
    </div>
</div>
<div style="padding: 20px" v-else>
    需要 <router-link :to="{ path: `/signin` }">登录</router-link> 后方可回复, 如果你还没有账号你可以 <router-link :to="{ path: `/signup` }">注册</router-link> 一个帐号。
</div>
</template>

<style>
/* 注意：评论样式不在 scope 之内，故意为之 */
.ic-comment {
    display: flex;    
    margin-bottom: 1em;
}

.ic-comment > .content > .head {
    padding-bottom: .6em;
}

.ic-comment > .content > .post {
}

.ic-comment > .content {
    flex: 1 0 0%;
    margin-left: 15px;

    border-radius: 3px;
    background: #fff;
    padding: 1px;
    position: relative;
    padding: .6em;
}

.ic-comment > .content:before, .ic-comment > .content:after {
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
    color: #aaa;
    position:absolute
}

.ic-comment > .content:after {
    float:left;
    left:-15px;
    border-color: #fff;
}
</style>

<script>
import state from '@/state.js'
import Avatar from './avatar.vue'

export default {
    data () {
        return {
            state,
            commentText: ''
        }
    },
    mounted: function () {
        this.addTest()
    },
    methods: {
        commentPost: async function () {
            ;
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

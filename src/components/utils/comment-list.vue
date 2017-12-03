<!-- 评论 -->
<template>
<div class="ic-comment-list">
    <div v-for="i in page.items" :key="i.id" class="ic-comment">
        <avatar :user="i.user" class="avatar"></avatar>
        <mu-paper class="content" :zDepth="1">
            <div class="head">
                <span>#1</span>
                <b>{{i.user.name}}</b>
                <span>2017-10-29 13:11</span>
            </div>
            <div class="post">123</div>
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
import Avatar from './avatar.vue'
import api from '@/netapi.js'

export default {
    props: {
        item: {
            type: Object
        }
    },
    data () {
        return {
            page: { info: {}, items: [] }
        }
    },
    created: async function () {
        this.addTest()
    },
    mounted: async function () {
    },
    methods: {
        addTest: function () {
            let func = () => {
                this.page.items.push({
                    user: {
                        id: 'asdasd',
                        nickname: 'John Doe'
                    }
                })
            }
            $.tpReg('一条评论', func)
        },
        removeTest: function () {
            ;
        }
    },
    watch: {
        'item': async function (val) {
            // 似乎 mounted 和 created 中都读不到 item.id
            let ret = await api.comment.get({id: this.item.id})
            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
            } else if (ret.code === api.retcode.NOT_FOUND) {
                ;
            } else {
                ;
            }
        }
    },
    components: {
        Avatar
    }
}
</script>

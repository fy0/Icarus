<!-- 评论 -->
<template>
<div class="ic-comment-list">
    <div class="ic-comment">
        <avatar class="avatar"></avatar>
        <div class="content">
            <div class="head">用户名</div>
            <div class="post">123</div>
        </div>
    </div>
</div>
</template>

<style>
/* 注意：评论样式不在 scope 之内，故意为之 */
.ic-comment {
    display: flex;
}

.ic-comment > .content > .head {
    padding-bottom: .6em;
}

.ic-comment > .content > .post {
}

.ic-comment > .content {
    flex: 1 0 0%;
    margin-left: 15px;

    border: 1px solid #ddd;
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
import Avatar from './avatar.vue'

export default {
    data () {
        return {
        }
    },
    components: {
        Avatar
    }
}
</script>

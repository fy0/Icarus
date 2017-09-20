<template>
<div class="ic-container forum-box">
    <div class="forum-topbtns">
        <a class="ic-btn keep blue" href="#">发表主题</a>
        <a class="ic-btn keep orange" href="#">板块列表</a>
        <a class="ic-btn orange" href="#">最近话题</a>
    </div>
    <div id="board-list">
        测试
    </div>
</div>
</template>

<style scoped>
.forum-box {
    ;
}

.forum-topbtns {
    display: flex;
}

.forum-topbtns > a {
    margin-right: .35em;
}

#board-list {
    margin-top: 3px;
}
</style>

<script>
export default {
    data () {
        return {
        }
    }
}
</script>

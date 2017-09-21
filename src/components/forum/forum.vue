<template>
<div class="ic-container forum-box">
    <div class="forum-topbtns">
        <a class="ic-btn keep blue" href="#">发表主题</a>
        <a class="ic-btn keep orange" href="#">板块列表</a>
        <a class="ic-btn orange" href="#">最近话题</a>
    </div>
    <div id="board-list">
        <div class="board-item" v-for="i in [1,2]">
            <div class="title">
                <h2><a href="#">水区</a></h2>
                <p>社区的哪一个大佬我没有见过？我跟他们谈笑风生！</p>
            </div>
            <div class="detail">
                <div class="count ic-eng ic-xs-hidden">
                    <span class="tip">24h</span>
                    <p class="num">1</p>
                    <p class="txt">Topics</p>
                </div>
                <div class="count ic-eng ic-xs-hidden">
                    <span class="tip">24h</span>
                    <p class="num">2</p>
                    <p class="txt">Replies</p>
                </div>
                <div class="recent ic-eng ic-md ic-hidden">
                    <span class="line"></span>
                    <strong><a href="#">root</a></strong>
                    <div class="post-content">前三十个文本</div>
                    <a href="#">...</a>
                </div>
            </div>
        </div>
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
    display: flex;
    flex-wrap: nowrap;
    flex-direction: column;
    justify-content: space-between;
}

/* 版块单项 */

.board-item {
    display: flex;
    height: 4em;
    margin-top: 0.5em;
}

.board-item > .title {
    flex: 15 0 auto;
    display: flex;
    flex-direction: column;    
    flex-basis: 0%;
    overflow: hidden;
    padding-top: 0.1em;
}

.board-item > .title > h2 {
    margin: 0px;
    flex: 1 0;
    font-size: 1em;
    font-weight: normal;
    white-space: nowrap;
    text-overflow: ellipsis;    
    overflow: hidden;
    line-height: 2em;
}

.board-item > .title > p {
    margin: 0px;
    flex: 1 0;
    font-size: 0.8em;
    color: #666;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}

.board-item .detail {
    display: flex;
    flex: 9 0 auto;
    flex-basis: 0%;
}

.board-item > .detail > .count {
    display: flex;
    position: relative;
    align-items: center;
    flex-direction: column;
    flex: 2 0 auto;
    flex-basis: 0%;
    overflow: hidden;
}

/* 板块条目 - 最近发言 */
.board-item > .detail > .recent {
    display: flex;
    flex-direction: column;
    justify-content: center;

    text-align: left;
    font-size: .75em;
    flex: 5 0 auto;
    flex-basis: 0%;
    overflow: hidden;
    position: relative;
}

.board-item > .detail > .recent > .line {
    position: absolute;
    left: 0;
    border-left: 4px solid #ccc;
    height: 85%;
    padding-left: 0;
}

.board-item > .detail > .recent > * {
    padding-left: 1.25em;
}


/* 板块条目 - 计数 */
.board-item > .detail > .count > .num {
    font-size: 1.25em;
    text-align: center;
    margin-top: 1em;
    margin-bottom: 0px;
    flex-basis: 0%;
}

.board-item > .detail > .count > .board {
    font-size: 14px;
    text-align: center;
    margin-top: 0.4em;
    margin-bottom: 0px;
    flex-basis: 0%;
}

.board-item > .detail > .count > .tip {
    position: absolute;
    font-size: .625em;
    right: 2em;
    top: .5em;
    flex-basis: 0%;
}

.board-item > .detail > .count > .txt {
    color: #777;
    font-weight: 300;
    font-size: .75em;
    margin-top: 0px;
    flex-basis: 0%;
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

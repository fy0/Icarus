<template>
<header class="ic-nav">
    <div class="ic-container ic-navbtns">
        <a class="ic-brand-heading ic-eng " href="#">Icarus</a>

        <ul class="menu-list center">
            <li class="menu-item"><a href="#">社区</a></li>
            <li class="menu-item"><a href="#">文档</a></li>
            <li class="menu-item"><a href="#">聊天室</a></li>
            <li class="menu-item"><a href="#">管理</a></li>
            <li class="menu-item"><a href="#">设置</a></li>
            <li class="menu-item"><a href="#">关于</a></li>
        </ul>

        <ul class="menu-list">
            <li class="menu-item"><a href="#">注册</a></li>
            <li class="menu-item"><a href="#">登录</a></li>
        </ul>
    </div>
</header>
</template>

<script>
export default {
    name: 'hello',
    data () {
        return {
        }
    }
}
</script>

<style scoped>
/* 横条 */

.ic-nav {
    border-bottom: 1px solid #ddd;
    margin-bottom: 15px;
    height: 40px;
}

/* 内容 */
.ic-navbtns {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: space-between;
    align-items: center;
    height: 100%;
}

/* 左侧 LOGO */

.ic-brand-heading:first-letter {
    color: #EE2433;
    font-weight: bold;
}

.ic-brand-heading {
    color: #000;
    text-decoration: none;
    white-space: nowrap;
    font-size: 1.125em;
    margin-right: 0.5em;
}

.ic-brand-heading:hover {
    color: #286090;
}

/* 中央与右侧导航 */

.menu-list {
    display: flex;
    flex-direction: row;
    margin: 0;
    padding: 0;
    flex-shrink: 0;
}

.menu-list > li {
    display: unset;
}

.menu-list.center {
    flex: 1 0 auto;
}

.menu-item > a {
    padding: .5em 1em;
    color: #777;
    text-decoration: none;
    font-size: .9em;
}

.menu-item > a:hover {
    background-color: #eee;
}

</style>

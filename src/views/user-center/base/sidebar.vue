<template>
<div>
    <div class="category">
        <span>个人中心</span>
        <ul>
            <nuxt-link tag="li" :to="{ name: 'account_notif' }" exact><a>用户提醒</a></nuxt-link>
            <li>我的帖子</li>
            <li>我的回复</li>
            <li>我的收藏</li>
        </ul>
    </div>
</div>
</template>

<style scoped>
.category > span {
    font-weight: bold;
}

.category > ul {
    list-style-type: none;
    padding-left: 0px;
}

.category > ul > li {
    padding: 10px;
}

.category > ul > li.nuxt-link-exact-active {
    font-weight: bold;
}

.category > ul > li.nuxt-link-active {
    font-weight: bold;
}
</style>

<script>

export default {
    data () {
        return {}
    },
    computed: {
        isLoginUser: function () {
            return this.$user.data // && this.$user.data.group >= this.$misc.USER_GROUP.USER
        }
    }
}
</script>

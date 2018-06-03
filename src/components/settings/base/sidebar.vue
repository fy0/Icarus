<template>
<div>
    <div class="category">
        <span>用户</span>
        <ul>
            <!-- 字典上只见“板块”，这里取为标准写法 -->
            <router-link tag="li" :to="{ name: 'setting_user_me' }" exact><a>个人信息</a></router-link>
        </ul>
    </div>

    <div class="category">
        <span>安全</span>
        <ul>
            <router-link tag="li" :to="{ name: 'setting_security_password' }" ><a>修改密码</a></router-link>
            <router-link tag="li" :to="{ name: 'setting_security_oauth' }" ><a>绑定账号</a></router-link>
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

.category > ul > li.router-link-exact-active {
    font-weight: bold;
}

.category > ul > li.router-link-active {
    font-weight: bold;
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

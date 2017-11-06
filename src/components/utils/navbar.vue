<template>
<header class="ic-nav">
    <div class="ic-container ic-navbtns">
        <a class="ic-brand-heading" href="#">Icarus</a>

        <a href="#" @click="navmenuToggle" :class="showNavmenuBtn ? 'x' : ''" class="ic-xs ic-hidden" id="navmenu-toggle-icon">
            <s class="bar"></s>
            <s class="bar"></s>
        </a>

        <transition name="custom" :enter-active-class="isXs ? 'animated fadeInRight':''">
            <div class="menu-lists" v-show="showNavmenuBtn">
                <ul class="menu-list center">
                    <router-link tag="li" class="menu-item" :to="{ name: 'forum' }" :class="navActive('forum')">
                        <a>社区</a>
                    </router-link>
                    <li class="menu-item"><a href="#">文档</a></li>
                    <li class="menu-item"><a href="#">聊天室</a></li>
                    <router-link tag="li" class="menu-item" :to="{ name: 'admin' }" :class="navActive('admin')">
                        <a>管理</a>
                    </router-link>
                    <li class="menu-item"><a href="#">设置</a></li>
                    <router-link tag="li" class="menu-item" :to="{ name: 'about' }" :class="navActive('about')">
                        <a>关于</a>
                    </router-link>
                </ul>

                <ul class="menu-list" v-if="!state.user">
                    <router-link tag="li" class="menu-item" :to="{ name: 'account_signup' }" :class="navActive('account_signup')">
                        <a>注册</a>
                    </router-link>
                    <router-link tag="li" class="menu-item" :to="{ name: 'account_signin' }" :class="navActive('account_signin')">
                        <a>登录</a>
                    </router-link>                    
                </ul>
                <ul class="menu-list" v-else>
                    <li class="menu-item"><a href="#">头像</a></li>
                    <li class="menu-item"><a href="#">{{state.user.email}}</a></li>
                    <li class="menu-item"><a href="#" @click="signout">注销</a></li>
                </ul>
            </div>
        </transition>
    </div>
    
    <!--<media :query="m.xs" @media-enter="xsEnter" @media-leave="xsLeave"></media>-->
    <media :query="m.sm" @media-enter="xsLeave" @media-leave="xsEnter"></media>
</header>
</template>


<style scoped>
/* 横条 */

.ic-nav {
    border-bottom: 1px solid #ddd;
    margin-bottom: 15px;
    height: 56px;
}

/* 内容 */
.ic-navbtns {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    z-index: 10000;
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
    font-size: 1.5em;
    margin-right: 0.5em;
    margin-top: -2px;
}

.ic-brand-heading:hover {
    color: #286090;
}

/* 中央与右侧导航 */

.menu-lists {
    display: flex;
    flex: 1 0 auto;
}

.menu-list {
    display: flex;
    flex-direction: row;
    margin: 0;
    padding: 0;
    flex-shrink: 0;
}

.menu-list.center {
    flex: 1 0 auto;
}

.menu-item {
    display: unset;
}

.menu-item > a {
    padding: .5em 1em;
    color: #777;
    text-decoration: none;
    font-size: 1em;
}

.menu-item > a:hover {
    background-color: #eee;
}

.menu-item.link-active > a {
    color: #000;
}

/* 小屏 */

@media screen and (max-width: 35.5em) {
    #navmenu-toggle-icon {
        position: absolute;
        top: 3px;
        right: 0;
        width: 34px;
        height: 34px;
    }

    #navmenu-toggle-icon > .bar {
        background-color: #777;
        display: block;
        width: 20px;
        height: 2px;
        border-radius: 100px;
        position: absolute;
        top: 18px;
        right: 7px;
        transition: all 0.5s;
    }

    #navmenu-toggle-icon .bar:first-child {
        transform: translateY(-6px);
    }

    #navmenu-toggle-icon.x .bar {
        transform: rotate(45deg);
    }

    #navmenu-toggle-icon.x .bar:first-child {
        transform: rotate(-45deg);
    }
    
    .menu-lists {
        flex-direction: column;
        align-self: flex-start;
        flex: 0 0 auto;
        margin-right: -10px;
        margin-top: 56px;

        border: 1px solid #ddd;
        background-color: #fff;
        z-index: 9999;
    }

    .menu-list {
        display: flex;
        flex-direction: column;
        margin: 0;
        padding: 0;
        flex-shrink: 0;
        align-self: flex-start;
        align-items: stretch;
        width: 100%;
    }

    .menu-list > li > a {
        display: block;
        padding: 1em 2em;
    }

    .fade-enter-active, .fade-leave-active {
        transition: opacity 1s;
    }

    .fade-enter, .fade-leave-to {
        opacity: 0;
    }
}
</style>


<script>
import Vue from 'vue'
import Media from 'vue-media'
import state from '@/state.js'
import api from '@/netapi.js'

export default {
    name: 'hello',
    data () {
        return {
            state,
            m: $.media,
            isXs: true,
            showNavmenuBtn: false
        }
    },
    mounted: function () {
    },
    methods: {
        navmenuToggle: function () {
            this.showNavmenuBtn = !this.showNavmenuBtn
        },
        xsEnter: function () {
            this.isXs = true
            this.showNavmenuBtn = false
        },
        xsLeave: function () {
            this.isXs = false
            this.showNavmenuBtn = true
        },
        navActive: function (...names) {
            for (let name of names) {
                if (this.$route.name && this.$route.name.startsWith(name)) {
                    return 'link-active'
                }
            }
            return 'flag'
        },
        signout: async function () {
            let ret = await api.user.signout()
            if (ret.code === api.retcode.SUCCESS) {
                $.message_success('登出成功')
                Vue.delete(state, 'user')
            }
        }
    },
    components: {
        Media
    }
}
</script>

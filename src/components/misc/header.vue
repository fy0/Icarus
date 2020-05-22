<template>
<header class="ic-nav">
    <div class="ic-container ic-navbtns">
        <nuxt-link :to="{name: 'index'}" class="ic-brand-heading" @dbclick="flagClick">{{config.logoText}}</nuxt-link>
        <!-- <a class="ic-brand-heading" href="/">Icarus</a> -->

        <!-- 移动端搜索框 -->
        <div class="search-box m ic-xs ic-hidden" v-if="isSearchEnable">
            <i class="icarus icon-search icon" />
            <input class="ic-input" type="text" placeholder="点此进行搜索" v-model="searchText" @keyup.enter="doSearch" />
        </div>

        <a href="#" @click="navmenuToggle" :class="showNavmenuBtn ? 'x' : ''" class="ic-xs ic-hidden" id="navmenu-toggle-icon">
            <s class="bar"></s>
            <s class="bar"></s>
        </a>

        <transition name="custom" :enter-active-class="isXs ? 'animated fadeInRight':''">
            <div class="menu-lists" v-show="showNavmenuBtn">
                <ul class="menu-list center">
                    <nuxt-link tag="li" class="menu-item" :to="{ name: 'forum' }" :class="navActive('forum', 'index')">
                        <a>论坛</a>
                    </nuxt-link>
                    <template v-if="$store.getters.BACKEND_CONFIG.WIKI_ENABLE">
                        <nuxt-link tag="li" class="menu-item" :to="{ name: 'wiki' }" :class="navActive('wiki')">
                            <a>百科</a>
                        </nuxt-link>
                    </template>
                    <li class="menu-item" v-if="false && isSiteAdmin"><a href="#">文档</a></li>
                    <li class="menu-item" v-if="false"><a href="#">聊天室</a></li>
                    <nuxt-link tag="li" v-if="userData" class="menu-item" :to="{ name: 'setting' }" :class="navActive('setting')">
                        <a>设置</a>
                    </nuxt-link>
                    <nuxt-link tag="li" v-if="isSiteAdmin" class="menu-item" :to="{ name: 'admin' }" :class="navActive('admin')">
                        <a>管理</a>
                    </nuxt-link>
                    <nuxt-link v-if="isAboutPageEnable" tag="li" class="menu-item" :to="{ name: 'about' }" :class="navActive('about')">
                        <a>关于</a>
                    </nuxt-link>
                </ul>

                <div class="search-box ic-xs-hidden" v-if="isSearchEnable">
                    <i class="icarus icon-search icon" />
                    <input class="ic-input" type="text" placeholder="点此进行搜索" v-model="searchText" @keyup.enter="doSearch" />
                </div>

                <no-ssr>
                    <ul class="menu-list" v-if="$store.getters.isInited && (!userData)">
                        <nuxt-link tag="li" class="menu-item" :to="{ name: 'account_signup' }" :class="navActive('account_signup')">
                            <a>注册</a>
                        </nuxt-link>
                        <nuxt-link tag="li" class="menu-item" :to="{ name: 'account_signin' }" :class="navActive('account_signin')">
                            <a>登录</a>
                        </nuxt-link>
                    </ul>

                    <ul class="menu-list" v-if="userData">
                        <li class="menu-item">
                            <user-link class="user-link" :nickname="false" :user="userData">
                                <avatar style="margin-right: 6px;" :user="userData" :size="28" class="avatar"></avatar>
                                <span class="user-text limit">{{userData.nickname}}</span>
                            </user-link>
                        </li>
                        <nuxt-link tag="li" class="menu-item" :to="{ name: 'account_notif' }" :class="navActive('account_signin')">
                            <a class="nav-icon" title="提醒">
                                <i class="icarus icon-bell-ring" v-if="unread"></i>
                                <ic-badge v-if="unread" style="margin-left: 6px">{{unread}}</ic-badge>
                                <i v-else class="icarus icon-bell"></i>
                            </a>
                        </nuxt-link>
                        <li class="menu-item">
                            <a title="注销" href="javascript:void(0)" class="nav-icon" @click="signout"><i class="icarus icon-logout"></i></a>
                        </li>
                        <!-- <li class="menu-item"><a href="#" @click="signout">注销</a></li> -->
                    </ul>
                </no-ssr>
            </div>
        </transition>
    </div>

    <!--<media :query="m.xs" @media-enter="xsEnter" @media-leave="xsLeave"></media>-->
    <media :query="m.sm" @media-enter="xsLeave" @media-leave="xsEnter"></media>
    <dialog-user-signout />
</header>
</template>

<style lang="scss" scoped>
/* 搜索框 */
.search-box {
    align-self: center;
    margin-right: 10px;
    position: relative;

    &.m {
        flex: 1;

        > .icon {
            top: 1px;
        }

        > input[type=text] {
            padding: 6px 5px 6px 23px;
        }
    }

    > .icon {
        left: 4px;
        top: -1px;
        font-size: 18px;
        position: absolute;
        pointer-events: none;
    }

    > input[type=text] {
        border: none;
        box-shadow: none;
        padding: 1px 5px 1px 23px;

        &:focus {
            width: 160px;
        }
        width: 28px;
    }
}

/* 横条 */

.ic-nav {
    border-bottom: 1px solid #ddd;
    height: 50px;
    background-color: $header-background-color;
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
    margin-top: -3px;
    font-weight: 300;
    font-family: PingFang SC, Lantinghei SC, Microsoft Yahei, Hiragino Sans GB, Microsoft Sans Serif, WenQuanYi Micro Hei, sans, FontAwesome, sans-serif;
}

.ic-brand-heading:hover {
    color: $link-hover-color;
}

/* 中央与右侧导航 */

.menu-lists {
    display: flex;
    flex: 1 0 auto;
    font-weight: normal;
}

.menu-list {
    display: flex;
    flex-direction: row;
    margin: 0;
    padding: 0;
    flex-shrink: 0;
    align-items: center;
}

.menu-list.center {
    flex: 1 0 auto;
}

.menu-item {
    display: unset;
}

.menu-item > a {
    padding: .5em 1em;
    color: $inactive;
    text-decoration: none;
    font-size: 1em;
}

.menu-item > a.nav-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5em 0.7em;
    height: 36.67px;
}

.menu-item > a.nav-icon > i {
    font-size: 1.5em;
    line-height: 1.2em;
}

.menu-item > a:hover {
    background-color: #eee;
}

.menu-item.link-active > a {
    color: $gray-900;
}

.menu-item > .user-link {
    padding: 4px 16px;
    display: flex;
    align-items: center;
}

/* 小屏 */

@media screen and (lt-rbp(lg)) {
    .menu-item > a.user-link {
        .user-text {
            max-width: 5em;
        }
    }
}

@media screen and (lt-rbp(sm)) {
    #navmenu-toggle-icon {
        position: absolute;
        top: 8px;
        right: 0;
        width: 34px;
        height: 34px;
    }

    #navmenu-toggle-icon > .bar {
        background-color: $gray-700;
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
        margin-top: 49px;

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

    .menu-item > .user-link > .avatar {
        display: none !important;
    }

    .menu-list > li > a {
        display: block;
        padding: 0.4em 1.6em;
        height: 36px;
        text-align: center;
    }

    .menu-item > a.user-link {
        padding: 0.4em 1.6em;

        .user-text {
            max-width: 5em;
        }
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
import Media from 'vue-media'
import { mapState, mapGetters } from 'vuex'

export default {
  data () {
    return {
      m: $.media,
      isXs: true,
      showNavmenuBtn: false,
      searchText: ''
    }
  },
  computed: {
    ...mapState([
      'config'
    ]),
    ...mapGetters([
      'isAboutPageEnable', 'isSearchEnable'
    ]),
    ...mapState('user', ['userData', 'unread']),
    ...mapGetters('user', ['isSiteAdmin'])
  },
  mounted: function () {
  },
  watch: {
    '$route' (to, from) {
      if (this.isXs) {
        this.showNavmenuBtn = false
      } else {
        this.showNavmenuBtn = true
      }
    }
  },
  methods: {
    doSearch: function () {
      // if (!this.searchText) return
      this.$router.push({
        name: 'search',
        query: {
          q: this.searchText.trim()
        }
      })
    },
    flagClick: function () {
      ;
    },
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
      this.$store.commit('dialog/SET_USER_SIGNOUT', { val: true })
    }
  },
  components: {
    Media
  }
}
</script>

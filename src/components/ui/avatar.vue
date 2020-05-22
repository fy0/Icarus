<!-- 用户头像 -->
<template>
<!-- 带链接情况 -->
<div style="display: flex; padding:3px" v-if="isLink">
    <!-- 纯占位符情况 -->
    <a class="sa-avatar" :style="style" v-if="placeholder">
    </a>
    <!-- 存在图像头像情况 -->
    <nuxt-link v-else-if="user && user.avatar" class="sa-avatar" :style="userStyle" :to="linkTo">
        <div class="ic-paper paper" :class="`ic-z${depth}`" :style="userStyle">
            <img style="width: 100%;height:100%" :src="staticUrl(user.avatar)"/>
        </div>
    </nuxt-link>
    <!-- 自动生成头像情况 -->
    <nuxt-link v-else class="sa-avatar" :style="style" :to="linkTo" >
        <div class="ic-paper paper" :class="`ic-z${depth}`">{{char}}</div>
    </nuxt-link>
</div>
<!-- 不带链接情况 -->
<div style="display: flex; padding:3px" v-else>
    <!-- 纯占位符情况 -->
    <span class="sa-avatar" :style="style" v-if="placeholder">
    </span>
    <!-- 存在图像头像情况 -->
    <span class="sa-avatar" :style="userStyle" v-if="user.avatar">
        <div class="ic-paper paper" :class="`ic-z${depth}`" style="line-height: 0">
            <img style="width: 100%;height:100%" :src="staticUrl(user.avatar)"/>
        </div>
    </span>
    <!-- 自动生成头像情况 -->
    <span v-else class="sa-avatar" :style="style">
        <div class="ic-paper paper" :class="`ic-z${depth}`">{{char}}</div>
    </span>
</div>
</template>

<style lang="scss">
/* sa: simple avatar */
.sa-avatar {
    font-weight: normal;
    text-align: center;
    user-select: none;
    border-radius: 4px;
    font-family: "Helvetica Neue",Arial,"Hiragino Sans GB","Hiragino Sans GB W3","Microsoft YaHei","Wenquanyi Micro Hei",sans-serif;
}

.sa-avatar .paper {
    color: #fff;
    border-radius: 4px;
    background-color: rgba(0, 0, 0, 0);
    font-size: calc(80%);
    overflow: hidden;
}
</style>

<script>
import murmurhash from 'murmurhash'

export default {
  props: {
    user: {},
    anonymous: {
      default: false
    },
    system: {
      default: false
    },
    placeholder: {
      default: false
    },
    isLink: {
      default: true
    },
    depth: {
      default: 0
    },
    size: {
      default: 50
    }
  },
  methods: {
    staticUrl: function (key) {
      return `${this.$store.getters.BACKEND_CONFIG.UPLOAD_STATIC_HOST}/${key}`
    }
  },
  computed: {
    linkTo: function () {
      if (this.system) {
        return ''
      } else if (this.anonymous) {
        // 未登录用户
        return {
          name: 'account_signup'
        }
      } else {
        return {
          name: 'account_userpage',
          params: { id: this.user.id }
        }
      }
    },
    char: function () {
      if (this.system) return '⚙️'
      if (this.anonymous) return '?'
      if (!this.user.nickname) return ''
      return this.user.nickname[0].toUpperCase()
    },
    userStyle: function () {
      let size = `${this.size}px`
      return {
        'width': size,
        'height': size
      }
    },
    style: function () {
      let size, fsize, bgColor
      if (this.anonymous || this.system) bgColor = '334455'
      else if (this.placeholder) bgColor = 'e9e9e9'
      else {
        if ((!this.user) || (!this.user.nickname)) return ''
        bgColor = murmurhash.v3(this.user.nickname).toString(16).slice(1, 7)
      }
      if (typeof this.size === 'string') {
        // 用于百分比模式
        // 现在还不能正常工作，因为并没有字体大小随父节点动态变化的css
        // 先只考虑纯css，那么以后再说
        size = ''
        fsize = ''
      } else {
        size = `${this.size}px`
        // 注意，这只是个备份，其实上 fsize 应为 calc 的结果，这里适用于 calc 无法使用的情况
        fsize = `${this.size - 10}px`
      }
      return {
        'width': size,
        'height': size,
        'font-size': fsize,
        'line-height': size,
        'color': 'white',
        'background-color': '#' + bgColor
      }
    }
  }
}
</script>

<!-- 用户头像 -->
<template>
<div style="display: flex" v-if="isLink">
    <a class="sa-avatar" :style="style" v-if="placeholder">
    </a>
    <router-link v-else class="sa-avatar" :style="style" :to="linkTo" >
        <mu-paper :zDepth="1" class="paper">{{char}}</mu-paper>
    </router-link>
</div>
<div style="display: flex" v-else>
    <span class="sa-avatar" :style="style" v-if="placeholder">
    </span>
    <span v-else class="sa-avatar" :style="style">
        <mu-paper :zDepth="1" class="paper">{{char}}</mu-paper>
    </span>
</div>
</template>

<style>
.sa-avatar {
    text-align: center;
    border-radius: 4px;
    user-select: none;
    font-family: "Helvetica Neue",Arial,"Hiragino Sans GB","Hiragino Sans GB W3","Microsoft YaHei","Wenquanyi Micro Hei",sans-serif;
}

.sa-avatar .paper {
    color: #fff;
    border-radius: 4px;
    background-color: rgba(0, 0, 0, 0);
    font-size: calc(80%);
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
        placeholder: {
            default: false
        },
        isLink: {
            default: true
        },
        size: {
            default: 50
        }
    },
    computed: {
        linkTo: function () {
            if (this.anonymous) {
                // 未登录用户
                return {
                    name: 'account_signup'
                }
            } else {
                return {
                    name: 'account_userpage',
                    params: {id: this.user.id}
                }
            }
        },
        char: function () {
            if (this.anonymous) return '?'
            if (!this.user.nickname) return ''
            return this.user.nickname[0].toUpperCase()
        },
        style: function () {
            let size, fsize, bgColor
            if (this.anonymous) bgColor = '334455'
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

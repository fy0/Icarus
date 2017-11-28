<!-- 用户头像 -->
<template>
<router-link class="sa-avatar" :style="style" :to="linkTo" >
    <mu-paper :zDepth="1" class="paper">{{char}}</mu-paper>
</router-link>
</template>

<style>
.sa-avatar {
    text-align: center;
    border-radius: 4px;
    user-select: none;
}

.sa-avatar .paper {
    color: #fff;
    border-radius: 4px;
    background-color: #00000000
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
                    name: 'user_page',
                    params: {id: this.user.id}
                }
            }
        },
        char: function () {
            if (this.anonymous) return '?'
            return this.user.nickname[0].toUpperCase()
        },
        style: function () {
            let size, fsize, bgColor
            if (this.anonymous) bgColor = '334455'
            else bgColor = murmurhash.v3(this.user.nickname).toString(16).slice(0, 6)
            if (typeof this.size === 'string') {
                // 用于百分比模式
                // 现在还不能正常工作，因为并没有字体大小随父节点动态变化的css
                // 先只考虑纯css，那么以后再说
                size = ''
                fsize = ''
            } else {
                size = `${this.size}px`
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

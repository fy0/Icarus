<!-- 用户头像 -->
<template>
<router-link class="sa-avatar" :to="linkTo" :style="style">{{char}}</router-link>
</template>

<style>
.sa-avatar {
    user-select: none;
    text-align: center;
    border-radius: 4px;
}
</style>

<script>
import murmurhash from 'murmurhash'

export default {
    props: {
        user: {},
        size: {
            default: 50
        }
    },
    computed: {
        linkTo: function () {
            return {
                name: 'user_page',
                params: {id: this.user.id}
            }
        },
        char: function () {
            return this.user.nickname[0].toUpperCase()
        },
        style: function () {
            let size, fsize
            let bgColor = murmurhash.v3(this.user.nickname).toString(16).slice(0, 6)
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

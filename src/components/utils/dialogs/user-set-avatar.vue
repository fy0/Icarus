<template>
<ic-dialog :show="state.dialog.userSetAvatar" :on-close="close">
    <div class="rect">点击或拖动图片至此处</div>
    <button class="ic-btn primary">取消</button>
</ic-dialog>
</template>

<style lang="scss" scoped>
.rect {
    background-color: #eee;
    padding: 30px;
}
</style>

<script>
import state from '@/state.js'

export default {
    data () {
        return {
            state
        }
    },
    methods: {
        close: function () {
            state.dialog.userSetAvatar = false
        }
    }
}
</script>

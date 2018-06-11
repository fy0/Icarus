<template>
<ic-dialog :show="state.dialog.userSetAvatar" :on-close="close">
    <template v-if="!image">
        <input type="file" ref="inputFile" @change="onFileChange" accept="image/*" class="input-file" />
        <div @click="selectFile" class="rect">点击或拖动图片至此处</div>
        <button class="ic-btn primary">取消</button>
    </template>
    <template v-else>
        <img :src="image" />
        <img :src="image2" />
        <img :src="image2" />
    </template>
</ic-dialog>
</template>

<style lang="scss" scoped>
.input-file {
    display: none;
}

.rect {
    background-color: $gray-200;
    padding: 30px;
}
</style>

<script>
import state from '@/state.js'

export default {
    data () {
        return {
            state,
            image: '',
            image2: ''
        }
    },
    methods: {
        selectFile: async function () {
            this.$refs.inputFile.click()
        },
        onFileChange: async function (e) {
            let files = e.target.files || e.dataTransfer.files
            if (!files.length) return
            this.createImage(files[0])
        },
        createImage: function (file) {
            let reader = new FileReader()
            reader.onload = (e) => {
                this.image = e.target.result
            }
            reader.readAsDataURL(file)
        },
        close: function () {
            state.dialog.userSetAvatar = false
        }
    }
}
</script>

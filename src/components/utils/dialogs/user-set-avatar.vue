<template>
<ic-dialog :show="state.dialog.userSetAvatar" :on-close="close">
    <div class="content">
        <template v-if="!image">
            <div class="up">
                <input type="file" ref="inputFile" @change="onFileChange" accept="image/*" class="input-file" />
                <div @click="selectFile" class="rect">点击或拖动图片至此处</div>
            </div>
            <div class="down">
                <button class="ic-btn primary">取消</button>
            </div>
        </template>
        <template v-else>
            <div class="up">
                <div class="img-container">
                    <img :src="image" />
                </div>
                <div class="vicp-range">
                    <input class="ic-input primary" type="range" step="1" min="0" max="100" value="68">
                    <i class="vicp-icon5"></i>
                    <i class="vicp-icon6"></i>
                </div>
                <img :src="image2" />
                <img :src="image2" />
            </div>
            <div class="down">
                <button class="ic-btn primary">取消</button>
            </div>
        </template>
    </div>
</ic-dialog>
</template>

<style lang="scss" scoped>
.content {
    display: flex;
    flex-direction: column;

    .down {
        margin-top: 20px;
        display: flex;
        justify-content: flex-end;
    }
}

.img-container {
    width: 240px;
    height: 180px;
    overflow: hidden;
}

.input-file {
    display: none;
}

.rect {
    text-align: center;
    background-color: $gray-200;
    padding: 80px 0;
    margin-bottom: 60px;
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

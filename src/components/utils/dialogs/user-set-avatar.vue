<template>
<ic-dialog :show="state.dialog.userSetAvatar" :on-close="close">
    <div class="content">
        <template v-if="!image">
            <div class="up">
                <input type="file" ref="inputFile" @change="onFileChange" accept="image/*" class="input-file" />
                <div @click="selectFile" class="rect">
                    <i class="icon1">
                        <i class="arrow"></i>
                        <i class="body"></i>
                        <i class="bottom"></i>
                    </i>
                    <span>点击或拖动图片至此处</span>
                </div>
            </div>
            <div class="down">
                <button class="ic-btn primary">取消</button>
            </div>
        </template>
        <template v-else>
            <div class="up">
                <div class="left">
                    <div class="img-container">
                        <img @load="imgChanged" ref="img" :style="imgStyle" :src="image" />
                    </div>
                    <div class="range-area">
                        <input class="ic-input primary" type="range" step="1" min="0" max="100" value="68">
                        <i class="icon5"></i>
                        <i class="icon6"></i>
                    </div>
                </div>
                <div class="right">
                    <img :src="image2" />
                    <img :src="image2" />
                    123
                </div>
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

    .up {
        display: flex;

        .right {
            flex: 1 0 0%;
        }
    }

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
    flex: 1 0 0%;
    text-align: center;
    background-color: $gray-200;
    padding: 60px 0;
    margin-bottom: 60px;
}

.range-area {
    position: relative;
    margin: 30px 0 10px 0;
    width: 240px;
    height: 18px;
}

.icon5,
.icon6 {
    position: absolute;
    top: -2px;
    width: 18px;
    height: 18px;
    border-radius: 100%;
    background-color: rgba(#000, 0.08);

    &:hover {
        @include bs1;
        cursor: pointer;
        background-color: rgba(#000, 0.14);
    }
}

// 上传图标
$i_c: rgba(#000, 0.3);
$i_w: 42px;
$i_h: 42px;

.icon1 {
    display: block;
    margin: 0 auto 6px;
    width: $i_w;
    height: $i_h;
    overflow: hidden;

    .arrow {
        display: block;
        margin: 0 auto;
        width: 0;
        height: 0;
        border-bottom: $i_h * 0.35 solid $i_c;
        border-left: $i_h * 0.35 solid transparent;
        border-right: $i_h * 0.35 solid transparent;
    }

    .body {
        display: block;
        width: $i_w * 0.3;
        height: $i_h * 0.35;
        margin: 0 auto;
        background-color: $i_c;
    }

    .bottom {
        box-sizing: border-box;
        display: block;
        height: $i_h * 0.3;
        border: 6px solid $i_c;
        border-top: none;
    }
}


// 减号
.icon5 {
    left: 0;

    &::before {
        position: absolute;
        content: '';
        display: block;
        left: 3px;
        top: 8px;
        width: 12px;
        height: 2px;
        background-color: #fff;
    }
}
// 加号
.icon6 {
    right: 0;

    &::before {
        position: absolute;
        content: '';
        display: block;
        left: 3px;
        top: 8px;
        width: 12px;
        height: 2px;
        background-color: #fff;
    }

    &::after {
        position: absolute;
        content: '';
        display: block;
        top: 3px;
        left: 8px;
        width: 2px;
        height: 12px;
        background-color: #fff;
    }
}


</style>

<script>
import state from '@/state.js'

export default {
    data () {
        return {
            state,
            image: '',
            image2: '',
            imgWidth: 0,
            imgHeight: 0,
            camera: {
                w: 240,
                h: 180,
                top: 0,
                left: 0
            }
        }
    },
    computed: {
        imgStyle: function () {
            return {
                top: `${this.camera.top}px`,
                left: `${this.camera.left}px`,
                width: `${this.camera.w}px`,
                height: `${this.camera.h}px`
            }
        }
    },
    methods: {
        selectFile: async function () {
            this.$refs.inputFile.click()
        },
        imgChanged: function (e) {
            this.imgWidth = e.target.naturalWidth
            this.imgWidth = e.target.naturalHeight
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

<template>
<ic-dialog title="设置头像" v-model="userSetAvatar" :show-button-area="false" :on-close="close" :allow-outside-close="false">
    <div class="content">
        <template v-if="loading">
            <div class="user-set-avatar-loading">
                <line-scale-pulse-out-loader :color="'#5599F9'" :size="'50px'"/>
                <span>应用中 ...</span>
            </div>
        </template>
        <template v-else-if="!image">
            <div class="up">
                <div class="box">
                    <input type="file" ref="inputFile" @change="onFileChange" accept="image/*" class="input-file" />
                    <div @click="selectFile" class="rect">
                        <i class="icon1">
                            <i class="arrow"></i>
                            <i class="body"></i>
                            <i class="bottom"></i>
                        </i>
                        <span>点击或拖动图片至此处</span>
                    </div>
                    <div v-show="tooSmall" style="color: red; text-align: center">× 图片最低像素为（宽*高）：200*200</div>
                </div>
            </div>
            <div class="down">
                <button class="ic-btn primary" @click="close">取消</button>
            </div>
        </template>
        <template v-else>
            <div class="up">
                <div class="left">
                    <div class="img-container">
                        <div class="shade left"></div>
                        <div class="shade right"></div>
                        <img @load="imgChanged" @mousedown.prevent="cameraMoveStart" @touchstart.prevent="cameraMoveStart"
                            @mouseout="cameraMoveEnd" @mouseup="cameraMoveEnd" @touchend="cameraMoveEnd"
                            @touchcancel="cameraMoveEnd" @mousemove="cameraMove" @touchmove="cameraMove"
                            ref="img" :style="imgStyle" :src="image" />
                    </div>
                    <div class="range-area">
                        <input class="ic-input primary" type="range" step="1" min="0" max="100" v-model="scale">
                        <i class="icon5"></i>
                        <i class="icon6"></i>
                    </div>
                </div>
                <div class="right">
                    <div class="preview-item rect" style="margin-left: 100px;">
                        <img :src="imageResult" />
                        <span class="text">预览</span>
                    </div>
                    <div class="preview-item circle" style="margin-right: 100px;">
                        <img :src="imageResult" />
                        <span class="text">预览</span>
                    </div>
                </div>
            </div>
            <canvas style="display: none" :width="imgBox.h" :height="imgBox.h" ref="canvas" />
            <div class="down">
                <button class="ic-btn primary" @click="backToStep1">返回</button>
                <button class="ic-btn primary" @click="saveAvatarImage">保存</button>
            </div>
        </template>
    </div>
</ic-dialog>
</template>

<style lang="scss">
.user-set-avatar-loading {
    .vue-loaders > * {
        // 这个必须暴露于全局
        background-color: $icarus !important;
    }
}
</style>

<style lang="scss" scoped>
.user-set-avatar-loading {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.preview-item {
    width: 100px;
    height: 100px;
    display: flex;
    flex-direction: column;

    img {
        width: 100%;
        height: 100%;
    }

    .text {
        color: $gray-600;
        margin-top: 10px;
        width: 100%;
        text-align: center;
    }

    &.rect {
        img {
            padding: 3px;
            background-color: #fff;
            border: 1px solid rgba(0, 0, 0, 0.15);
        }
    }

    &.circle {
        img {
            border-radius: 100%;
            padding: 3px;
            background-color: #fff;
            border: 1px solid rgba(0, 0, 0, 0.15);
        }
    }
}

.content {
    // width: 580px;
    height: 295px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    .up {
        display: flex;

        .box {
            width: 100%;
            display: flex;
            flex-direction: column;

            .rect {
                flex: 1 0 0%;
                text-align: center;
                background-color: $gray-200;
                padding: 60px 0;
            }
        }

        .right {
            // margin: 0 0 0 80px;
            flex: 1 0 0%;
            display: flex;
            justify-content: space-between;
        }
    }

    .down {
        .ic-btn {
            margin-left: 10px;
            padding-left: 25px;
            padding-right: 25px;
        }

        margin-top: 20px;
        display: flex;
        justify-content: flex-end;
    }
}

.img-container {
    width: 260px;
    height: 200px;
    overflow: hidden;
    position: relative;

    img {
        position: absolute;
    }

    .shade {
        z-index: 1;
        position: absolute;
        box-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.18);
        background-color: rgba(241, 242, 243, 0.8);
        width: 30px; // (260-200)/2
        pointer-events: none;

        &.left {
            height: 100%;
            width: 30px;
        }

        &.right {
            height: 100%;
            width: 30px;
            right: 0;
        }
    }
}

.input-file {
    display: none;
}

.range-area {
    position: relative;
    margin: 30px 0 10px 0;
    width: 260px;
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
import { mapState } from 'vuex'
import * as qiniu from 'qiniu-js'
import { retcode } from 'slim-tools'
import { asyncGetUploadToken } from '@/utils/upload'

export default {
  data () {
    return {
      image: '',
      imageResult: '',
      loading: false,

      tooSmall: false,
      offsetX: 0,
      offsetY: 0,
      shadeWidth: 30,

      scale: 0,

      imgBox: {
        w: 260,
        h: 200
      },

      imgMax: {
        w: 0,
        h: 0
      },

      imgMin: {
        w: 0,
        h: 0
      },

      camera: {
        top: 0,
        left: 0,
        w: 0,
        h: 0,

        moving: false,
        movePoint: { x: 0, y: 0 }
      }
    }
  },
  computed: {
    ...mapState('dialog', [
      'userSetAvatar'
    ]),
    imgStyle: function () {
      return {
        top: `${this.camera.top}px`,
        left: `${this.camera.left}px`,
        width: `${this.camera.w}px`,
        height: `${this.camera.h}px`,
        transform: `translate(${-this.offsetX}px, ${-this.offsetY}px)`
      }
    }
  },
  watch: {
    scale: function (val) {
      let ncw = (this.imgMax.w - this.imgMin.w) * (val / 100) + this.imgMin.w
      let nch = (this.imgMax.h - this.imgMin.h) * (val / 100) + this.imgMin.h
      this.camera.left -= (ncw - this.camera.w) / 2
      this.camera.top -= (nch - this.camera.h) / 2
      this.camera.w = ncw
      this.camera.h = nch
      this.debounceRefreshResult()
    },
    'camera.left': function (val) {
      let ocx = this.camera.w - this.imgMin.w
      this.camera.left = -this.clamp(-val, -this.offsetX - this.shadeWidth, this.offsetX + this.shadeWidth + ocx)
    },
    'camera.top': function (val) {
      let ocy = this.camera.h - this.imgMin.h
      this.camera.top = -this.clamp(-val, -this.offsetY, this.offsetY + ocy)
    }
  },
  methods: {
    backToStep1: function () {
      this.image = ''
    },
    clamp: function (val, a, b) {
      if (val < a) return a
      if (val > b) return b
      return val
    },
    selectFile: async function () {
      this.$refs.inputFile.click()
    },
    cameraMoveStart: function (e) {
      this.camera.movePoint.x = e.clientX
      this.camera.movePoint.y = e.clientY
      this.camera.moving = true
    },
    cameraMoveEnd: function (e) {
      this.camera.moving = false
      this.refreshResult()
    },
    refreshResult: function () {
      let width = this.imgBox.h
      let img = this.$refs.img
      let canvas = this.$refs.canvas
      let ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, width, width)

      let factor = this.imgMax.w / this.camera.w
      ctx.drawImage(img,
        (-this.camera.left + this.offsetX + this.shadeWidth) * factor,
        (-this.camera.top + this.offsetY) * factor,
        width * factor, width * factor, 0, 0, width, width)
      this.imageResult = canvas.toDataURL('image/png')
    },
    debounceRefreshResult: _.debounce(function () {
      this.refreshResult()
    }, 500),
    cameraMove: function (e) {
      if (this.camera.moving) {
        this.camera.left += e.clientX - this.camera.movePoint.x
        this.camera.top += e.clientY - this.camera.movePoint.y
        this.camera.movePoint.x = e.clientX
        this.camera.movePoint.y = e.clientY
      }
    },
    imgChanged: function (e) {
      this.scale = 0
      if (e.target.naturalWidth < 200 || e.target.naturalHeight < 200) {
        this.image = ''
        this.tooSmall = true
        return
      }
      this.tooSmall = false
      this.imgMax.w = e.target.naturalWidth
      this.imgMax.h = e.target.naturalHeight

      let ratioImg = this.imgMax.w / this.imgMax.h
      let ratioStd = this.imgBox.w / this.imgBox.h

      if (ratioImg > ratioStd) {
        // 横向宽于标准尺寸
        this.imgMin.w = this.imgBox.h * ratioImg
        this.imgMin.h = this.imgBox.h
        this.offsetX = (this.imgMin.w - this.imgBox.w) / 2
        this.offsetY = 0
      } else if (ratioImg < ratioStd) {
        // 横向窄于标准尺寸
        if (ratioImg === 1) {
          // 正方形
          this.imgMin.w = this.imgBox.h
          this.imgMin.h = this.imgBox.h
          this.offsetX = (this.imgMin.w - this.imgBox.w) / 2
          this.offsetY = (this.imgMin.h - this.imgBox.h) / 2
        } else {
          // 长方形
          this.imgMin.w = this.imgBox.w
          this.imgMin.h = this.imgBox.w / ratioImg
          this.offsetX = 0
          this.offsetY = (this.imgMin.h - this.imgBox.h) / 2
        }
      } else {
        // 正好标准比例
        this.imgMin.w = this.imgBox.w
        this.imgMin.h = this.imgBox.h
        this.offsetX = 0
        this.offsetY = 0
      }

      this.camera.w = this.imgMin.w
      this.camera.h = this.imgMin.h
      this.refreshResult()
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
        this.scale = 0
      }
      reader.readAsDataURL(file)
    },
    close: function () {
      this.image = ''
      this.imageResult = ''
      this.$dialogs.setUserAvatar(false)
    },
    saveAvatarImage: async function () {
      this.loading = true
      let pngFile = $.dataURItoBlob(this.imageResult)
      let token = await asyncGetUploadToken(true)

      if (token !== null) {
        let ob = qiniu.upload(pngFile, null, token, null)
        ob.subscribe({
          complete: (res) => {
            // 注意，这里的res是本地那个callback的结果，七牛直接转发过来了
            // console.log('done', res)
            if (res.code === retcode.SUCCESS) {
              let newData = Object.assign({}, this.$user.data)
              newData.avatar = res.data
              this.$store.commit('user/SET_USER_DATA', newData)
            }
            // TODO: 完成的效果先不弄了，直接关掉了事
            this.loading = false
            this.close()
          }
        })
      } else {
        this.$message.error('操作失败！可能是网络原因或帐户权限不够。')
        this.loading = false
        this.close()
      }
    }
  }
}
</script>

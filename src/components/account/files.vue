<template>
<div class="ic-container box">
    <div v-title>文件管理 - {{state.config.title}}</div>
    <div class="left">
        <div>
        </div>
    </div>
    <div class="right">
        <div class="file-list">
            <div>我的文件列表</div>

            <div>
                <img :src="image" />
                <input type="file" ref="inputFile" @change="onFileChange" accept="image/*" class="input-file" />
                <button @click="selectFile">上传</button>
            </div>
            
            <div>
                <div>2018.09</div>
                <div>
                    <div></div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
.input-file {
    display: none;
}

.box {
    display: flex;
    flex-direction: row;
}

.box > .left {
    display: flex;
    /* flex: 3 0 0%; */
    flex: 0 0 0%;

    /* border: 1px solid #ccc; */
    align-items: center;
    justify-content: center;
}

.box > .right {
    flex: 9 0 0%;
}

.right > .file-list {
    /* margin-left: 20px; */
}
</style>

<script>
import state from '@/state.js'
import api from '@/netapi.js'
// import * as qiniu from 'qiniu-js'

export default {
    data () {
        return {
            state,
            image: '',
            uploadToken: '',
            keyTime: 0
        }
    },
    created: async function () {
        await this.fetchData()
    },
    methods: {
        selectFile: async function () {
            this.$refs.inputFile.click()
        },
        getUploadToken: async function () {
            let offset = state.misc.BACKEND_CONFIG.UPLOAD_QINIU_DEADLINE_OFFSET - 2 * 60
            let now = Date.parse(new Date()) / 1000
            // 若 token 的有效时间降至，那么申请一个新的（2min余量）
            if ((now - this.keyTime) > offset) {
                let ret = await api.upload.token('user')
                if (ret.code === api.retcode.SUCCESS) {
                    this.keyTime = now
                    this.uploadToken = ret.data
                } else {
                    // 异常情况
                    return null
                }
            }
            return this.uploadToken
        },
        onFileChange: async function (e) {
            let files = e.target.files || e.dataTransfer.files
            if (!files.length) return
            let token = await this.getUploadToken()
            if (token !== null) {
            }
            this.createImage(files[0])
        },
        createImage: function (file) {
            let reader = new FileReader()
            reader.onload = (e) => {
                this.image = e.target.result
            }
            reader.readAsDataURL(file)
        },
        fetchData: async function () {
            let key = state.loadingGetKey(this.$route)
            this.state.loadingInc(this.$route, key)
            // let params = this.$route.query
            // this.page.curPage = params.page
            // let ret = await api.upload.token('user')

            // if (ret.code === api.retcode.SUCCESS) {
            //     // this.page = ret.data
            //     // let pageNumber = this.$route.query.page
            //     // if (pageNumber) this.commentPage = parseInt(pageNumber)
            // } else {
            //     $.message_by_code(ret.code)
            // }
            this.state.loadingDec(this.$route, key)
        }
    },
    watch: {
        '$route': 'fetchData'
    }
}
</script>

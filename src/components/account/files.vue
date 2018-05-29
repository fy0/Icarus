<template>
<div class="ic-container box">
    <div v-title>文件管理 - {{state.config.title}}</div>
    <div class="left">
        <div>
            <img :src="image" />
            <form enctype="multipart/form-data">
                <input type="file" multiple @change="onFileChange" accept="image/*" class="input-file" />
            </form>
            <button @click="doUpload">上传</button>
        </div>
    </div>
    <div class="right">
        <div class="file-list">
            <div>我的文件列表</div>
            <div>

            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
.box {
    display: flex;
    flex-direction: row;
}

.box > .left {
    display: flex;
    flex: 3 0 0%;

    border: 1px solid #ccc;
    align-items: center;
    justify-content: center;
}

.box > .right {
    flex: 9 0 0%;
}

.right > .file-list {
    margin-left: 20px;
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
            image: ''
        }
    },
    created: async function () {
        await this.fetchData()
    },
    methods: {
        doUpload: async function () {
            ;
        },
        onFileChange: function (e) {
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
        fetchData: async function () {
            let key = state.loadingGetKey(this.$route)
            this.state.loadingInc(this.$route, key)
            // let params = this.$route.query
            // this.page.curPage = params.page
            let ret = await api.upload.token('user')

            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
                // let pageNumber = this.$route.query.page
                // if (pageNumber) this.commentPage = parseInt(pageNumber)
            } else {
                $.message_by_code(ret.code)
            }
            this.state.loadingDec(this.$route, key)
        }
    },
    watch: {
        '$route': 'fetchData'
    }
}
</script>

<template>
<setting-base>
    <div v-title>个人信息 - 用户设置 - {{state.config.title}}</div>
    <h3 class="ic-header">个人信息</h3>

	<my-upload field="img"
        v-model="avatarUploadShow"
		:width="300"
		:height="300"
		url="/upload"
		:params="{}"
		:headers="{}"
		img-format="png"></my-upload>

    <div class="box">
        <div class="left">
            <div class="lbox">
                <div class="setting-item">
                    <span class="label">Email</span>
                    <div class="line">
                        <span>{{user.email}}</span>
                    </div>
                </div>

                <div class="setting-item">
                    <span class="label">昵称</span>
                    <div class="line">
                        <span>{{user.nickname}}</span>
                    </div>
                </div>

                <div class="setting-item">
                    <span class="label">帐户状态</span>
                    <div class="line">
                        <span>{{state.misc.POST_STATE_TXT[user.state]}}</span>
                    </div>
                </div>

                <div class="setting-item">
                    <span class="label">简介</span>
                    <div class="line">
                        <textarea class="ic-input commentArea" rows="5" placeholder="" v-model="user.biology" maxLength="255"></textarea>
                    </div>
                </div>

                <div class="setting-item">
                    <span class="label">URL</span>
                    <div class="line">
                        <input class="ic-input commentArea" rows="5" placeholder="" v-model="user.url" />
                    </div>
                </div>

                <div class="setting-item">
                    <span class="label">所在地</span>
                    <div class="line">
                        <input class="ic-input commentArea" rows="5" placeholder="" v-model="user.location" />
                    </div>
                </div>

                <div class="setting-item" v-if="false">
                    <span class="label">手机</span>
                    <div class="line">
                        <input class="ic-input commentArea" rows="5" placeholder="" v-model="user.phone" />
                    </div>
                </div>

                <button class="ic-btn primary">更新个人信息</button>
            </div>
        </div>
        <div class="right">
            <div class="setting-item">
                <div class="line" @click="state.dialog.userSetAvatar = true" >
                    <avatar :is-link="false" :user="user" :size="200" class="avatar"></avatar>
                </div>
            </div>

            <div class="setting-item">
                <span class="label">用户组</span>
                <div class="line">
                    <span>{{state.misc.USER_GROUP_TXT[user.group]}}</span>
                </div>
            </div>

            <div class="setting-item">
                <span class="label">注册时间</span>
                <div class="line">
                    <ic-time :ago="false" :timestamp="user.time" />
                </div>
            </div>

            <div class="setting-item">
                <span class="label">最后登录时间</span>
                <div class="line">
                    <ic-time :ago="false" :timestamp="user.key_time" />
                </div>
            </div>
            
        </div>
    </div>
</setting-base>
</template>

<style scoped>

.lbox {
    width: 85%;
}

.commentArea {
    width: 100%;
}

.setting-item {
    margin-bottom: 20px;
}

.setting-item > .label {
    font-size: 17px;
    font-weight: 500;
    display: block;
    margin-bottom: 6px;
}

.box {
    display: flex;
    flex-direction: row;
}

.box > .left {
    display: flex;
    flex: 3 0 0%;

    /* border: 1px solid #ccc; */
    flex-direction: column;
}

.box > .right {
    flex: 1 0 0%;
}

.right > .rbox {
    margin-left: 20px;
}
</style>

<script>
// import api from '@/netapi.js'
import state from '@/state.js'
import SettingBase from '../base/base.vue'
import myUpload from 'vue-image-crop-upload'

export default {
    data () {
        return {
            state,
            avatarUploadShow: false
        }
    },
    computed: {
        'user': function () {
            return state.user
        }
    },
    methods: {
        fetchData: async function () {
            // let params = this.$route.params
            // let ret = await api.topic.get({
            //     id: params.id,
            // })
        }
    },
    created: async function () {
        let key = state.loadingGetKey(this.$route)
        this.state.loadingInc(this.$route, key)
        await this.fetchData()
        this.state.loadingDec(this.$route, key)
    },
    watch: {
        // 如果路由有变化，会再次执行该方法
        '$route': 'fetchData'
    },
    components: {
        myUpload,
        SettingBase
    }
}
</script>

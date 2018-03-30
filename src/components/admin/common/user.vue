<template>
<admin-base>
    <div v-title>用户管理 - 管理界面 - {{state.config.title}}</div>
    <div class="search-box">
        <input v-model="searchTxt" placeholder="搜索 用户名/uid/邮箱" />
        <mu-raised-button @click="doSearch()" label="搜索" class="search-btn" primary/>
    </div>
    <div>
        <ul class="ic-collection">
            <li class="item ic-collection-item" v-for="i in page.items" :key="i.id">
                <avatar :user="i" class="avatar" />
                <div class="right">
                    <user-link :user="i" />
                    <div class="info">
                        <span>注册于 <ic-time :ago="false" :timestamp="i.reg_time" /></span> ·
                        <span>{{state.misc.USER_GROUP_TXT[i.group]}}</span> ·
                        <span>{{state.misc.TOPIC_STATE_TXT[i.state]}}</span> ·
                        <i class="mdi-icarus ic-topic-manage-icon icon-sword-cross" title="管理" @click="setTopicManage(i)"></i>
                    </div>
                    <div>
                        <a @click="userPasswordReset(i)" href="javascript:void(0);">密码重置</a>
                        <a @click="userKeyReset(i)" href="javascript:void(0);">会话重置</a>
                    </div>
                </div>
            </li>
        </ul>
    </div>
    <paginator :page-info='page' :route-name='"admin_common_user"' />
</admin-base>
</template>

<style scoped>
.item {
    display: flex;
}

.item > .right {
    padding-left: 10px;
}

.search-box {
    flex: 1;
    align-items: center;
    display: flex;
}

.search-box > input {
    width: 45%;
    height: 45px;
    padding: 10px 10px;
    margin-top: 1rem;
    margin-bottom: 1rem;
    background: #FFFFFF;
    border-radius: 2px;
    border: 1px solid #ddd;
    font-size: 1.3rem;
    box-sizing: border-box;
    transition: all .2s ease;    
}

.search-box > .search-btn {
    height: 45px;
    margin-left: 10px;
}
</style>


<script>
import api from '@/netapi.js'
import swal from 'sweetalert'
import state from '@/state.js'
import AdminBase from '../base/base.vue'

export default {
    data () {
        return {
            state,
            searchTxt: '',
            page: {}
        }
    },
    methods: {
        setTopicManage: function (topic) {
            state.dialog.topicManageData = topic
            state.dialog.topicManage = true
        },
        userPasswordReset: function (user) {
            swal({
                title: '重要：密码重置操作',
                text: '请输入一个新的密码',
                content: 'input',
                dangerMode: true,
                buttons: {
                    cancel: true,
                    confirm: true
                }
            }).then((inputValue) => {
                if (inputValue === null) return false
                if (inputValue === '') {
                    // 此 API 在 swal 2.x 中移除
                    // swal.showInputError('新密码不能为空')
                    swal('新密码不能为空', '', 'warning')
                } else {
                    swal({
                        title: '',
                        text: '执行中……',
                        buttons: { confirm: false }
                    })
                    // $.post("/j/admin/user/password_reset", {user_id: self.attr('item-id'), new_password: inputValue}, function() {
                    //     swal("操作成功!", "新密码: " + inputValue, "success");
                    // });
                }
            })
        },
        userKeyReset: function (user) {
            swal({
                title: '重要：重置用户会话',
                text: '重置之后，用户的自动登录将会失效；当前登陆的用户会自动登出',
                type: 'warning',
                dangerMode: true,
                // confirmButtonColor: "#DD6B55",
                // cancelButtonText: "取消",
                // confirmButtonText: "确定，我要重置",
                buttons: {
                    cancel: true,
                    confirm: true
                }
            }).then((inputValue) => {
                if (inputValue) {
                    swal({
                        title: '',
                        text: '执行中……',
                        buttons: { confirm: false }
                    })
                }
                // $.post("/j/admin/user/password_reset", {user_id: self.attr('item-id'), new_password: inputValue}, function() {
                //     swal("操作成功!", "", "success");
                // });
            })
        },
        fetchData: async function () {
            let params = this.$route.params
            let retList = await api.user.list({
                // order: 'sticky_weight.desc,weight.desc,time.desc',
                // select: 'id, time, user_id, board_id, title, state',
                // loadfk: {'user_id': null, 'board_id': null, 'id': {'as': 's', loadfk: {'last_comment_id': {'loadfk': {'user_id': null}}}}}
            }, params.page, null, 'admin')
            if (retList.code === api.retcode.SUCCESS) {
                this.page = retList.data
            }
        }
    },
    created: async function () {
        this.state.loading++
        await this.fetchData()
        this.state.loading--
    },
    watch: {
        // 如果路由有变化，会再次执行该方法
        '$route': 'fetchData'
    },
    components: {
        AdminBase
    }
}
</script>

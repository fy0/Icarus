<template>
<div class="ic-container box">
    <div class="login">
        <h3 class="title">登录</h3>
        <form class="ic-form">
            <div class="ic-form-row">
                <label for="username">帐号/邮箱/昵称</label>
                <input type="text" name="username" id="username" v-model="info.account">
            </div>
            <div class="ic-form-row">
                <label for="password">密码</label>
                <input type="password" name="password" id="password" v-model="info.password">
            </div>
            <div class="ic-form-row">
                <input class="ic-btn green click" type="submit" name="" value="登 录">
            </div>
        </form>
    </div>
</div>
</template>

<style scoped>
.title {
    color: #444;
}

.box {
    height: 80vh;
    display: flex;
    align-items: center;
}

.login {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
}

.ic-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 320px;

    padding: 10px 30px;
    border: 1px solid #ddd;
}

.ic-form-row > * {
    width: 100%;
}

.ic-form-row {
    width: 100%;
    padding-top: 10px;
    padding-bottom: 10px;
}
</style>

<script>
export default {
    data () {
        return {
            info: {
                account: '',
                password: ''
            }
        }
    }
}
</script>

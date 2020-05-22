<template>
  <div>
    <div class="category">
      <span>用户</span>
      <ul>
        <!-- 字典上只见“板块”，这里取为标准写法 -->
        <nuxt-link tag="li" :to="{ name: 'setting_user_me' }" exact>
          <a>个人信息</a>
        </nuxt-link>
        <nuxt-link v-if="false && isLoginUser" tag="li" :to="{ name: 'setting_user_upload' }" exact>
          <a>我的上传</a>
        </nuxt-link>
        <nuxt-link
          v-if="false && isLoginUser"
          tag="li"
          :to="{ name: 'setting_user_privacy' }"
          exact
        >
          <a>隐私设置</a>
        </nuxt-link>
      </ul>
    </div>

    <div class="category">
      <span>安全</span>
      <ul>
        <nuxt-link tag="li" :to="{ name: 'setting_security_password' }">
          <a>修改密码</a>
        </nuxt-link>
        <nuxt-link v-if="false && isLoginUser" tag="li" :to="{ name: 'setting_security_oauth' }">
          <a>绑定账号</a>
        </nuxt-link>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.category > span {
  font-weight: bold;
}

.category > ul {
  list-style-type: none;
  padding-left: 0px;
}

.category > ul > li {
  padding: 10px;
}

.category > ul > li.nuxt-link-exact-active {
  font-weight: bold;
}

.category > ul > li.nuxt-link-active {
  font-weight: bold;
}
</style>

<script>
export default {
  data () {
    return {}
  },
  computed: {
    isLoginUser: function () {
      return this.$user.data // && this.$user.data.group >= this.$misc.USER_GROUP.USER
    }
  }
}
</script>

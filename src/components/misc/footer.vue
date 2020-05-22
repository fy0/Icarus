<template>
<footer class="ic-container">
    <div class="left">
        <div class="copyright">Powered by <a href="https://github.com/fy0/icarus" target="_blank">Icarus</a> 2.0.0 alpha 1 © 2019</div>
        <span>当前共有 {{$store.state.online}} 人在线</span>
    </div>
    <div class="right">
        <div v-html="extraHtml" v-if="extraHtml"></div>
    </div>
</footer>
</template>

<style lang="scss" scoped>
footer.ic-container {
    width: 100%;
    padding-top: 16px;
    padding-bottom: 24px;
    border-top: 1px solid #ddd;
    color: #999;

    display: flex;
    flex-direction: row;
    justify-content: space-between;

    > .left {
        flex: 1;
        width: 0%;
    }

    > .right {
        flex: 1;
        width: 0%;
        text-align: right;
        text-overflow: ellipsis;
        overflow: hidden;
        overflow-wrap: break-word;
    }
}

@media screen and (lt-rbp(sm)) {
    footer.ic-container {
        font-size: 12px;
        flex-direction: column;
        .copyright {
            display: inline-block;
            margin-right: 1em;
        }
        > .left, .right {
            width: 100%;
        }
        > .right {
            text-align: left;
        }
    }
}
</style>

<script>
export default {
  data () {
    return {}
  },
  computed: {
    extraHtml: function () {
      return this.$store.getters.BACKEND_CONFIG.FOOTER_EXTRA_HTML
    }
  }
}
</script>

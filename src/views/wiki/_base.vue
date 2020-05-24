<template>
  <div class="ic-container">
    <!-- <div v-title>百科 - {{config.title}}</div> -->
    <div class="wrapper">
      <div class="left-nav ic-xs-hidden">
        <div class="box ic-paper ic-z1">
          <div class="sidebar-content" v-html="marked(sidebar.content || '')"></div>
          <div class="ic-hr" style="margin: 10px 0px;"></div>
          <div class="bottom" v-if="!loading">
            <div style="font-weight: bold">
              <nuxt-link :to="{ name: 'wiki_list' }">全部文章</nuxt-link>
            </div>
            <div style="font-weight: bold">
              <nuxt-link :to="{ name: 'wiki_random' }">随机页面</nuxt-link>
            </div>

            <template v-if="isWikiAdmin">
              <div class="ic-hr" style="margin: 10px 0px;"></div>
              <div>
                <nuxt-link :to="{ name: 'wiki_article_new' }">添加文章</nuxt-link>
              </div>
              <div>
                <nuxt-link
                  :to="{ name: 'wiki_article_edit', params: {'id': this.sidebar.id }, query: { manage: true } }"
                >编辑目录</nuxt-link>
              </div>
              <div>
                <nuxt-link
                  :to="{ name: 'wiki_article_edit', params: {'id': this.mainpageId }, query: { manage: true } }"
                >编辑主页</nuxt-link>
              </div>
            </template>
          </div>
        </div>
      </div>
      <div class="right" slot="right">
        <slot />
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.left-nav > .box > .sidebar-content {
  * {
    font-size: 14px;
    margin: 0;
    max-width: 100%;
  }
  > * {
    padding: 0px 1em;
  }

  p {
    margin: 0;
  }

  blockquote {
    margin-left: 1em;
  }

  ul,
  ol {
    padding-top: 0;
    padding-bottom: 0;
    padding-left: 1em;
    margin-left: 1em;
  }

  > p > a {
    padding-left: 1em;
  }

  li {
    margin-left: 1em;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    padding: 0px 10px 3px 10px;
  }

  // 一些修改
  .img-center {
    text-align: center;
  }
}
</style>

<style lang="scss" scoped>
// .center {
//     background-color: $gray-200;
// }

$title-text-color: #777;
$title-text-active-color: darken(#373434, 0);

.wrapper {
  display: flex;
  height: 100%;
  flex: 1;

  .left-nav {
    flex: 5 1 0%;
    max-width: $page-left-max-width;
    height: 100%;
  }

  .left-nav > .box {
    // background-color: #373434;
    // height: 100%;
    margin-right: 20px;
    padding-top: 10px;
    padding-bottom: 10px;
    font-size: 14px;

    a {
      color: $title-text-color;
    }

    > .sidebar-content {
      font-size: 14px;
    }

    .bottom > * {
      padding: 0 10px;
    }

    > * {
      // padding: 10px;
      color: $title-text-color;
      background-color: $white;

      &.active {
        color: $title-text-active-color;
        border-left: 1px solid $title-text-active-color;
      }
    }
  }

  .right {
    width: 0%;
    flex: 19 1 0%;
  }
}
</style>

<script>
import { mapState, mapGetters } from 'vuex'
import { marked } from '@/utils/md.ts'
import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      marked,
      sidebar: {},
      mainpageId: null
    }
  },
  computed: {
    ...mapState(['config', 'loading']),
    ...mapGetters('user', ['isWikiAdmin'])
  },
  methods: {
    fetchData: async function () {
      let wrong = false
      let role = this.$user ? this.$user.basicRole : null

      let getSidebar = async () => {
        let ret = await this.$api.wiki.get(
          {
            flag: 1
          },
          { role }
        )

        if (ret.code === retcode.SUCCESS) {
          this.sidebar = ret.data
        } else {
          wrong = ret
        }
      }
      let getMainPage = async () => {
        let ret = await this.$api.wiki.get(
          {
            select: 'id',
            flag: 2
          },
          { role }
        )

        if (ret.code === retcode.SUCCESS) {
          this.mainpageId = ret.data.id
        } else {
          wrong = ret
        }
      }
      await Promise.all([getSidebar(), getMainPage()])

      if (wrong) {
        this.$message.byCode(wrong.code)
      }
    }
  },
  async asyncData (ctx) {
    // nuxt 组件中不能用asyncData，等等再想办法吧
  },
  created: async function () {
    this.$store.commit('LOADING_INC', 1)
    await this.fetchData()
    this.$store.commit('LOADING_DEC', 1)
  }
}
</script>

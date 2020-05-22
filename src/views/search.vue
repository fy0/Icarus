<template>
  <div class="ic-container">
    <template v-if="tooFrequent">
        <span>搜索过于频繁，请稍后再试。还需等待{{needWait}}秒。</span>
    </template>
    <template v-else-if="queryText">
        <div>以下为<b>“{{queryText}}”</b>的搜索结果，共{{info.hits.total}}条</div>
        <div class="results" v-if="info.hits.hits">
            <div class="item" v-for="(v, k) in info.hits.hits" :key="k">
                <h3 class="title limit m18">
                    <template v-if="v._source.type == $misc.POST_TYPES.COMMENT">
                        <post-link :type="v._source.related_type" :item="{id: v._source.related_id, title: v._source.related_title}" />
                    </template>
                    <template v-else>
                        <post-link :type="v._source.type" :item="v._source" :use-slot="v.highlight.title">
                            <span v-if="v.highlight.title" v-html="v.highlight.title[0]" />
                        </post-link>
                    </template>

                    <span class="suffix">
                        <template v-if="v._source.type == $misc.POST_TYPES.COMMENT">评论</template>
                        <template v-else>
                            <template v-if="v._source.main_category == 'forum'">论坛</template>
                            <template v-else-if="v._source.main_category == 'wiki'">百科</template>
                        </template>
                    </span>
                </h3>
                <div class="link">
                    <post-link :type="v._source.related_type" :item="{id: v._source.related_id, title: v._source.related_title}" :use-slot="true" v-if="v._source.type == $misc.POST_TYPES.COMMENT">
                        <span>{{getPostPath({id: v._source.related_id, title: v._source.related_title})}}</span>
                    </post-link>
                    <post-link :type="v._source.type" :item="v._source" :use-slot="true" v-else>
                        <span>{{getPostPath(v._source)}}</span>
                    </post-link>
                    <!-- <span>1234个回复，5678次查看</span> -->
                </div>
                <div class="brief" v-if="v.highlight.content" v-html="v.highlight.content[0]"></div>
                <div class="info">
                    <ic-time :timestamp="v._source.time / 1000" :ago="false" />
                    <span> - </span>
                    <post-link :type="$misc.POST_TYPES.USER" :item="{id: v._source.user_id, nickname: v._source.user_nickname}" />
                </div>
            </div>
        </div>
    </template>
    <template v-else>没有指定搜索的关键字</template>
  </div>
</template>

<style lang="scss">
.results {
  > .item {
    > .title {
      em {
        font-style: normal; // 移除斜体效果
        color: $red !important;
      }

      a {
        color: $gray-700;
      }
    }
    > .brief {
      em {
        font-style: normal; // 移除斜体效果
        color: darken($red, .5) !important;
      }
    }
    > .link {
      a {
        color: $blue;
      }
    }
    > .info {
      font-weight: bold;
      color: $gray-700;
    }
  }
}
</style>

<style lang="scss" scoped>
.results {
  margin-top: 20px;
  > .item {
    > .title {
      > .suffix {
        font-size: 16px;
        margin-left: .5em;
        color: #b53b78;
      }
    }
    margin-bottom: 30px;
  }
}
</style>

<script>
import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      tooFrequent: false,
      needWait: 0,
      info: {
        hits: {}
      }
    }
  },
  head () {
    return {
      title: this.queryText ? `搜索 - ${this.queryText}` : '搜索',
      meta: [
        { hid: 'description', name: 'description', content: '文章搜索页面' }
      ]
    }
  },
  computed: {
    queryText: function () {
      return this.$route.query.q
    }
  },
  methods: {
    getPostPath: function (src) {
      let name = 'forum_topic'
      let params = { id: src.id }

      switch (src.type) {
        case this.$misc.POST_TYPES.TOPIC:
          name = 'forum_topic'; break
        case this.$misc.POST_TYPES.WIKI:
          name = 'wiki_article_by_ref'; params.ref = src.ref; break
      }

      let info = this.$router.resolve({ name, params })
      return window.location.origin + info.href
    },
    fetchData: async function () {
      this.$store.commit('LOADING_INC', 1)
      let ret = await this.$api.search.search(this.queryText)
      if (ret.code === retcode.SUCCESS) {
        this.info = ret.data
        this.tooFrequent = false
      } else if (ret.code === retcode.TOO_FREQUENT) {
        this.info = { hits: {} }
        this.tooFrequent = true
        this.needWait = ret.data
      }
      this.$store.commit('LOADING_DEC', 1)
    }
  },
  created: async function () {
    await this.fetchData()
  },
  watch: {
    '$route.query.q': async function (val) {
      await this.fetchData()
    }
  }
}
</script>

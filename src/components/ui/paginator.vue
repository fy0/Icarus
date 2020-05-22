<template>
<div>
<ul class="ic-pages" v-if="pageInfo && pageInfo.info && pageInfo.info.page_count > 1">
   <li v-if="pageInfo.first_page">
        <nuxt-link :to="toInfo(pageInfo.first_page)" class="slim">«</nuxt-link>
    </li>

    <li v-if="pageInfo.prev_page">
        <nuxt-link :to="toInfo(pageInfo.prev_page)" class="slim">‹</nuxt-link>
    </li>
    <li v-else><a href="javascript:void(0);" class="disable slim">‹</a></li>

    <li v-for="i in pageInfo.page_numbers" :key="i">
        <nuxt-link :to="toInfo(i)" :class="(pageInfo.cur_page == i) ? 'active' : ''">{{i}}</nuxt-link>
    </li>

    <li v-if="pageInfo.next_page">
        <nuxt-link :to="toInfo(pageInfo.next_page)" class="slim">›</nuxt-link>
    </li>
    <li v-else><a href="javascript:void(0);" class="disable slim">›</a></li>

    <li v-if="pageInfo.last_page">
        <nuxt-link :to="toInfo(pageInfo.last_page)" class="slim">»</nuxt-link>
    </li>
</ul>
</div>
</template>

<style scoped>
/* 分页 */
.ic-pages {
    display: flex;
    padding-left: 0px;
    list-style-type: none;
}

.ic-pages > li {
    display: flex;
    align-items: center;
}

.ic-pages > li > a {
    margin: 0 4px;
    transition: all .45s cubic-bezier(.23,1,.32,1);
}

.ic-pages > li > a:hover {
    background: rgba(0, 0, 0, 0.1)
}

.ic-pages > li > a {
    padding-left: 13px;
    padding-right: 13px;
    font-size: 16px;
    height: 32px;
    border-radius: 2px;
}

.ic-pages > li > a.active {
    background-color: #e70013;
    color: #fff;
}

.ic-pages > li > a.slim {
    color: #474a4f;
    padding-left: 8px;
    padding-right: 8px;
    font-weight: bold;
    border: .5px solid #ccc;
}

.ic-pages > li:first-child {
    margin: 0 4px 0 0;
}

.ic-pages > li:last-child {
    margin: 0 0 0 4px;
}

.ic-pages > li > a.disable {
    color: #d3d6db;
}
</style>

<script>
/*
我觉得有必要解释一下。之所以没有使用 muse-ui 的分页器，但是部分借用了其样式，是因为以下原因：

1. muse-ui 分页器左右两侧有留白，对齐上并不好看

2. muse-ui 分页器内部不是 a 标签，而是响应事件，但个人而言右键某页在新标签打开是稀松平常的事情，其分页器做不到这点。

故而不予使用，但是样式确实漂亮，因此又“借”之。
*/

export default {
  props: {
    pageInfo: Object,
    routeName: String,
    linkMethod: {
      type: String,
      default: 'params' // params, query
    },
    pageKey: {
      type: String,
      default: 'page'
    }
  },
  data () {
    return {}
  },
  methods: {
    toInfo: function (page) {
      let info = {
        name: this.routeName,
        query: {},
        params: {}
      }

      if (this.linkMethod === 'query') {
        _.assign(info.query, this.$route.query)
      } else {
        info.query = this.$route.query
      }

      info[this.linkMethod][this.pageKey] = page
      return info
    }
  }
}
</script>

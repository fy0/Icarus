<template>
<ul class="ic-pages" v-if="pageInfo && pageInfo.page_count > 1">
   <li v-if="pageInfo.first_page">
        <router-link :to="toInfo(pageInfo.first_page)" class="slim">«</router-link>
    </li>

    <li v-if="pageInfo.prev_page">
        <router-link :to="toInfo(pageInfo.prev_page)" class="slim">‹</router-link>
    </li>
    <li v-else><a href="javascript:void(0);" class="disable slim">‹</a></li>

    <li v-for="i in pageInfo.page_numbers" :key="i">
        <router-link :to="toInfo(i)" :class="(pageInfo.cur_page == i) ? 'active' : ''">{{i}}</router-link>
    </li>

    <li v-if="pageInfo.next_page">
        <router-link :to="toInfo(pageInfo.next_page)" class="slim">›</router-link>
    </li>
    <li v-else><a href="javascript:void(0);" class="disable slim">›</a></li>
    
    <li v-if="pageInfo.last_page">
        <router-link :to="toInfo(pageInfo.last_page)" class="slim">»</router-link>
    </li>
</ul>
</template>


<style scoped>
/* 分页 */
.ic-pages {
    display: flex;
    padding-left: 0px;
    list-style-type: none;
}

.ic-pages > li > a {
    margin: 0.1em 0.1em 0 0;
    border: 1px solid #eee;
    padding: 0.4em 0.65em 0.4em 0.65em;
}

.ic-pages > li > a.active {
    background-color: #0078e7;
    color: #fff;
}

.ic-pages > li > a.slim {
    padding-left: 0.4em;
    padding-right: 0.4em;
    font-weight: bold;
}

.ic-pages > li > a.disable {
    color: #aaa;
}
</style>


<script>
import state from '@/state.js'

export default {
    props: {
        pageInfo: Object,
        routeName: String,
        pageKey: {
            type: String,
            default: 'page'
        }
    },
    data () {
        return {
            state
        }
    },
    methods: {
        toInfo: function (page) {
            return {
                name: this.routeName,
                params: {
                    p: 'p',
                    [this.pageKey]: page
                }
            }
        }
    }
}
</script>

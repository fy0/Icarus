<template>
<div id="app">
    <!-- <div v-title>{{config.title}}</div> -->
    <navbar class="header"></navbar>

    <div class="center" :class="{ 'gray': isWikiPage }">
        <loading v-if="loading" />

        <transition name="fade" mode="out-in">
            <nuxt class="main" :style="loading ? { 'display': 'none'} : {}" />
        </transition>
    </div>

    <my-footer class="footer"></my-footer>
    <no-ssr>
        <ic-gotop />
    </no-ssr>
    <msg-box />
</div>
</template>

<style lang="scss" scoped>
#app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}
.center.gray {
    transition: background-color .3s ease;
    background-color: $gray-200;
}
.center {
    width: 100%;
    flex: 1;
    display: flex;
    > .main {
        flex: 1;
        width: 100%;
        padding-top: 25px;
        padding-bottom: 15px;
    }
}
@media screen and (lt-rbp(sm)) {
    .center {
        .main {
            padding-top: 20px;
        }
    }
}
</style>

<script lang="ts">
// import {
//   Component,
//   Prop,
//   Vue
// } from "nuxt-property-decorator"

// @Component({})
// export default class Card extends Vue {
//     test () {
//     }
// }
// </script>

<script lang="ts">
import Vue from "vue"
import Navbar from '@/components/misc/header.vue'
import MyFooter from '@/components/misc/footer.vue'
import MsgBox from '@/components/misc/msgbox.vue'
import { mapState } from 'vuex'

export default Vue.extend({
    name: 'app',
    data () {
        return {}
    },
    head () {
        return {
            titleTemplate: `%s - ${this.$config.title}`
        }
    },
    computed: {
        ...mapState([
            'config',
            'loading'
        ]),
        isWikiPage: function () {
            let name = this.$route.name
            if (name) {
                return name === 'wiki' || (
                    name.startsWith('wiki_') &&
                    (name !== 'wiki_article_new' && name !== 'wiki_article_edit')
                )
            }
            return false
        }
    },
    components: {
        Navbar,
        MyFooter,
        MsgBox
    }
})
</script>

<template>
<!-- 搞不懂为什么有时候加载未完成，那边就会触发渲染了，不挡一下的话会报错 -->
<span v-if="item">
    <!-- 用户 -->
    <template v-if="type === state.misc.POST_TYPES.USER">
        <span v-if="showType" class="type-name" :class="{'bold': typeBold}">{{state.misc.POST_TYPES_TXT[type]}}</span>
        <router-link :to="{ name: 'account_userpage', params: {id: item.id} }" :title="item.nickname">
            <template v-if="!useSlot">
                <template>{{item.nickname || '错误的值'}}</template>
                <span v-if="goto">[转到]</span>
            </template>
            <slot v-else />
        </router-link>
    </template>

    <!-- 板块 -->
    <template v-else-if="type === state.misc.POST_TYPES.BOARD">
        <span v-if="showType" class="type-name" :class="{'bold': typeBold}">{{state.misc.POST_TYPES_TXT[type]}}</span>
        <router-link :to="{ name: 'forum_board', params: {id: item.id} }" :title="item.name">
            <template v-if="!useSlot">
                <template>{{item.name || '错误的值'}}</template>
                <span v-if="goto">[转到]</span>
            </template>
            <slot v-else />
        </router-link>
    </template>

    <!-- 主题 -->
    <template v-else-if="type === state.misc.POST_TYPES.TOPIC">
        <span v-if="showType" class="type-name" :class="{'bold': typeBold}">{{state.misc.POST_TYPES_TXT[type]}}</span>
        <router-link :to="{ name: 'forum_topic', params: {id: item.id} }" :title="item.title">
            <template v-if="!useSlot">
                <template>{{item.title || '错误的值'}}</template>
                <span v-if="goto">[转到]</span>
            </template>
            <slot v-else />
        </router-link>
    </template>
</span>
</template>

<style scoped>
.bold {
    font-weight: bold;
}
</style>

<script>
import state from '@/state.js'

export default {
    data () {
        return {
            state
        }
    },
    props: {
        item: {},
        type: null,
        showType: {
            default: false
        },
        typeBold: {
            default: false
        },
        goto: {
            default: false
        },
        useSlot: {
            default: false
        }
    },
    methods: {
    }
}
</script>

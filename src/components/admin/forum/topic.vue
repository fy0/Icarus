<template>
<admin-base>
    <div class="search-box">
        <input v-model="searchTxt" />
        <mu-raised-button @click="doSearch()" label="搜索" class="search-btn" primary/>
    </div>    
</admin-base>
</template>

<style scoped>

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
    border: 1px solid #a4a4a4;
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
// import api from '@/netapi.js'
import state from '@/state.js'
import AdminBase from '../base/base.vue'

export default {
    data () {
        return {
            state,
            searchTxt: ''
        }
    },
    methods: {
        fetchData: async function () {
            // let params = this.$route.params
            // let ret = await api.topic.get({
            //     id: params.id,
            // })
        }
    },
    created: async function () {
        this.state.loading++
        await this.fetchData()
        this.state.loading--
    },
    components: {
        AdminBase
    }
}
</script>

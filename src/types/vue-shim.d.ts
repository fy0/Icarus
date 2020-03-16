declare module 'vue/types/vue' {
    interface Vue {
        $api: any
        $store: any
    }
}

declare module "*.vue" {
    import Vue from 'vue'
    export default Vue
}

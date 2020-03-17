declare module 'vue/types/vue' {
    interface Vue {
        $api: any
    }
}

declare module "*.vue" {
    import Vue from 'vue'
    export default Vue
}

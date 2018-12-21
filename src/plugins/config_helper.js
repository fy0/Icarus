
export default {
    install (Vue, options) {
        Object.defineProperty(Vue.prototype, '$config', {
            get () {
                return this.$store.state.config
            }
        })
    }
}

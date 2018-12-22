
export default {
    install (Vue, options) {
        Object.defineProperty(Vue.prototype, '$misc', {
            get () {
                return this.$store.state.misc
            }
        })
    }
}

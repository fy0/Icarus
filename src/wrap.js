
class BaseWrapper {
    constructor (ctx) {
        this.ctx = ctx
        this._data = {}
    }

    get $store () {
        return this.ctx.store
    }

    get $storage () {
        return this.$store.app.$storage
    }

    get $route () {
        return this.ctx.route
    }
}

let makeFetchWrapper = (cls) => {
    let FetchWrapper = new Proxy(cls, {
        construct (Target, args) {
            let ins = new Target(...args)
            return new Proxy(ins, {
                get (target, name) {
                    if (name in target._data) {
                        return target._data[name]
                    }
                    if (name in target.$route.app) {
                        return target.$route.app[name]
                    }
                    if (name in target) {
                        return target[name]
                    }
                },
                set (target, name, value) {
                    target._data[name] = value
                },
                aaaa () {
                    console.log(111)
                }
            })
        }
    })
    return FetchWrapper
}

export { BaseWrapper, makeFetchWrapper }

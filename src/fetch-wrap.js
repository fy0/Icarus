
class BaseWrapper {
  constructor (ctx) {
    this.ctx = ctx
    this._data = {}
  }

  get $route () {
    return this.ctx.route
  }

  get $store () {
    return this.ctx.store
  }

  get $param () {
    return this.ctx.store
  }

  get $storage () {
    return this.$store.app.$storage
  }
}

const makeFetchWrapper = (cls) => {
  const FetchWrapper = new Proxy(cls, {
    construct (Target, args) {
      const ins = new Target(...args)
      return new Proxy(ins, {
        get (target, name) {
          if (name in target._data) {
            return target._data[name]
          }
          if (name in target.$store.app) {
            return target.$store.app[name]
          }
          if (name in target) {
            return target[name]
          }
        },
        set (target, name, value, receiver) {
          target._data[name] = value
          return true
        }
      })
    }
  })
  return FetchWrapper
}

const createFetchWrapper = (cls, ctx) => {
  const WrapCls = makeFetchWrapper(cls)
  return new WrapCls(ctx)
}

export { BaseWrapper, makeFetchWrapper, createFetchWrapper }

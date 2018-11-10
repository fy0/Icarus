
class Tween {
    constructor (options) {
        this.running = false
        this.frame = null
        this.opts = {
            start: options.start || 0,
            end: options.end || 100,
            duration: options.duration || 500,
            tick: options.tick,
            complete: options.complete,
            easing: (t, b, c, d) => {
                if ((t /= d / 2) < 1) return c / 2 * t * t + b
                return -c / 2 * ((--t) * (t - 2) - 1) + b
            }
        }
    }

    stop () {
        this.running = false
        if (this.frame) cancelAnimationFrame(this.frame)
    }

    start () {
        this.running = true
        let firstTime = null
        let opts = this.opts

        let func = (ts) => {
            if (!this.running) return
            firstTime = firstTime || ts
            if (ts >= firstTime + opts.duration) {
                if (opts.complete) opts.complete()
                return
            }

            let elapsed = ts - firstTime
            if (opts.tick) {
                let val = opts.easing(elapsed, opts.start, opts.end - opts.start, opts.duration)
                opts.tick(val)
            }
            this.frame = requestAnimationFrame(func)
        }
        this.frame = requestAnimationFrame(func)
    }
}

let scroller = null

$.scrollTo = function (el) {
    if (!el) return
    if (scroller) scroller.stop()

    scroller = new Tween({
        start: window.pageYOffset,
        end: el.getBoundingClientRect().top + window.pageYOffset,
        duration: 500,
        tick: v => window.scrollTo(0, v),
        complete: () => { scroller = null }
    }).start()
}

$.timeout = function (delay) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve()
        }, delay)
    })
}

/**
 * Deep diff between two object, using lodash
 * @param  {Object} object Object compared
 * @param  {Object} base   Object to compare with
 * @return {Object}        Return a new object who represent the diff
 */
$.objDiff = function (object, base) {
    let changes = function (object, base) {
        return _.transform(object, (result, value, key) => {
            if (!_.isEqual(value, base[key])) {
                result[key] = (_.isObject(value) && _.isObject(base[key])) ? changes(value, base[key]) : value
            }
        })
    }
    return changes(object, base)
}

$.media = {
    xs: { maxWidth: '35.5em' },
    sm: { minWidth: '35.5em' },
    md: { minWidth: '48em' },
    lg: { minWidth: '64em' },
    xl: { minWidth: '80em' }
}

$.textLimit = (text, len) => {
    if (text.length <= len) return text
    return text.slice(0, len) + '…'
}

$.dataURItoBlob = function (dataURI) {
    // convert base64 to raw binary data held in a string
    // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
    var byteString = atob(dataURI.split(',')[1])

    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]

    // write the bytes of the string to an ArrayBuffer
    var ab = new ArrayBuffer(byteString.length)
    var ia = new Uint8Array(ab)
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i)
    }

    return new Blob([ab], { type: mimeString })
}

$.regex = {
    id: /[a-fA-F0-9]+/,
    email: /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/,
    nickname: /^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]+$/
}

$.atConvert = function (text) {
    /* eslint-disable no-control-regex */
    return text.replace(/\x01([a-zA-Z0-9]+)-(.+?)\x01/g, '<a href="javascript:userPage(\'$1\', \'$2\')">@$2</a>')
}

$.atConvert2 = function (text) {
    /* eslint-disable no-control-regex */
    return text.replace(/\x01([a-zA-Z0-9]+)-(.+?)\x01/g, '@$2')
}

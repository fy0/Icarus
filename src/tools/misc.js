import Tweezer from 'tweezer.js'

let scroller = null

$.scrollTo = function (el) {
    if (scroller) scroller.stop()
    scroller = new Tweezer({
        start: window.pageYOffset,
        end: el.getBoundingClientRect().top + window.pageYOffset,
        duration: 500
    })
        .on('tick', v => window.scrollTo(0, v))
        .on('done', () => {
            scroller = null
        })
        .begin()
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

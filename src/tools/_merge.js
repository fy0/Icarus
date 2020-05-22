import './misc.js'
import './post.js'
import './tick.js'

if (process.browser) {
  window.userPage = function (uid, nickname) {
    console.log(uid, nickname)
  }
}

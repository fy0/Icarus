import './board.js'
import './level.js'
import './message.js'
import './misc.js'
import './post.js'
import './time.js'
import './upload.js'
import './user.js'
import './tick.js'

if (process.browser) {
    window.userPage = function (uid, nickname) {
        console.log(uid, nickname)
    }
}

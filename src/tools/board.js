import Color from 'color'
import murmurhash from 'murmurhash'

$.boardColor = function (board) {
    if (board.color) {
        try {
            return Color(board.color).string()
        } catch (error) {
            try {
                const c = '#' + board.color
                return Color(c).string()
            } catch (error) {}
        }
    }
    const bgColor = murmurhash.v3(board.name).toString(16).slice(0, 6)
    return '#' + bgColor
}

$.lineStyle = function (board, key = 'border-left-color') {
    return { [key]: $.boardColor(board) }
}

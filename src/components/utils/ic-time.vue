<!-- 时间戳转时间或 xx 时间前 -->
<template>
<span>{{getTime()}}</span>
</template>

<style scoped>
</style>

<script>
export default {
    props: {
        timestamp: {}
    },
    methods: {
        DateFormat: function (d, format) {
            var date, k
            date = {
                'M+': d.getMonth() + 1,
                'd+': d.getDate(),
                'h+': d.getHours(),
                'm+': d.getMinutes(),
                's+': d.getSeconds(),
                'q+': Math.floor((d.getMonth() + 3) / 3),
                'S+': d.getMilliseconds()
            }
            if (/(y+)/i.test(format)) {
                format = format.replace(RegExp.$1, (d.getFullYear() + '').substr(4 - RegExp.$1.length))
            }
            for (k in date) {
                if (new RegExp('(' + k + ')').test(format)) {
                    format = format.replace(RegExp.$1, RegExp.$1.length === 1 ? date[k] : ('00' + date[k]).substr(('' + date[k]).length))
                }
            }
            return format
        },
        timestampToXXAgo: function (timestamp) {
            timestamp = Number(timestamp)
            if (timestamp === 0) {
                return '从未'
            }
            let date = new Date()
            let now = date.getTime() / 1000
            let offset = now - timestamp
            let str = (() => {
                switch (offset) {
                case !(offset < 30):
                    return '刚刚'
                case !(offset < 60):
                    return '一分钟内'
                case !(offset < 60 * 60):
                    return Math.floor(offset / 60) + '分钟前'
                case !(offset < 60 * 60 * 24):
                    return Math.floor(offset / (60 * 60)) + '小时前'
                case !(offset < 60 * 60 * 24 * 30):
                    return Math.floor(offset / (60 * 60 * 24)) + '天前'
                case !(offset < 60 * 60 * 24 * 30 * 12):
                    return Math.floor(offset / (60 * 60 * 24 * 30)) + '月前'
                case !(offset < 60 * 60 * 24 * 30 * 12 * 20):
                    return (offset / (60 * 60 * 24 * 30 * 12)).toFixed(1) + '年前'
                default:
                    date.setTime(timestamp * 1000)
                    return this.DateFormat(date, 'yyyy-MM-dd hh:mm')
                }
            })()
            return str
        },
        getTime: function () {
            return this.timestampToXXAgo(this.timestamp)
        }
    }
}
</script>

<!-- 时间戳转时间或 xx 时间前 -->
<template>
<span :title="getRealTime()">{{getTime()}}</span>
</template>

<style scoped>
</style>

<script>
export default {
  props: {
    timestamp: {},
    ago: {
      default: true
    }
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
    timestampToXXAgo: function (timestamp, ago = true) {
      timestamp = Number(timestamp)
      if (timestamp === 0) {
        return '从未'
      }
      let date = new Date()
      let now = date.getTime() / 1000
      let offset = now - timestamp
      let val = null

      if (ago) {
        if (isNaN(offset)) {
          val = '未知'
        } else if (offset < -60) {
          // 有时候服务器和本地时间会有些偏差，我们加个60秒容错
          val = '未来'
        } else if (offset < 30) {
          val = '刚刚'
        } else if (offset < 60) {
          val = '一分钟内'
        } else if (offset < 60 * 60) {
          val = Math.floor(offset / 60) + '分钟前'
        } else if (offset < 60 * 60 * 24) {
          val = Math.floor(offset / (60 * 60)) + '小时前'
        } else if (offset < 60 * 60 * 24 * 30) {
          val = Math.floor(offset / (60 * 60 * 24)) + '天前'
        } else if (offset < 60 * 60 * 24 * 30 * 12) {
          val = Math.floor(offset / (60 * 60 * 24 * 30)) + '月前'
        } else if (offset < 60 * 60 * 24 * 30 * 12 * 20) {
          val = (offset / (60 * 60 * 24 * 30 * 12)).toFixed(1) + '年前'
        }
      }

      if (!val) {
        date.setTime(timestamp * 1000)
        val = this.DateFormat(date, 'yyyy-MM-dd hh:mm')
      }

      return val
    },
    getTime: function () {
      return this.timestampToXXAgo(this.timestamp, this.ago)
    },
    getRealTime: function () {
      return this.timestampToXXAgo(this.timestamp, false)
    }
  }
}
</script>

<template>
  <div class="ic-topbtns-box">
    <div class="ic-topbtns">
        <div>
            <button class="ic-btn smoke outline btn-order" @blur="showOrderMenu = false" @click="showOrderMenu = !showOrderMenu">
                <i class="icon icarus" :class="orders[0][1].icon"></i>
                <span class="ic-xs-hidden">{{orders[0][1].text}}</span>
                <!-- 大概五像素的占位符，用来保证小屏幕下只显示图标时，::after不会换行 -->
                <span>&nbsp;</span>
            </button>
            <div v-show="showOrderMenu" class="order-menu">
                <button class="ic-btn smoke outline option ic-xs ic-hidden" @mousedown="changeOrderType(orders[0])">
                    <i class="icon icarus" :class="orders[0][1].icon"></i>
                    <span>{{orders[0][1].text}}</span>
                    <span>&nbsp;</span>
                </button>
                <button class="ic-btn smoke outline option" @mousedown="changeOrderType(i[0])" v-for="i in orders.slice(1)" :key="i[0]">
                    <i class="icon icarus" :class="i[1].icon"></i>
                    <span>{{i[1].text}}</span>
                    <span>&nbsp;</span>
                </button>
            </div>
        </div>
        <div class="brief ic-xs-hidden ic-md-hidden" title="板块简介" v-if="board">{{board.brief}}</div>
    </div>
    <div v-if="$user.data" style="display: flex; align-items: center;">
        <!-- <span>声望: {{state.user.repute}}</span> -->
        <div class="char-info">
            <div class="bar-area">
                <span class="level">lv. {{levelInfo.level}}</span>
                <ic-progress :show-percent-when-hover="true" class="expbar" v-model="levelInfo.cur" :title="`${levelInfo.cur}/${levelInfo.exp.level}`" :max="levelInfo.exp.level"/>
            </div>
            <div class="other">
                <span><i class="icarus icon-bulb"/> {{$user.data.exp}}</span>
                <span><i class="icarus icon-coin1"/> {{$user.data.credit}}</span>
            </div>
        </div>
        <span class="ic-btn outline orange checkin" @click="checkIn" v-if="!checkedIn">签到</span>
        <span class="ic-btn outline secondary checkin" v-else
            @mousedown="showCheckedHits1 = !showCheckedHits1" @mouseover="showCheckedHits2 = true" @mouseout="showCheckedHits2 = false"
            >{{checkedInText}}</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.brief {
  overflow: hidden;
  text-overflow: ellipsis;
  margin-left: 20px;
  flex: 1 0 0%;
  word-break: break-all;
  // 会无限撑开上级，无法给出合适的宽度，因此使用替代的多行方案
  // max-width: 515px;
  // white-space: nowrap;
  color: $gray-600;
}

.ic-btn.checkin {
  min-width: 58px;
  max-width: 58px;
  white-space: nowrap;
  padding-left: 0;
  padding-right: 0;
}

.char-info {
  display: inline-flex;
  flex-direction: column;
  margin-right: 5px;
  min-width: 120px;
  font-size: 12px;
  line-height: 16px;

  .bar-area {
    flex: 1;
    height: 16px;
    display: flex;
    align-items: center;

    .level {
      margin-right: 3px;
    }

    .expbar {
      flex: 1;
      max-height: 10px;
      padding: 1px;
      border: 1px solid $primary;
      border-radius: 3px;
      font-size: 5px !important;

      .ic-progress-bar {
        padding: 1px;
        border-radius: 2px;
      }
    }
  }

  .other {
    flex: 1;
    margin-left: 24px;

    > span {
      margin-right: 5px;

      > i {
        font-size: 12px;
      }
    }
  }
}

/* 首页由于标题居中的特殊效果上下自有间隔，其他页面需要留白 15px 实现对齐 */
.ic-topbtns-box {
  display: flex;
  padding-left: 10px;
  padding-right: 12px;
  align-items: center;
  justify-content: space-between;

  .ic-topbtns {
    display: flex;
    align-items: center;

    > a {
      display: block;
      margin-right: 6px;
    }
  }
}

.btn-order {
  &::after {
    content: "\203A";
    position: absolute;
    transform: rotate(90deg);
    margin-left: 5px;
    font-size: 24px;
  }
  border-width: 0.5px;
  padding-right: 24px;
}

.ic-btn > .icon {
  margin-right: 5px;
}

.order-menu {
  position: absolute;
  display: flex;
  flex-direction: column;
  z-index: 1;

  > * {
    padding-right: 24px;
  }

  .ic-btn.outline.option {
    border-width: 0.5px;
  }

  .ic-btn.outline.option:not(:hover) {
    background-color: $light !important;
  }

  .ic-btn.outline.option:not(:first-child) {
    border-top: none;
  }
}
</style>

<script>
import { getLevelByExp } from '@/utils/level'
import { retcode } from 'slim-tools'

export default {
  props: {
    board: null
  },
  data () {
    return {
      withSubBoardsTopic: false,
      showOrderMenu: false,
      showCheckedHits1: false,
      showCheckedHits2: false
    }
  },
  computed: {
    orders: function () {
      let query = this.$route.query
      let names = [
        // 图标稍后，这个只能使用 icon font
        { icon: 'icon-fire', text: '默认排序' },
        { icon: 'icon-time', text: '更新时间' },
        { icon: 'icon-time1', text: '发布时间' }
      ]
      let func = (order) => [order, names[order - 1]]
      switch (query.type) {
        case '2': case 2: return _.map([2, 1, 3], func)
        case '3': case 3: return _.map([3, 1, 2], func)
        default: return _.map([1, 2, 3], func)
      }
    },
    levelInfo: function () {
      return getLevelByExp(this.$user.data.exp)
    },
    checkedIn: function () {
      return this.$user.data && this.$user.data['last_check_in_time'] >= this.$misc.extra.midnight_time
    },
    checkedInText: function () {
      if (this.showCheckedHits1 || this.showCheckedHits2) {
        return `x ${this.$user.data.check_in_his}`
      }
      return '已签'
    }
  },
  methods: {
    changeOrderType: function (type) {
      let newQuery = _.clone(this.$route.query)
      newQuery.type = type
      this.$router.replace({
        name: this.$route.name,
        params: this.$route.params,
        query: newQuery
      })
    },
    checkIn: async function () {
      let ret = await this.$api.user.checkIn()
      if (ret.code === retcode.SUCCESS) {
        let newData = Object.assign({}, this.$user.data)
        newData['last_check_in_time'] = ret.data.time
        newData['check_in_his'] = ret.data.check_in_his
        newData.exp += ret.data.exp
        newData.credit += ret.data.credit
        this.$store.commit('user/SET_USER_DATA', newData)
        this.showCheckedHits2 = true
        this.$message.success(`签到成功！获得经验 ${ret.data.exp} 点，积分 ${ret.data.credit} 点，已连续签到 ${ret.data.check_in_his} 次！`, 5000)
      } else {
        this.$message.byCode(ret.code, ret.data)
      }
    },
    navActiveStrict: function (...names) {
      for (let name of names) {
        if (name === this.$route.name) {
          return 'keep'
        }
      }
      return 'flag'
    }
  }
}
</script>

<template>
<div class="test-panel" :style="panelStyle" @mouseout="mouseOut"
    @mousedown="dragStart" @mousemove="dragMove" @mouseup="dragEnd"
    @touchstart="dragStart" @touchmove="dragMove" @touchend="dragEnd"
>
    <mu-raised-button @click="hello" label="测试面板" primary/>
    <mu-raised-button @click="chat_test" label="chat.test" primary/>
    <mu-raised-button :key="i[0]" v-for="i in state.test.items" @click="i[1]" :label="i[0]" primary/>
</div>
</template>

<style>
.test-panel {
    user-select: none;
    position: fixed;
    opacity: 0.7;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 3px;
    background: #fff;
}
</style>

<script>
import ws from '@/ws.js'
import state from '@/state.js'

export default {
    data () {
        return {
            state,
            drag: null,
            top: 80,
            right: 30
        }
    },
    mounted: async function () {
        let data = JSON.parse(localStorage.getItem('_test_panel'))
        if (data) {
            this.top = data.t
            this.right = data.r
        }
    },
    computed: {
        panelStyle: function () {
            return {
                'top': `${this.top}px`,
                'right': `${this.right}px`
            }
        }
    },
    methods: {
        hello: function () {
            alert('hello!')
        },

        chat_test: async function () {
            console.log(1111)
            await ws.conn.execute('chat.test', null, (data) => {
                console.log('process', data)
            })
            console.log(222)
        },

        mouseOut: function (e) {
            if (this.drag) {
                this.dragEnd(e)
            }
        },

        dragStart: function (e) {
            if (e.touches) this.drag = [e.touches[0].clientX, e.touches[0].clientY]
            else this.drag = [e.x, e.y]
        },

        dragMove: function (e) {
            if (this.drag) {
                let [x, y] = e.touches ? [e.touches[0].clientX, e.touches[0].clientY] : [e.x, e.y]
                let offset = [x - this.drag[0], y - this.drag[1]]
                this.drag = [x, y]
                this.right -= offset[0]
                this.top += offset[1]
            }
        },

        dragEnd: function (e) {
            if (this.drag) {
                this.drag = null
                localStorage.setItem('_test_panel', JSON.stringify({'t': this.top, 'r': this.right}))
            }
        }
    }
}
</script>

<style>
</style>

<template>
<div class="dialog-wrapper" tabindex="-1" v-if="show">
    <div class="dialog-box">
        <slot />
    </div>
    <div class="dialog-overlay" @click="closeOutside"></div>
</div>
</template>

<style scoped>
.dialog-box {
    width: 75%;
    max-width: 768px;
    padding: 20px;
    background-color: #fff;
    border-radius: 2px;
    font-size: 16px;
    box-shadow: 0 19px 60px rgba(0,0,0,.298039), 0 15px 20px rgba(0,0,0,.219608);    
}

.dialog-overlay {
    background-color: #000;
    opacity: 0.4;
    animation-duration: 0.5s;
    animation-name: showOverlay;
    width: 100%;
    height: 100%;
    z-index: -1;
    position: fixed;
}

.dialog-wrapper {
    display: flex;
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    flex-direction: row;
    align-items: center;
    justify-content: center;

    z-index: 999999;
    overflow-x: hidden;
}

@keyframes showOverlay {
    0% {
        background-color: #000;
        opacity: 0;
    }

    100% {
        background-color: #000;
        opacity: 0.4;
    }
}

</style>

<script>
import state from '@/state.js'

export default {
    props: {
        'show': {
            type: Boolean,
            default: false
        },
        'customClass': {
            type: String,
            default: ''
        },
        'title': {
            type: String,
            default: '标题'
        },
        'showClose': {
            type: Boolean,
            default: true
        },
        'allowOutsideClose': {
            type: Boolean,
            default: true
        },
        'showOK': {
            type: Boolean,
            default: true
        },
        'showCancel': {
            type: Boolean,
            default: true
        },
        'confirmText': {
            type: String,
            default: '确定'
        },
        'cancelText': {
            type: String,
            default: '取消'
        },
        'onConfirm': {
            type: Function,
            default: null
        },
        'onCancel': {
            type: Function,
            default: null
        },
        'onClose': {
            type: Function,
            default: null
        },
        'animation': {
            type: String,
            default: 'default'
        },
        'width': {
            type: String,
            default: '32em'
        }
    },
    data () {
        return {
            state
        }
    },
    methods: {
        closeOutside: async function () {
            if (this.onClose) {
                this.onClose()
            }
        }
    }
}
</script>

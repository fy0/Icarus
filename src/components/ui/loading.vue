<template>
<div class="ic-container loading">
    <div class="mu-circular-progress" style="width: 60px; height: 60px;">
        <div class="mu-circle-wrapper active" style="width: 60px; height: 60px;">
            <div class="mu-circle-spinner active" style="border-color: rgb(244, 67, 54);">
                <div class="mu-circle-clipper left">
                    <div class="mu-circle" style="border-width: 2px;"></div>
                </div>
                <div class="mu-circle-gap-patch">
                    <div class="mu-circle"></div>
                </div>
                <div class="mu-circle-clipper right">
                    <div class="mu-circle" style="border-width: 2px;"></div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style lang="scss" scoped>
.loading {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}

.mu-circular-progress {
    display: inline-block;
    position: relative;
    overflow: hidden;
}

// speed factor
$sf: 1.5;

.mu-circle-wrapper {
    display: inline-block;
    position: relative;
    width: 48px;
    height: 48px;

    &.active {
        animation: container-rotate $sf*1568ms linear infinite;
    }

    .mu-circle {
        border-radius: 50%;
    }

    .left {
        float: left!important;
    }

    .right {
        float: right!important;
    }
}

.mu-circle-spinner {
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0;
    border-color: #7e57c2;
    opacity: 1;
    animation: fill-unfill-rotate $sf*5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both;
}

.mu-circle-spinner.active .mu-circle-clipper.right .mu-circle {
    animation: left-spin $sf*1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both;
}

.mu-circle-spinner.active .mu-circle-clipper.right .mu-circle {
    animation: right-spin $sf*1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both;
}

.mu-circle-clipper.left .mu-circle {
    left: 0;
    border-right-color: transparent !important;
    transform: rotate(129deg);
}

.mu-circle-clipper.right .mu-circle {
    left: -100%;
    border-left-color: transparent !important;
    transform: rotate(-129deg);
}

.mu-circle-clipper, .mu-circle-gap-patch {
    height: 100%;
    overflow: hidden;
    border-color: inherit;
}

.mu-circle-clipper {
    display: inline-block;
    position: relative;
    width: 50%;
}

.mu-circle-gap-patch {
    position: absolute;
    top: 0;
    left: 45%;
    width: 10%;
}

.mu-circle-clipper, .mu-circle-gap-patch {
    height: 100%;
    overflow: hidden;
    border-color: inherit;
}

.mu-circle-clipper {
    display: inline-block;
    position: relative;
    width: 50%;
}

.mu-circle-clipper .mu-circle {
    width: 200%;
    height: 100%;
    border-width: 3px;
    border-style: solid;
    border-color: inherit;
    border-bottom-color: transparent!important;
    border-radius: 50%;
    animation: none;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
}

@keyframes fill-unfill-rotate {
    12.5% {
        transform: rotate(135deg);
    }
    25% {
        transform: rotate(270deg);
    }
    37.5% {
        transform: rotate(405deg);
    }
    50% {
        transform: rotate(540deg);
    }
    62.5% {
        transform: rotate(675deg);
    }
    75% {
        transform: rotate(810deg);
    }
    87.5% {
        transform: rotate(945deg);
    }
    to {
        transform: rotate(1080deg);
    }
}

@keyframes container-rotate {
    to {
        transform: rotate(360deg);
    }
}

@keyframes left-spin {
    from {
        transform: rotate(130deg);
    }
    50% {
        transform: rotate(-5deg);
    }
    to {
        transform: rotate(130deg);
    }
}

@keyframes right-spin {
    from {
        transform: rotate(-130deg)
    }
    50% {
        transform: rotate(5deg)
    }
    to {
        transform: rotate(-130deg)
    }
}
</style>

<script>
export default {
  computed: {
  }
}
</script>

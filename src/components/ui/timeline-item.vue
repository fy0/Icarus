<template>
<div class="ic-timeline-item">
    <div class="misc">
        <div class="circle"></div>
        <div class="line"></div>
    </div>
    <div class="info-box">
        <div class="time">
            <slot name="time" />
        </div>
        <div class="content">
            <slot name="content" />
        </div>
    </div>
</div>
</template>

<style scoped lang="scss">
.ic-timeline {
    .ic-timeline-item:last-of-type {
        .misc {
            .line {
                display: none;
            }
        }
    }
}

.ic-timeline-item {
    display: flex;

    .misc {
        display: flex;
        flex-direction: column;
        align-items: center;

        .circle {
            border-radius: 50%;
            border: 2px solid $primary;
            width: 15px;
            height: 15px;
        }

        .line {
            border-left: 2px solid rgb(232, 232, 232);
            flex: 1;
        }
    }

    .info-box {
        flex: 1;

        .content {
            margin-left: 20px;
            padding-bottom: 20px;
        }

        .time {
            margin-left: 20px;
            font-weight: 700;
            font-size: 15px;
        }
    }
}
</style>

<script>
export default {
}
</script>

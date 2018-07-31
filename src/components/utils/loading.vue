<template>
<div class="ic-container loading">
    <div class="mu-circular-progress" style="width: 180px; height: 180px;">
        <div class="mu-circle-wrapper active" style="width: 180px; height: 180px;">
            <div class="mu-circle-spinner active" style="border-color: rgb(244, 67, 54);">
                <div class="mu-circle-clipper left">
                    <div class="mu-circle" style="border-width: 1px;"></div>
                </div>
                <div class="mu-circle-gap-patch">
                    <div class="mu-circle"></div>
                </div>
                <div class="mu-circle-clipper right">
                    <div class="mu-circle" style="border-width: 1px;"></div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
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
.mu-circle-wrapper.active {
    -webkit-animation: e 1568ms linear infinite;
    animation: e 1568ms linear infinite;
}
.mu-circle-wrapper {
    display: inline-block;
    position: relative;
    width: 48px;
    height: 48px;
}

.mu-circle-spinner {
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0;
    border-color: #7e57c2;
    opacity: 1;
    -webkit-animation: b 5332ms cubic-bezier(.4,0,.2,1) infinite both;
    animation: b 5332ms cubic-bezier(.4,0,.2,1) infinite both;
}

.mu-circle-wrapper .left {
    float: left!important;
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

.mu-circle-wrapper .right {
    float: right!important;
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



.mu-circle-spinner.active .mu-circle-clipper.right .mu-circle {
    -webkit-animation: d 1333ms cubic-bezier(.4,0,.2,1) infinite both;
    animation: d 1333ms cubic-bezier(.4,0,.2,1) infinite both;
}
.mu-circle-clipper.right .mu-circle {
    left: -100%;
    border-left-color: transparent!important;
    -webkit-transform: rotate(-129deg);
    -ms-transform: rotate(-129deg);
    transform: rotate(-129deg);
}
.mu-circle-clipper .mu-circle {
    width: 200%;
    height: 100%;
    border-width: 3px;
    border-style: solid;
    border-color: inherit;
    border-bottom-color: transparent!important;
    border-radius: 50%;
    -webkit-animation: none;
    animation: none;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
}

.mu-circle-wrapper .mu-circle {
    border-radius: 50%;
}
</style>

<script>
export default {
}
</script>

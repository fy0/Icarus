export class Tween {
  running: boolean
  frame: any
  opts: any

  constructor (options: any) {
    this.running = false
    this.frame = null
    this.opts = {
      start: options.start || 0,
      end: options.end || 100,
      duration: options.duration || 500,
      tick: options.tick,
      complete: options.complete,
      easing: (t: number, b: number, c: number, d: number) => {
        if ((t /= d / 2) < 1) return c / 2 * t * t + b
        return -c / 2 * ((--t) * (t - 2) - 1) + b
      }
    }
  }

  stop () {
    this.running = false
    if (this.frame) cancelAnimationFrame(this.frame)
  }

  start () {
    this.running = true
    let firstTime: any = null
    const opts = this.opts

    const func = (ts: number) => {
      if (!this.running) return
      firstTime = firstTime || ts
      if (ts >= firstTime + opts.duration) {
        if (opts.complete) opts.complete()
        return
      }

      const elapsed = ts - firstTime
      if (opts.tick) {
        const val = opts.easing(elapsed, opts.start, opts.end - opts.start, opts.duration)
        opts.tick(val)
      }
      this.frame = requestAnimationFrame(func)
    }
    this.frame = requestAnimationFrame(func)
  }
}

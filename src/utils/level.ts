let fibMemo: any = {}
let levelExp: number[] = []
let levelAllExp: number[] = []

function fib (num: number, memo: any = null) {
  if (fibMemo[num]) return fibMemo[num]
  if (num <= 1) return 1

  fibMemo[num] = fib(num - 1, fibMemo) + fib(num - 2, fibMemo)
  return fibMemo[num]
}

export function getLevelExp (level: number) {
  if (level < 1) return { level: 0, all: 0 }
  level -= 1
  if (levelExp.length <= level) {
    for (let i = levelExp.length; i <= level; i++) {
      levelExp[i] = fib(i) * 100
      if (i > 0) {
        levelAllExp[i] = levelAllExp[i - 1] + levelExp[i]
      } else {
        levelAllExp[i] = levelExp[i]
      }
    }
  }
  return {
    level: levelExp[level],
    all: levelAllExp[level]
  }
}

export function getLevelByExp (exp: number) {
  for (let i = 1; ;i++) {
    const val = getLevelExp(i)
    if (exp < val.all || i === 255) {
      return {
        cur: exp - getLevelExp(i - 1).all,
        level: i,
        exp: val
      }
    }
  }
}

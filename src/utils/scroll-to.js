Math.easeInOutQuad = function(t, b, c, d) {
  t /= d / 2
  if (t < 1) return c / 2 * t * t + b
  t--
  return -c / 2 * (t * (t - 2) - 1) + b
}

export function scrollTo(to, duration = 500, callback) {
  const start = window.scrollY || document.documentElement.scrollTop
  const change = to - start
  const increment = 20
  let currentTime = 0

  const animateScroll = () => {
    currentTime += increment
    const val = Math.easeInOutQuad(currentTime, start, change, duration)
    window.scrollTo(0, val)
    if (currentTime < duration) {
      setTimeout(animateScroll, increment)
    } else {
      if (callback && typeof callback === 'function') {
        callback()
      }
    }
  }

  animateScroll()
}

export function animateTo(to, duration = 500, callback) {
  const start = window.pageYOffset
  const change = to - start
  const startTime = performance.now()

  const animateScroll = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const ease = progress < 0.5 ? 4 * progress * progress * progress : (progress - 1) * (2 * progress - 2) * (2 * progress - 2) + 1

    window.scrollTo(0, start + change * ease)

    if (elapsed < duration) {
      requestAnimationFrame(animateScroll)
    } else {
      if (callback) callback()
    }
  }

  requestAnimationFrame(animateScroll)
}

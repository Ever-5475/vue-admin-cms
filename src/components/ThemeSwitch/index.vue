<template>
  <!--
    日月主题切换按钮 — 移植自 WpfGorgeousThemeSwitch
    动画原理：
    - 滑块平移: PowerEase EaseInOut → CSS cubic-bezier
    - 背景颜色渐变: EasingColorKeyFrame → CSS transition
    - 星星闪烁: ScaleTransform 关键帧循环 → CSS @keyframes
    - 光晕偏移: TranslateTransform → CSS transform
    - 云朵位移: TranslateTransform.Y → CSS transform
    - 月亮/太阳切换: 月亮初始 X=34(隐藏) → checked时 X=0(显示)
    - 太阳hover旋转: RotateTransform 30° → CSS :hover
    - 自动折叠: Clip动画 + Width动画 → CSS overflow+width
  -->
  <div class="theme-switch-wrapper">
    <label class="theme-switch" :class="{ checked: isDark, folded: autoFold && !hovering }"
      @mouseenter="onMouseEnter" @mouseleave="onMouseLeave" @click="toggle">
      <!-- 背景条 -->
      <div class="switch-bg" :class="{ dark: isDark }"></div>

      <div class="scene-layer">
        <!-- 光晕(3层) — 仿 WPF glow1/glow2/glow3 -->
        <div class="glow glow-1" :class="{ dark: isDark }"></div>
        <div class="glow glow-2" :class="{ dark: isDark }"></div>
        <div class="glow glow-3" :class="{ dark: isDark }"></div>

        <!-- 云朵 — 仿 WPF cloud1/cloud2 -->
        <div class="cloud cloud-1" :class="{ dark: isDark }">
          <svg viewBox="150 280 380 200"><path fill="rgba(255,255,255,0.53)" d="M158.99,453.56 C169.78,423.31 203.15,392.42 241.6,404.12 C262,383.72 299.3,391.57 305.3,392.78 C330.16,362.4 353.16,370 368.59,378.92 C370.8,377.87 376.54,377 381.07,376.83 C387.44,354.9 410.64,354.27 420.44,355.75 C432.85,341.48 440.28,342.84 451.88,342.33 C457.75,307.27 472.82,288.95 509.06,292.16 L526.8,292.62 L526.81,465.68 L155,465.66 Z"/></svg>
        </div>
        <div class="cloud cloud-2" :class="{ dark: isDark }">
          <svg viewBox="150 280 380 200"><path fill="white" d="M158.99,453.56 C169.78,423.31 203.15,392.42 241.6,404.12 C262,383.72 299.3,391.57 305.3,392.78 C337.22,353.76 390.5,373.44 398.9,384.98 C412.5,378.21 430,381.42 430,381.42 C436.82,362.13 456.18,352.96 465,351.59 C460.57,304 510.56,292.35 521.34,292.26 L525.94,292.62 L526.81,465.68 L155,465.66 Z"/></svg>
        </div>

        <!-- 星星 Canvas — 仿 WPF stars + star1~star5 闪烁动画 -->
        <div class="stars" :class="{ dark: isDark }">
          <span class="star s-1" :class="{ blink: isDark }"></span>
          <span class="star s-2" :class="{ blink: isDark }"></span>
          <span class="star s-3" :class="{ blink: isDark }"></span>
          <span class="star s-4" :class="{ blink: isDark }"></span>
          <span class="star s-5" :class="{ blink: isDark }"></span>
          <span class="star s-6"></span>
          <span class="star s-7"></span>
          <span class="star s-8"></span>
          <span class="star s-9"></span>
          <span class="star s-10"></span>
        </div>
      </div>

      <!-- 滑块(圆) — 仿 WPF thumb -->
      <div class="thumb" :class="{ hover: hovering && !isDark }">
        <!-- 太阳面 — 仿 WPF sun -->
        <div class="sun-face" :class="{ dark: isDark }">
          <div class="sun-highlight" :class="{ show: hovering }"></div>
        </div>
        <!-- 月亮面 — 仿 WPF moon -->
        <div class="moon-face" :class="{ dark: isDark }">
          <div class="moon-crater c-1"></div>
          <div class="moon-crater c-2"></div>
          <div class="moon-crater c-3"></div>
        </div>
      </div>

      <!-- 外框阴影 — 仿 WPF ShadowElement -->
      <div class="shadow-ring" :class="{ hidden: autoFold && !hovering }"></div>
    </label>

    <span class="theme-label" v-if="showLabel">{{ isDark ? '深色模式' : '浅色模式' }}</span>
  </div>
</template>

<script>
export default {
  name: 'ThemeSwitch',
  props: {
    value: { type: Boolean, default: false },
    autoFold: { type: Boolean, default: true },
    showLabel: { type: Boolean, default: false }
  },
  data() {
    return {
      isDark: this.value,
      hovering: false
    }
  },
  watch: {
    value(v) { this.isDark = v }
  },
  methods: {
    toggle() {
      this.isDark = !this.isDark
      this.$emit('input', this.isDark)
      this.$emit('change', this.isDark)
    },
    onMouseEnter() { this.hovering = true },
    onMouseLeave() { this.hovering = false }
  }
}
</script>

<style lang="scss" scoped>
// ========== 容器 ==========
.theme-switch-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}
.theme-label {
  font-size: 14px;
  color: #333;
  user-select: none;
}

// ========== 开关主体 ==========
.theme-switch {
  position: relative;
  display: inline-block;
  width: 80px;
  height: 40px;
  border-radius: 20px;
  cursor: pointer;
  user-select: none;
  overflow: hidden;
  -webkit-tap-highlight-color: transparent;
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);

  &.folded { width: 40px; }
}

// ===== 场景层（缩放内部控制画面） =====
.scene-layer {
  position: absolute; inset: 0;
  transform: scale(1.08);
  transform-origin: left center;
  pointer-events: none;
}

// ========== 背景条 (仿 backBorder) ==========
.switch-bg {
  position: absolute;
  inset: 0;
  border-radius: 20px;
  background: #4685C0;
  transition: background-color 0.7s cubic-bezier(0.4, 0, 0.2, 1);
  &.dark { background: #171E33; }
}

// ========== 光晕(3层) (仿 glow1/glow2/glow3) ==========
.glow {
  position: absolute;
  top: 50%;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
}
.glow-1 {
  width: 79px; height: 79px;
  background: rgba(255,255,255,0.07);
  left: 0;
  &.dark { left: 23px; }
}
.glow-2 {
  width: 67px; height: 67px;
  background: rgba(255,255,255,0.13);
  left: 0;
  &.dark { left: 35px; }
}
.glow-3 {
  width: 55px; height: 55px;
  background: rgba(255,255,255,0.13);
  left: 0;
  &.dark { left: 47px; }
}

// ========== 云朵 (仿 cloud1/cloud2) ==========
.cloud {
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 50%;
  transform: translateY(-42%);
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
  &.dark { transform: translateY(-10%); }
  svg { width: 100%; height: 100%; }
}

// ========== 星星 (仿 stars) ==========
.stars {
  position: absolute;
  inset: 0;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateY(-55%);
  &.dark { transform: translateY(4%); }
}
.star {
  position: absolute;
  width: 4px; height: 4px;
  background: white;
  clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
  transition: opacity 0.5s;
  opacity: 0;
  .dark & { opacity: 1; }
}
.s-1 { left: 18%; top: 65%; width: 5px; height: 5px; }
.s-2 { left: 30%; top: 40%; width: 3px; height: 3px; }
.s-3 { left: 42%; top: 70%; width: 4px; height: 4px; }
.s-4 { left: 58%; top: 28%; width: 3px; height: 3px; }
.s-5 { left: 72%; top: 55%; width: 3px; height: 3px; }
.s-6 { left: 12%; top: 30%; width: 2px; height: 2px; }
.s-7 { left: 52%; top: 55%; width: 2px; height: 2px; }
.s-8 { left: 65%; top: 43%; width: 2px; height: 2px; }
.s-9 { left: 80%; top: 22%; width: 2px; height: 2px; }
.s-10{ left: 25%; top: 78%; width: 2px; height: 2px; }

// 星星闪烁 (仿 star1~star5 ScaleX关键帧)
@keyframes twinkle-1 { 0%,100%{opacity:1} 40%{opacity:0.2} }
@keyframes twinkle-2 { 0%,100%{opacity:1} 50%{opacity:0.2} }
@keyframes twinkle-3 { 0%,100%{opacity:1} 45%{opacity:0.2} }
@keyframes twinkle-4 { 0%,100%{opacity:1} 35%{opacity:0.2} }
@keyframes twinkle-5 { 0%,100%{opacity:1} 55%{opacity:0.2} }
.blink.s-1 { animation: twinkle-1 3.5s ease-in-out infinite; }
.blink.s-2 { animation: twinkle-2 2.8s ease-in-out infinite 0.5s; }
.blink.s-3 { animation: twinkle-3 3.2s ease-in-out infinite 0.3s; }
.blink.s-4 { animation: twinkle-4 3.0s ease-in-out infinite 0.8s; }
.blink.s-5 { animation: twinkle-5 2.5s ease-in-out infinite 1.0s; }

// ========== 滑块 (仿 thumb) ==========
.thumb {
  position: absolute;
  top: 2px; left: 2px;
  width: 36px; height: 36px;
  border-radius: 50%;
  transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform: translateX(0);
  .checked & { transform: translateX(42px); }
  &.hover { .sun-face { transform: rotate(30deg); } }
}

// ========== 太阳面 (仿 sun) ==========
.sun-face {
  position: absolute;
  inset: 2px;
  border-radius: 50%;
  background: #F3C62B;
  overflow: hidden;
  transition: transform 0.7s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.5s;
  opacity: 1;
  .dark & { opacity: 0; transform: translateX(34px) rotate(30deg); }

  // 太阳高光渐变 (仿 highlightMask)
  &::before {
    content: '';
    position: absolute; inset: 0; border-radius: 50%;
    background: linear-gradient(135deg, rgba(255,255,255,0.5), transparent 60%);
  }
}
.sun-highlight {
  position: absolute; inset: 0; border-radius: 50%;
  opacity: 0;
  transition: opacity 0.5s;
  &.show { opacity: 1; }
}

// ========== 月亮面 (仿 moon) ==========
.moon-face {
  position: absolute;
  inset: 2px;
  border-radius: 50%;
  background: #C4C9D4;
  overflow: hidden;
  transition: transform 0.7s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.5s;
  opacity: 0;
  transform: translateX(34px);
  .dark & { opacity: 1; transform: translateX(0); }

  // 月亮渐变光泽
  &::after {
    content: '';
    position: absolute; inset: 0; border-radius: 50%;
    background: linear-gradient(180deg, rgba(255,255,255,0.3) 0%, transparent 40%);
  }
}
// 月亮陨石坑
.moon-crater {
  position: absolute;
  border-radius: 50%;
  background: #9A9FB2;
  border: 0.5px solid rgba(0,0,0,0.4);
  &.c-1 { width: 8px; height: 8px; left: 6px; top: 14px; }
  &.c-2 { width: 5px; height: 5px; left: 13px; top: 6px; }
  &.c-3 { width: 6px; height: 6px; left: 19px; top: 18px; }
}

// ========== 外框阴影 (仿 ShadowElement) ==========
.shadow-ring {
  position: absolute;
  inset: -1px;
  border-radius: 20px;
  border: 1.5px solid #5C6170;
  box-shadow: 0 0 6px rgba(0,0,0,0.25);
  transition: opacity 0.5s;
  pointer-events: none;
  &.hidden { opacity: 0; }
}
</style>

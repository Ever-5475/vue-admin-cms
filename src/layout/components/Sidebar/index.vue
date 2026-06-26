<template>
  <div :class="{'has-logo':showLogo, 'sidebar-with-theme-switch': true}">
    <logo v-if="showLogo" :collapse="isCollapse" />
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :background-color="menuColors.bg"
        :text-color="menuColors.text"
        :unique-opened="false"
        :active-text-color="menuColors.activeText"
        :collapse-transition="false"
        mode="vertical"
      >
        <sidebar-item v-for="route in routes" :key="route.path" :item="route" :base-path="route.path" />
      </el-menu>
    </el-scrollbar>

    <!-- 日月主题切换按钮（固定在侧边栏底部，收起时隐藏） -->
    <div class="theme-switch-bar" v-if="!isCollapse">
      <theme-switch v-model="isDark" @change="onThemeChange" :auto-fold="false" :show-label="false" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Logo from './Logo'
import SidebarItem from './SidebarItem'
import ThemeSwitch from '@/components/ThemeSwitch/index.vue'
import variables from '@/styles/variables.scss'

const STORAGE_KEY = 'app_theme_mode'

export default {
  components: { SidebarItem, Logo, ThemeSwitch },
  data() {
    return {
      // true = 深色（默认），false = 浅色
      isDark: true
    }
  },
  computed: {
    ...mapGetters([
      'sidebar',
      'isAdmin'
    ]),
    routes() {
      const filterRoutes = (routes) => {
        return routes.filter(route => {
          // 需要管理员权限的路由，非管理员用户过滤掉
          if (route.meta && route.meta.adminOnly && !this.isAdmin) {
            return false
          }
          // 递归过滤子路由（不修改原始路由对象）
          if (route.children && route.children.length > 0) {
            const filteredChildren = filterRoutes(route.children)
            // 如果子路由全被过滤掉了，则父路由也不显示
            return filteredChildren.length > 0
          }
          return true
        }).map(route => {
          // 返回新对象，不修改原始路由
          const newRoute = { ...route }
          if (route.children && route.children.length > 0) {
            newRoute.children = filterRoutes(route.children)
          }
          return newRoute
        })
      }
      return filterRoutes(this.$router.options.routes)
    },
    activeMenu() {
      const route = this.$route
      const { meta, path } = route
      // if set path, the sidebar will highlight the path you set
      if (meta.activeMenu) {
        return meta.activeMenu
      }
      return path
    },
    showLogo() {
      return this.$store.state.settings.sidebarLogo
    },
    variables() {
      return variables
    },
    isCollapse() {
      return !this.sidebar.opened
    },
    // 根据当前主题动态返回菜单配色
    menuColors() {
      if (this.isDark) {
        return {
          bg: variables.menuBg,
          text: variables.menuText,
          activeText: variables.menuActiveText
        }
      }
      return {
        bg: '#f4f6fa',
        text: '#303133',
        activeText: '#409EFF'
      }
    }
  },
  mounted() {
    const saved = localStorage.getItem(STORAGE_KEY)
    // 默认深色模式；如果本地存了 light 则切浅色
    this.isDark = saved !== 'light'
    this.applyTheme()
  },
  methods: {
    onThemeChange(val) {
      this.isDark = val
      localStorage.setItem(STORAGE_KEY, this.isDark ? 'dark' : 'light')
      this.applyTheme()
    },
    applyTheme() {
      const body = document.body
      body.classList.remove('theme-dark', 'theme-light')
      body.classList.add(this.isDark ? 'theme-dark' : 'theme-light')
    }
  }
}
</script>

<style lang="scss" scoped>
.theme-switch-bar {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 12px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  z-index: 10;
  background: inherit;
  display: flex;
  justify-content: center;
}

/* 浅色模式下切换按钮区域的样式（由全局 body class 驱动） */
.theme-light .theme-switch-bar {
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}
</style>

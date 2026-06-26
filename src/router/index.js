import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '主页', icon: 'el-icon-s-home' }
    }]
  },

  {
    path: '/user',
    component: Layout,
    redirect: '/user/list',
    meta: { title: '用户管理', icon: 'el-icon-user', adminOnly: true },
    children: [
      {
        path: 'list',
        name: 'UserList',
        component: () => import('@/views/user/list'),
        meta: { title: '用户列表', icon: 'el-icon-user-solid', adminOnly: true }
      },
      {
        path: 'create',
        name: 'UserCreate',
        component: () => import('@/views/user/form'),
        meta: { title: '新增用户', icon: 'el-icon-plus' },
        hidden: true
      },
      {
        path: 'edit/:id(\\d+)',
        name: 'UserEdit',
        component: () => import('@/views/user/form'),
        meta: { title: '编辑用户', icon: 'el-icon-edit' },
        hidden: true
      }
    ]
  },

  {
    path: '/article',
    component: Layout,
    redirect: '/article/list',
    meta: { title: '文章管理', icon: 'el-icon-document' },
    children: [
      {
        path: 'list',
        name: 'ArticleList',
        component: () => import('@/views/article/list'),
        meta: { title: '文章列表', icon: 'el-icon-notebook-2' }
      },
      {
        path: 'create',
        name: 'ArticleCreate',
        component: () => import('@/views/article/form'),
        meta: { title: '发布文章', icon: 'el-icon-edit-outline' },
        hidden: true
      },
      {
        path: 'edit/:id(\\d+)',
        name: 'ArticleEdit',
        component: () => import('@/views/article/form'),
        meta: { title: '编辑文章', icon: 'el-icon-edit' },
        hidden: true
      },
      {
        path: 'detail/:id(\\d+)',
        name: 'ArticleDetail',
        component: () => import('@/views/article/detail'),
        meta: { title: '文章详情', icon: 'el-icon-document' },
        hidden: true
      }
    ]
  },

  {
    path: '/report',
    component: Layout,
    redirect: '/report/index',
    meta: { title: '数据报表', icon: 'el-icon-data-analysis' },
    children: [
      {
        path: 'index',
        name: 'ReportIndex',
        component: () => import('@/views/report/index'),
        meta: { title: '综合报表', icon: 'el-icon-data-board' }
      },
      {
        path: 'article',
        name: 'ReportArticle',
        component: () => import('@/views/report/article'),
        meta: { title: '文章报表', icon: 'el-icon-document' }
      },
      {
        path: 'comment',
        name: 'ReportComment',
        component: () => import('@/views/report/comment'),
        meta: { title: '评论报表', icon: 'el-icon-chat-line-round' }
      }
    ]
  },

  {
    path: '/school',
    component: Layout,
    redirect: '/school/intro',
    meta: { title: '公司概况', icon: 'el-icon-school' },
    children: [
      {
        path: 'intro',
        name: 'SchoolIntro',
        component: () => import('@/views/school/intro'),
        meta: { title: '公司介绍', icon: 'el-icon-reading' }
      }
    ]
  },

  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    children: [
      {
        path: 'index',
        name: 'Profile',
        component: () => import('@/views/profile/index'),
        meta: { title: '个人中心', icon: 'el-icon-setting' }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router

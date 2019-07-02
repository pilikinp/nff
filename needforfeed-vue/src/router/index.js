import Vue from 'vue'
import Router from 'vue-router'

import Login from '@/components/Login'
import Registration from '@/components/Registration'

import Index from '@/components/Index'
import Meals from '@/components/Meals'
import Meal from '@/components/Meal'
import Chefs from '@/components/Chefs'
import Chef from '@/components/Chef'
import Account from '@/components/Account'
import Order from '@/components/Order'
import ChefOrders from '@/components/ChefOrders'


Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/meals',
      name: 'Meals',
      component: Meals
    },
    {
      path: '/meal/:mealId',
      name: 'Meal',
      component: Meal
    },
    {
      path: '/chefs',
      name: 'Chefs',
      component: Chefs
    },
    {
      path: '/chef/:chefId',
      name: 'Chef',
      component: Chef
    },
    {
      path: '/account/:username',
      name: 'Account',
      component: Account
    },
    {
      path: '/auth/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/auth/reg',
      name: 'Registration',
      component: Registration
    },
    {
      path: '/order',
      name: 'Order',
      component: Order
    },
    {
      path: '/chef-orders/:chefId',
      name: 'ChefOrders',
      component: ChefOrders
    }
  ]
})

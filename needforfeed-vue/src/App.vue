<template>
  <div id="app">
    <div id="page-wrapper">
      <!-- Header -->
      <section id="header" style="background-image: url('../static/images/header_bkg.jpg');background-size: cover">

        <!--<div v-if="username" class="badge badge-secondary mb2">-->

          <!--<router-link-->
            <!--:to="{name: 'Account', params: {'username': username}}">-->
            <!--<h2 :class="avatarClass">-->
              <!--{{ username}}-->
              <!--<img :src="imgPath(avatar)" class="avatar"/>-->
            <!--</h2>-->
          <!--</router-link>-->
        <!--</div>-->

        <!--<div v-if="username&&isOrder" class="badge badge-secondary mb2" style="float: right">-->
          <!--<router-link to="/order">-->
            <!--<h4 class="icon fa-shopping-basket">Корзина</h4>-->
            <!--<span style="font-size: 2em;">Всего: {{ cartAmount }}</span>-->
          <!--</router-link>-->

        <!--</div>-->

        <div class="container">

          <!-- Logo -->
          <h1 id="logo">
            <router-link to="/">NeedForFeed</router-link>
          </h1>
          <h3><p style="color: #c36753">Накормите друг-друга!</p></h3>

          <!-- Nav -->
          <nav id="nav">
            <ul>
              <li>
                <router-link to="/" class="icon fa-home"><span>Главная</span></router-link>
              </li>
              <li>
                <router-link to="/chefs" class="icon fa-users"><span>Наши повара</span></router-link>
              </li>
              <li>
                <router-link to="/meals" class="icon fa-cutlery"><span>Блюда</span></router-link>
              </li>
              <li v-if="!isToken">
                <router-link to="/auth/login" class="icon fa-user-circle"><span>Вход</span></router-link>
              </li>
              <li v-if="!isToken">
                <router-link to="/auth/reg" class="icon fa-user-circle"><span>Регистрация</span></router-link>
              </li>
              <li v-else @click.prevent="logOut">
                <a href="" class="icon fa-user-circle">Выйти</a>
              </li>
              <li v-if="username">
                <a href="#" class="icon fa-user-circle"><span>{{username}}</span></a>
                <ul>
                  <li>
                    <router-link
                      :to="{name: 'Account', params: {'username': username}}" class="list-group-item-action">
                      Личный кабинет
                      <img :src="imgPath(avatar)" class="avatar"/>
                    </router-link>
                  </li>
                  <li v-if="username&&isOrder">
                    <router-link to="/order" class="list-group-item-action">
                      Корзина: <span style="float: right">{{ cartAmount }}</span>
                    </router-link>
                  </li>
                  <li v-if="user&&user.is_producer">
                    <router-link :to="{name: 'ChefOrders', params: {'chefId': user.id}}" class="list-group-item-action">
                      Мои заказы: <span v-if="chefOrders" style="float: right">{{ chefOrders.length }}</span>
                    </router-link>
                  </li>
                </ul>
              </li>
            </ul>
          </nav>

        </div>
      </section>

      <router-view/>
    </div>
  </div>
</template>

<script>

  import Login from "./components/Login";
  import Registration from "./components/Registration";
  import Index from './components/Index'
  import axios from 'axios'

  export default {
    name: 'App',
    components: {Registration, Login, Index},

    data() {
      return {
        // serverSource: 'http://13.58.186.3',
        serverSource: 'http://127.0.0.1:8000',
        // apiUrl: 'http://13.58.186.3/api_v1/',
        apiUrl: 'http://127.0.0.1:8000/api_v1/',
        // apiAuthUrl: 'http://13.58.186.3/api_v1_auth/',
        apiAuthUrl: 'http://127.0.0.1:8000/api_v1_auth/',
        userId: +sessionStorage.getItem('userId'),
        username: sessionStorage.getItem('username'),
        token: sessionStorage.getItem('token'),
        avatar: sessionStorage.getItem('avatar'),
        order: null,
        user: null,
        chefOrders: null,

        authenticatedHeaders: {
          "Authorization": `Token ${sessionStorage.getItem('token')}`,
          "Content-Type": "application/json"
        },
        notAuthenticatedHeaders: {

          "Content-Type": "application/json"
        },
        authenticatedHeadersFile: {
          "Authorization": `Token ${sessionStorage.getItem('token')}`,
          "Content-Type": "multipart/form-data"
        },
        notAuthenticatedHeadersFile: {

          "Content-Type": "multipart/form-data"
        },
      }
    },

    computed: {
      isOrder() {
        return !!this.order
      },

      isToken() {
        if (sessionStorage.getItem('token')) {
          return true
        }
      },

      isUser() {
        return !!this.user
      },

      avatarClass() {
        return "icon fa-user-circle" ? this.avatar : ""
      },

      cartAmount() {
        let count = 0;
        if (this.order.length === 0) {
          return count
        }
        for (let item of this.order) {
          count += +item.quantity
        }
        return count
      }
    },

    methods: {
      getJson(url) {
        let _headers = this.isToken ? this.authenticatedHeaders : this.notAuthenticatedHeaders;
        return fetch(this.apiUrl + url, {
          headers: _headers
        })
          .then(result => {
              return result.json()
            }
          )
          .catch(error => {
              console.log(error);
            }
          )
      },

      postJson(url, data) {
        return fetch(this.apiUrl + url, {
          method: 'POST',
          headers: this.authenticatedHeaders,
          body: JSON.stringify(data),
        })
          .then(result => result.json())
          .catch(error => {
            console.log(error);
          })
      },

      putJson(url, data) {
        return fetch(this.apiUrl + url, {
            method: 'PUT',
            headers: this.authenticatedHeaders,
            body:
              JSON.stringify(data)
          }
        )
          .then(result => result)
          .catch(error => {
            console.log(error);
          })
      },

      deleteJson(url) {
        return fetch(this.apiUrl + url, {
            method: 'DELETE',
            headers: this.authenticatedHeaders,
          }
        )
          .then(result => result)
          .catch(error => {
            console.log(error);
          })
      },

      postFile(url, data) {
        return axios({
          method: 'POST',
          url: this.apiUrl + url,
          data: data,
          headers: this.authenticatedHeadersFile
        })
      },

      putFile(url, data) {
        return axios({
          method: 'PUT',
          url: this.apiUrl + url,
          data: data,
          headers: this.authenticatedHeadersFile
        })
      },

      postAuthFile(url, data) {
        return axios({
          method: 'POST',
          url: this.apiAuthUrl + url,
          data: data,
          headers: this.notAuthenticatedHeadersFile
        })
      },

      postAuth(url, data) {
        return fetch(this.apiAuthUrl + url, {
          method: 'POST',
          headers: this.notAuthenticatedHeaders,
          body: JSON.stringify(data),
        })
          .then(result => result.json())
          .catch(error => {
            console.log(error);
          })
      }
      ,

      logOut() {
        return fetch(this.apiAuthUrl + 'logout/', {
          method: 'POST',
          headers: this.authenticatedHeaders,
          body: JSON.stringify({data: 'test'})
        })
          .then(result => {
            if (result.status === 202) {
              sessionStorage.removeItem('token');
              sessionStorage.removeItem('username');
              window.location = '/'
            } else {
              sessionStorage.removeItem('token');
              sessionStorage.removeItem('username');
              window.location = '/'
            }
          })
          .catch(error => {
            console.log(error);
          })
      },

      imgPath(originPath) {
        return originPath
        // return /^\/media/i.test(originPath) ? `${this.serverSource}${originPath}` : originPath
      },

      findItem(data) {
        return this.order.find(elem => {
          return elem.consumer.id === data.consumer && elem.chef.id === data.chef && elem.meal.id === data.meal
        });
      },

      addOrder(consumerId, chefId, mealId) {
        if (!chefId) {
          return alert('Повар не выбран!')
        }
        let data = {
          consumer: +consumerId,
          chef: +chefId,
          meal: +mealId,
          quantity: 1
        };

        let item = this.findItem(data);

        if (!item) {
          this.postJson('orders/', data)
            .then(response => {
              this.getOrders(this.userId);
            })
            .catch(error => console.log(error))
        } else {
          data.id = item.id;
          data.quantity = item.quantity + 1;
          data.status = item.status;
          this.putJson(`orders/${item.id}/`, data)
            .then(data => {
              console.log(data);
              this.getOrders(this.userId);
            })
        }
      },

      getOrders(userId) {
        this.getJson(`orders/?user_id=${userId}`)
          .then(data => {
            this.order = data.results;
            console.log('orders>>', this.order)
          });
      },

      getChefOrders(chefId) {
        this.getJson(`orders/?chef_id=${chefId}`)
          .then(data => {
            this.chefOrders = data.results
          })
      },

      getUser(userId) {
        this.getJson(`users/${userId}/`)
          .then(data => {
            console.log(data);
            this.user = data;
            this.user.avatar = this.imgPath(this.user.avatar);
            console.log(this.user);
            if (this.user.is_producer) {
              for (let item of this.user.menu) {
                // console.log(item);
                item.image = this.imgPath(item.image)
              }
              this.getChefOrders(this.user.id)
            }
          })
          .catch(error => console.log(error))
      }
      ,
    },

    mounted() {

      if (this.isToken) {
        this.getOrders(this.userId);
        this.getUser(this.userId)
      }
      let script_6 = document.createElement('script');
      script_6.setAttribute('src', "static/js/main.js");
      document.body.appendChild(script_6);

    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  .avatar {
    height: 50px;
    width: 50px;
    border-radius: 50%;
    background-size: cover;
  }

  .pagination {
    justify-content: center;
  }
</style>

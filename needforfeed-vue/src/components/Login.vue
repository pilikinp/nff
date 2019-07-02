<template>
  <div class="form-wrap">
    <div class="my-form">
      <div class="form-row">
        <div class="form-group col-md-12">
          <input type="text" v-model="username" class="form-control" placeholder="Имя">
          <p class="error"></p>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group col-md-12">
          <input type="password" v-model="password" class="form-control" placeholder="Пароль">
          <p class="error"></p>
        </div>
      </div>
      <button class="btn btn-primary" @click.prevent="setLogin">Войти</button>
    </div>
  </div>
</template>

<script>
  import $ from 'jquery'

  export default {
    name: "Login",
    data() {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      setLogin() {
        this.$parent.postAuth('login/', {
          username: this.username,
          password: this.password
        })
          .then(data => {
              // alert('Вы вошли', data);
              sessionStorage.setItem('token', data.token);
              sessionStorage.setItem('username', data.username);
              sessionStorage.setItem('userId', data.id);
              sessionStorage.setItem('avatar', data.avatar);
              window.location = '/';
          })
          .catch(error => {
            alert('Что-то не так(')
          })
      }
    }
  }
</script>

<style scoped>
  .form-wrap {
    margin: auto;
    padding: 20px;
    max-width: 800px
  }
</style>

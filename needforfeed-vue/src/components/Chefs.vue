<template>
  <!-- Main -->
  <!--<section id="main">-->
  <div class="container">
    <div class="row">

      <!-- Sidebar -->
      <div id="sidebar" class="col-4 col-12-medium">

        <!-- Highlights -->
        <section class="list-group">
          <h2>Smth here</h2>
          <!--<ul>-->
          <!--<li class="list-group-item" v-for="chef of chefs" :key="chef.user.id">-->
          <!--<article class="box highlight">-->
          <!--<header>-->
          <!--<h3><router-link :to="{name: 'Chef', params: {'userId': chef.user.id}}" class="list-group-item-action">{{ chef.user.first_name }} {{ chef.user.last_name }}</router-link></h3>-->
          <!--</header>-->
          <!--<img src="https://placehold.it/200x150" alt=""/>-->
          <!--<p>location: {{ chef.user.location }}</p>-->
          <!--<ul class="actions">-->
          <!--<li><router-link :to="{name: 'Chef', params: {'userId': chef.user.id}}" class="button icon fa-file">Learn More</router-link></li>-->
          <!--</ul>-->
          <!--</article>-->

          <!--</li>-->
          <!--</ul>-->
        </section>

      </div>

      <!-- Content -->
      <div id="content" class="col-8 col-12-medium imp-medium">

        <!-- Meals -->
        <article class="box post">
          <header>
            <h2>Chefs!</h2>
          </header>

          <div v-for="chef of chefs" :key="chef.user.id" class="w-auto card">
            <img v-if="chef.user.avatar" :src="chef.user.avatar" alt="" class="card-image-top chef_avatar__card"/>
            <img v-else src="https://placehold.it/200x150" alt="" class="chef_avatar__card"/>
            <div class="card-header">
              {{chef.user.username}}
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ chef.user.first_name }} {{ chef.user.last_name }}</h5>

              <p class="card-text">{{ chef.snippet | truncate(10) }}</p>
              <router-link :to="{name: 'Chef', params: {'chefId': chef.id}}" class="button icon fa-file">Learn
                More
              </router-link>
            </div>
          </div>
        </article>

        <!-- Pagination -->
        <div>
          <ul class="pagination">
            <li v-if="previous" class="page-item">
              <a class="page-link" aria-label="Previous" @click="getChefs(current_page - 1)">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li v-for="i in pages_num" class="page-item">
              <a class="page-link" @click="getChefs(i)">{{ i }}</a>
            </li>
            <li v-if="next" class="page-item">
              <a class="page-link" aria-label="Next" @click="getChefs(current_page + 1)">
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
          </ul>
        </div>

      </div>

    </div>
  </div>
  <!--</section>-->
</template>

<script>
  export default {
    name: "Chefs",

    data() {
      return {
        previous: null,
        next: null,
        page_size: 4, // записей на странице
        pages_num: 1, // количество страниц
        current_page: 1, // текущая страница
        chefs: [],
        chefsRout: '/chefs'
      }
    },

    methods: {

      getChefs(page) {
        let url = page ? `chefs/?page=${page}&page_size=${this.page_size}` : `chefs/?page_size=${this.page_size}`;
        if (page) {
          this.current_page = page
        }
        this.$parent.getJson(url)
          .then(data => {
            console.log(data);
            this.chefs = [...data.results];
            this.previous = data.previous;
            this.next = data.next;
            this.pages_num = Math.ceil(data.count / this.page_size);
            // console.log(this.chefs)
          })
      }
    },

    mounted() {
      this.getChefs()
    }
  }
</script>

<style scoped>
  .chef_avatar__card {
    max-width: 200px;
    align-self: center;
    border-radius: 10%;
    margin: 10px 0 10px;
  }

</style>

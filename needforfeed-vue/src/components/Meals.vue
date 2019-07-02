<template>
  <!-- Main -->
  <!--<section id="main">-->
  <div class="container">
    <div class="row">

      <!-- Sidebar -->
      <div id="sidebar" class="col-4 col-12-medium">

        <!-- Highlights -->
        <section class="list-group">
          <h2>Our chefs!</h2>
          <ul>
            <li class="list-group-item" v-for="chef of chefs" :key="chef.id">
              <article class="box highlight">
                <header>
                  <h3>
                    <router-link :to="{name: 'Chef', params: {'chefId': chef.id}}" class="list-group-item-action">
                      {{ chef.user.first_name }} {{ chef.user.last_name }}
                    </router-link>
                  </h3>
                </header>
                <img v-if="chef.user.avatar" :src="chef.user.avatar" alt="" class="chef_avatar__card"/>
                <img v-else src="https://placehold.it/200x150" alt="" class="chef_avatar__card"/>
                <p>location: {{ chef.user.location }}</p>
                <ul class="actions">
                  <li>
                    <router-link :to="{name: 'Chef', params: {'chefId': chef.id}}" class="button icon fa-file">
                      Learn More
                    </router-link>
                  </li>
                </ul>
              </article>

            </li>
          </ul>
        </section>

      </div>

      <!-- Content -->
      <div id="content" class="col-8 col-12-medium imp-medium">

        <!-- Meals -->
        <article class="box post">
          <header>
            <h2>Meals!</h2>
          </header>

          <div v-for="meal of meals" :key="meal.id" class="w-auto card">
            <img v-if="meal.image" :src="meal.image" class="card-img-top" alt="...">
            <img v-else src="https://placehold.it/200x150" class="card-img-top" alt="...">

            <div class="card-body">
              <h5 class="card-title">{{ meal.title }}</h5>
              <p class="card-text">{{ meal.snippet }}</p>
              <p class="card-text">{{ meal.price }} &#8381;</p>
              <router-link :to="{name: 'Meal', params: {'mealId': meal.id}}" class="btn btn-outline-success">
                Подробнее
              </router-link>
            </div>
          </div>

        </article>

        <!-- Pagination -->
        <div>
          <ul class="pagination">
            <li v-if="previous" class="page-item">
              <a class="page-link" aria-label="Previous" @click="getMeals(current_page - 1)">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li v-for="i in pages_num" class="page-item">
              <a class="page-link" @click="getMeals(i)">{{ i }}</a>
            </li>
            <li v-if="next" class="page-item">
              <a class="page-link" aria-label="Next" @click="getMeals(current_page + 1)">
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
    name: "Meals",

    data() {
      return {
        previous: null,
        next: null,
        page_size: 4, // записей на странице
        pages_num: 1, // количество страниц
        current_page: 1, // текущая страница
        meals: [],
        chefs: [],
        chefsRout: '/chefs'
      }
    },

    methods: {

      getMeals(page) {
        let url = page ? `meals/?page=${page}&page_size=${this.page_size}` : `meals/?page_size=${this.page_size}`;
        if (page) {
          this.current_page = page
        }
        this.$parent.getJson(url)
          .then(data => {
            this.meals = [...data.results];
            this.previous = data.previous;
            this.next = data.next;
            this.pages_num = Math.ceil(data.count / this.page_size);
            // console.log(`getmeals page: ${page} count: ${this.count}, next ${this.next} prev ${this.previous}`);
          })
          .catch(error => console.log(error))
      },

      getChefs() {
        this.$parent.getJson('chefs/')
          .then(data => {
            this.chefs = [...data.results]
          })
          .catch(error => console.log(error))
      }

    },

    mounted() {
      this.getMeals();
      this.getChefs();
    }
  }
</script>

<style scoped>
  .chef_avatar__card {
    width: 200px;
    height: 150px;
  }
</style>

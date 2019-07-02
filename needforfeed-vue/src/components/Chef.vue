<template>
  <!-- Main -->
  <!--<section id="main">-->
  <div class="container">

    <div class="row">

      <!-- Sidebar -->
      <div id="sidebar" class="col-4 col-12-medium">

        <!-- Highlights -->
        <section v-if="gotChef" class="list-group">
          <h2>menu</h2>
          <ul>
            <li class="list-group-item" v-for="menuItem of chef.menu" :key="menuItem.id">
              <article class="box highlight">
                <header>
                  <h3><a class="list-group-item-action" href="#">{{ menuItem.title }}</a></h3>
                </header>
                <img v-if="!menuItem.image" src="https://placehold.it/200x150" alt=""/>
                <img v-else :src="menuItem.image" alt=""/>
                <h4><span class="badge badge-light">Цена: {{ menuItem.price }} rub</span></h4>
                <ul class="actions inline-flex">
                  <li>
                    <router-link :to="{name: 'Meal', params: {'mealId': menuItem.id}}" class="btn btn-outline-success">
                      Подробнее
                    </router-link>
                  </li>
                  <li>
                    <a href="" @click.prevent="addOrder(
                      userId,
                      chefId,
                      menuItem.id
                      )" class="btn btn-outline-success">
                      Заказать!
                    </a>
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
        <article v-if="gotChef" class="box post">
          <header>
            <h2>{{ chef.user.first_name }} {{ chef.user.last_name }}</h2>
          </header>
          <div>
            <img v-if="chef.user.avatar" :src="chef.user.avatar"/>
          </div>
          <div>
            <h3>location:</h3>
            <p v-if="chef.user.location">{{ chef.user.location }}</p>
            <p v-else>Местоположение не указано</p>
          </div>
          <div>
            <h3>Phone:</h3>
            <p>{{ chef.phone }}</p>
          </div>
          <div>
            <h3>About:</h3>
            <p v-if="chef.snippet">{{ chef.snippet }}</p>
            <p v-else>Наш повар еще ничего о себе не написал(</p>
          </div>
        </article>

      </div>

    </div>
  </div>
  <!--</section>-->
</template>

<script>
  export default {
    name: "Chef",
    data() {
      return {
        userId: +sessionStorage.getItem('userId'),
        chef: null,
        chefId: this.$route.params.chefId,
        order: JSON.parse(sessionStorage.getItem('order')),
      }
    },

    computed: {
      gotChef() {
        return !!this.chef
      },

      gotOrder() {
        return !!(this.order === null)
      }

    },

    methods: {
      getChef(chefId) {
        this.$parent.getJson(`chefs/${chefId}/`)
          .then(data => {
            console.log(data);
            this.chef = data;
            this.chef.user.avatar = this.$parent.imgPath(this.chef.user.avatar);
            for (let item of this.chef.menu) {
              // console.log(item);
              item.image = this.$parent.imgPath(item.image)
            }
          })
          .catch(error => console.log(error))
      },

      postOrder(userId, chefId, mealId) {
        let data = {
          order: {
            consumer: userId,
            chef: chefId
          },
          meal: mealId,
          quantity: 1
        };
        console.log(data);
        this.$parent.postJson('orders/', data)
          .then(response => console.log(response));
      },

      addOrder(userId, chefId, mealId) {
        if (this.chef.user.id===this.userId) {
          return alert('Вы не можете заказать у себя!')
        }
        return this.$parent.addOrder(userId, chefId, mealId)
      }

      // addOrder(userId, chefId, mealId) {
      //   let data = {
      //     order: {
      //       consumer: +userId,
      //       chef: +chefId
      //     },
      //     meal: +mealId,
      //     quantity: 1
      //   };
      //   // console.log(this.$parent.order);
      //   let item = this.$parent.order.find(elem => {
      //     return elem.meal === data.meal && elem.order.chef === data.order.chef
      //   });
      //   // console.log(item);
      //   if (item) {
      //     item.quantity++
      //   } else {
      //     this.$parent.order.push(data)
      //   }
      //   console.log(this.$parent.order)
      // }
    },
    mounted() {
      this.getChef(this.chefId);
    }
  }
</script>

<style scoped>

</style>

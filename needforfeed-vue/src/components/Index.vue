<template>
  <!-- Main -->
  <!--<section id="main">-->
  <div class="container">
    <div class="row">

      <!-- Sidebar -->
      <div id="sidebar" class="col-4 col-12-medium">

        <!-- Highlights -->
        <section class="list-group">
          <h2>Some meals!</h2>
          <ul>
            <li class="list-group-item" v-for="meal of meals" :key="meal.id">
              <article class="box highlight">
                <header>
                  <h3>
                    <router-link :to="{name: 'Meal', params: {'mealId': meal.id}}" class="list-group-item-action">
                      {{ meal.title }}
                    </router-link>
                  </h3>
                </header>
                <img v-if="meal.image" :src="meal.image" alt="" class="meal_image__card"/>
                <img v-else src="https://placehold.it/200x150" alt="" class="meal_image__card"/>
                <p>{{ meal.snippet }}</p>
                <ul class="actions">
                  <li>
                    <router-link :to="{name: 'Meal', params: {'mealId': meal.id}}" class="button icon fa-file">Learn
                      More
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

        <!-- Post -->
        <article class="box post">
          <header>
            <h2>Some very useful content</h2>
          </header>
          <h3>Content 1</h3>
          <p>Phasellus laoreet massa id justo mattis pharetra. Fusce suscipit
            ligula vel quam viverra sit amet mollis tortor congue. Sed quis mauris
            sit amet magna accumsan tristique. Curabitur leo nibh, rutrum eu malesuada
            in, tristique at erat lorem ipsum dolor sit amet lorem ipsum sed consequat
            magna tempus veroeros lorem sed tempus aliquam lorem ipsum veroeros
            consequat magna tempus lorem ipsum consequat Phasellus laoreet massa id
            justo mattis pharetra. Fusce suscipit ligula vel quam viverra sit amet
            mollis tortor congue. Sed quis mauris sit amet magna accumsan tristique.
            Curabitur leo nibh, rutrum eu malesuada in tristique</p>

          <h3>Content 2</h3>
          <p>Consequat Phasellus laoreet massa id in, tristique at erat lorem
            ipsum dolor sit amet lorem ipsum sed consequat magna tempus veroeros
            consequat magna tempus lorem ipsum consequat Phasellus laoreet massa id
            justo mattis pharetra. Fusce suscipit ligula vel quam viverra sit amet
            mollis tortor congue. Sed quis mauris sit amet magna.</p>

          <h3>Content 3</h3>
          <p>Nullam dolore etiam sed massa id in, tristique at erat lorem
            ipsum dolor sit amet lorem ipsum sed consequat magna tempus veroeros
            consequat magna tempus lorem ipsum consequat Phasellus laoreet massa id
            justo mattis pharetra. Fusce suscipit ligula vel quam viverra sit amet
            mollis tortor congue. Sed quis mauris sit amet magna.</p>

        </article>

      </div>

    </div>
  </div>
  <!--</section>-->


</template>

<script>

  export default {
    name: "Index",

    data() {
      return {
        meals: [],
      }
    },

    methods: {

      getMeals() {
        this.$parent.getJson('meals/' + '?page_size=3')
          .then(data => {
            this.meals = data.results;
            console.log(data.results)
          })
      }

    },

    mounted() {
      this.getMeals();
    }
  }
</script>

<style scoped>
  .meal_image__card {
    width: 200px;
    height: 150px;
  }
</style>

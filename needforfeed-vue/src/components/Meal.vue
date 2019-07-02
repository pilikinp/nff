<template>

    <!-- Main -->
    <!--<section id="main">-->
    <div class="container">
        <div class="row" style="z-index: 100">

            <!-- Sidebar -->
            <div id="sidebar" class="col-4 col-12-medium">

                <!-- Highlights -->
                <section class="list-group">
                    <h2>Smth here</h2>
                </section>

            </div>

            <!-- Content -->
            <div id="content" class="col-8 col-12-medium imp-medium">

                <!-- Meals -->
                <article v-if="gotMeal" class="box post">
                    <header>
                        <h2>{{this.meal.title}}</h2>
                    </header>

                    <div class="jumbotron jumbotron-fluid">
                        <div class="container">
                            <div v-if="chefs.length">
                                <h5 class="display-5" style="display: block;">Приготовят Вам:</h5>
                                <div :class="chefBadgeClass(chef.id)" v-for="chef of chefs" :key="chef.id"
                                     style="margin: 5px;">
                                    <router-link :to="{name: 'Chef', params: {'chefId': chef.id}}">

                                        <img :src="chef.user.avatar" class="avatar"/>
                                        <h4>
                                            {{ chef.user.username}}
                                        </h4>
                                    </router-link>
                                    <input :id="chef.user.username" type="radio" :value="chef.id" v-model="chefId"
                                           style="-webkit-appearance: checkbox"/> <!--не отображыется(-->
                                    <label :for="chef.user.username">Выбрать</label>
                                </div>
                            </div>

                            <div v-else>
                                <div v-if="gotAllChefs" class="input-group input-group-sm mb-3">
                                    <div class="input-group-prepend">
                                        <label class="input-group-text" for="chefSelector">Выберите повара</label>
                                    </div>
                                    <select v-model="chefId" class="custom-select" aria-label="Small"
                                            aria-describedby="inputGroup-sizing-sm" id="chefSelector">
                                        <option disabled value="">Выбор...</option>
                                        <option v-for="chef of allChefs" :key="chef.id" :value="chef.id"
                                                v-if="chef.user.id!==userId">{{ chef.user.username }}
                                        </option>
                                    </select>
                                </div>
                            </div>

                            <h5 class="display-5">Категория: {{ this.meal.category.title }}</h5>
                            <h4 class="display-4">Цена: {{this.meal.price}} &#8381;</h4>
                            <h5 class="display-5">
                                <span>Вес: {{this.totalWeight}}</span>
                                <span>Калорийность: {{this.totalEnergy}}</span>
                            </h5>
                            <p class="lead">{{ this.meal.snippet }}</p>
                            <hr>
                            <h3>Состав:</h3>
                            <ul class="list-group">
                                <li class="list-group-item product_item" v-for="ingredient of meal.ingredients"
                                    :key="ingredient.id">
                                    {{ ingredient.product.title }}
                                    <img v-if="ingredient.product.image" :src="ingredient.product.image"
                                         class="avatar"/>
                                    <span v-else
                                          class="badge badge-primary mb3">{{ ingredient.product.title[0] }}</span>
                                </li>
                                <li class="list-group-item">
                                    <a href="" @click.prevent="addOrder(
                      userId,
                      chefId,
                      meal.id
                      )" class="btn btn-outline-success">
                                        Заказать!
                                    </a>
                                    <a v-show="inMenu" href="" @click.prevent="isModal = true" class="btn btn-outline-success">
                                        Добавить в меню
                                    </a>
                                </li>
                            </ul>

                        </div>
                    </div>

                </article>
            </div>

        </div>
        <div class="modal-wrapper" v-show="isModal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-body">
                        Вы уверены, что хотите добавить блюдо в меню?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click.prevent="isModal=false">Close</button>
                        <button type="button" class="btn btn-primary" @click.prevent="addMealInMenu(
                      userId,
                      meal.id
                      )" data-dismiss="modal">Добавить
                        </button>
                    </div>
                </div>
            </div>
            <div class="modal-wrapper__screen"></div>
        </div>
    </div>
    <!--</section>-->

</template>

<script>
    export default {
        name: "Meal",
        data() {
            return {
                userId: +sessionStorage.getItem('userId'),
                consumerId: 0,
                meal: null,
                mealId: this.$route.params['mealId'],
                chefs: [],
                allChefs: null,
                chefId: 0,
                inMenu: true,
                isModal: false
            }
        },

        computed: {

            gotMeal() {
                return !!this.meal
            },

            gotAllChefs() {
                return !!this.allChefs
            },

            totalWeight() {
                return this.meal.ingredients.reduce(
                    (accumulator, currentValue) => {
                        return accumulator + currentValue.weight;
                    },
                    0
                );
            },
            totalEnergy() {
                return this.meal.ingredients.reduce(
                    (accumulator, currentValue) => {
                        return accumulator + currentValue.product.energy;
                    },
                    0
                );
            }
        },

        methods: {

            getChef(chefId) {
                this.$parent.getJson(`chefs/${chefId}/`)
                    .then(data => {
                        console.log(data);
                        let tmp = data;
                        tmp.user.avatar = this.$parent.imgPath(tmp.user.avatar);
                        this.chefs.push(tmp)
                    })
                    .catch(error => console.log(error))
            },

            getMeal(mealId) {
                this.$parent.getJson(`meals/${this.mealId}/`)
                    .then(data => {
                        console.log(data);
                        this.meal = data;
                        for (let chef of data.producerprofile_set) {
                            console.log(chef.id);
                            if (chef.id === this.userId) {
                                this.inMenu = false
                            }
                            this.getChef(chef.id)
                        }
                        console.log(this.chefs)
                    })
                    .catch(error => console.log(error))
            },

            getChefs() {
                let url = `chefs/`;
                this.$parent.getJson(url)
                    .then(data => {
                        console.log(data);
                        this.allChefs = [...data.results];
                    })
            },

            addOrder(userId, chefId, mealId) {
                return this.$parent.addOrder(userId, chefId, mealId)
            },

            addMealInMenu(userId, mealId) {
                let data = {
                    consumer: +userId,
                    meal: +mealId
                };

                this.isModal = false;
                this.$parent.postJson('meals/', data)
                    .then(data => {
                        console.log(data);
                        this.getMeal()
                    })
                    .catch(error => console.log(error))

            },

            chooseChef(chefId) {
                this.chefId = chefId;
                console.log(this.chefId)
            },

            chefBadgeClass(chefId) {
                return chefId === this.chefId ? "badge badge-success mb2" : "badge badge-secondary mb2"
            },
        },

        mounted() {
            this.getMeal(this.mealId);
            this.getChefs()

        }
    }
</script>

<style scoped>
    .product_item {
        display: inline-flex;
        justify-content: space-around;
    }

    .modal-wrapper__screen {
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #222;
        opacity: 0.8;
        position: fixed;
        top: 0;
        z-index: 100;
        display: block;
        text-align: center;
    }

    .modal-dialog {
        max-height: 80%;
        max-width: 80%;
        z-index: 101;
        position: fixed;
        margin: auto;
        left: 0;
        top: 0;
        bottom: 0;
        right: 0;
    }
</style>

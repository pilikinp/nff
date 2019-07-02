<template>
    <div>

        <!-- Modal -->
        <div class="modal fade" id="addProduct" tabindex="-1" role="dialog"
             aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Добавление блюда</h5>
                        <button type="button" class="close" data-dismiss="modal" data-toggle="modal"
                                data-target="#addMealtoMenu" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal" data-toggle="modal"
                                    data-target="#addMealtoMenu">Close
                            </button>
                            <button @click="postMeal()" type="button" class="btn btn-primary" data-dismiss="modal"
                                    data-toggle="modal"
                                    data-target="#addMealtoMenu">Сохранить блюдо
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal fade" id="addMealtoMenu" tabindex="-1" role="dialog"
             aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLongTitle">Добавление блюда</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">

                        <div class="input-group input-group-sm mb-3">
                            <div class="input-group-prepend">
                                <label class="input-group-text" for="titleInput">Название</label>
                            </div>
                            <input v-model="mealTitle" id="titleInput" type="text" class="form-control"
                                   aria-label="Small"
                                   aria-describedby="inputGroup-sizing-sm">
                        </div>

                        <div v-if="isCategories" class="input-group input-group-sm mb-3">
                            <div class="input-group-prepend">
                                <label class="input-group-text" for="categoryInput">Категория</label>
                            </div>
                            <select v-model.number="selectedCategoryId" class="custom-select" aria-label="Small"
                                    aria-describedby="inputGroup-sizing-sm" id="categoryInput">
                                <option disabled value="">Выбор...</option>
                                <option v-for="cat of categories" :key="cat.id" :value="cat.id">{{ cat.title }}</option>
                            </select>
                        </div>

                        <div v-if="isProducts" class="input-group input-group-sm mb-3">
                            <div class="input-group-prepend">
                                <label class="input-group-text" for="productInput">Продукт</label>
                                <button v-if="!newProduct" class="btn btn-primary" @click="newProduct=true">new
                                </button>
                                <button v-else class="btn btn-primary" @click="newProduct=false">exist
                                </button>
                            </div>

                            <div v-if="newProduct">
                                <div class="input-group-prepend">
                                    <label class="input-group-text" for="titleProduct">Название</label>
                                    <input v-model="productTitle" id="titleProduct" type="text"
                                           class="form-control"
                                           aria-label="Small"
                                           aria-describedby="inputGroup-sizing-sm">
                                </div>
                                <div class="input-group-prepend">
                                    <label class="input-group-text" for="energyProduct">Energy</label>
                                    <input v-model="productEnergy" id="energyProduct" type="text"
                                           class="form-control"
                                           aria-label="Small"
                                           aria-describedby="inputGroup-sizing-sm">
                                </div>
                                <div class="input-group-prepend">
                                    <label class="input-group-text" for="fatProduct">Fat</label>
                                    <input v-model="productFat" id="fatProduct" type="text"
                                           class="form-control"
                                           aria-label="Small"
                                           aria-describedby="inputGroup-sizing-sm">
                                </div>

                                <div class="input-group-prepend">
                                    <label class="input-group-text" for="proteinProduct">Protein</label>
                                    <input v-model="productProtein" id="proteinProduct" type="text"
                                           class="form-control"
                                           aria-label="Small"
                                           aria-describedby="inputGroup-sizing-sm">
                                </div>
                                <div class="input-group-prepend">
                                    <label class="input-group-text" for="carbohydrateProduct">Carbohydrate</label>
                                    <input v-model="productCarbohydrate" id="carbohydrateProduct" type="text"
                                           class="form-control"
                                           aria-label="Small"
                                           aria-describedby="inputGroup-sizing-sm">
                                </div>
                                <div class="input-group input-group-sm mb-3">
                                    <div class="input-group-prepend">
                                        <label class="input-group-text" for="imageInput">Image</label>
                                    </div>
                                    <input id="imageInput" type="file" @change="loadImage">
                                </div>

                            </div>

                            <select v-else v-model.number="currentSelectedProduct" class="custom-select"
                                    aria-label="Small"
                                    aria-describedby="inputGroup-sizing-sm" id="productInput" style="width: 70%">
                                <option disabled value="">Выбор...</option>
                                <option v-for="prod of products" :key="prod.id" :value="prod">{{ prod.title }}</option>
                            </select>
                            <div class="input-group-prepend">
                                <label class="input-group-text" for="weightInput">вес</label>
                                <input v-model="currentSelectedProductWeight" id="weightInput" type="text"
                                       class="form-control"
                                       aria-label="Small"
                                       aria-describedby="inputGroup-sizing-sm">
                            </div>

                            <button class="btn btn-primary" @click="addIngredient()">+
                            </button>
                        </div>

                        <ul v-if="ingredients.length" class="list-group">
                            <li v-for="(ingr, idx) in ingredients" class="list-group-item">{{ ingr.product.title }} - {{
                                ingr.weight
                                }}
                                <button class="btn btn-primary" @click="delIngredient(idx)">X</button>
                            </li>
                        </ul>


                        <div class="input-group input-group-sm mb-3">
                            <div class="input-group-prepend">
                                <label class="input-group-text" for="priceInput">Стоимость</label>
                            </div>
                            <input v-model.number="mealPrice" id="priceInput" type="text" class="form-control"
                                   aria-label="Small"
                                   aria-describedby="inputGroup-sizing-sm">
                        </div>

                        <div class="input-group input-group-sm mb-3">
                            <div class="input-group-prepend">
                                <label class="input-group-text" for="snippetInput">Краткое описание</label>
                            </div>
                            <textarea v-model="mealSnippet" id="snippetInput" type="text" class="form-control"
                                      aria-label="Small"
                                      aria-describedby="inputGroup-sizing-sm"></textarea>
                        </div>

                        <div class="input-group input-group-sm mb-3">
                            <div class="input-group-prepend">
                                <label class="input-group-text" for="recipeInput">Рецепт</label>
                            </div>
                            <textarea v-model="mealRecipe" id="recipeInput" type="text" class="form-control"
                                      aria-label="Small"
                                      aria-describedby="inputGroup-sizing-sm"></textarea>
                        </div>

                        <div class="input-group input-group-sm mb-3">
                            <div class="input-group-prepend">
                                <label class="input-group-text" for="imageInput">Image</label>
                            </div>
                            <input id="imageInput" type="file" @change="loadImage">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button @click="postMeal()" type="button" class="btn btn-primary" data-dismiss="modal">Сохранить
                            блюдо
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div class="container">
            <div class="row">
                <div id="sidebar" class="col-4 col-12-medium">
                    <section v-if="isUser && user.is_producer" class="list-group">
                        <h2>Мое Меню</h2>
                        <!--<h2 v-else>Мои Заказы</h2>-->
                        <button type="button" class="btn btn-primary" data-toggle="modal"
                                data-target="#addMealtoMenu">Добавить блюдо
                        </button>
                        <ul>
                            <li class="list-group-item" v-for="menuItem of user.menu" :key="menuItem.id">
                                <article class="box highlight">
                                    <header>
                                        <h3>
                                            <router-link class="list-group-item-action"
                                                         :to="{name: 'Meal', params: {'mealId': menuItem.id}}">
                                                {{ menuItem.title }}
                                            </router-link>
                                        </h3>
                                    </header>
                                    <img :src="menuItem.image" alt="" class="meal_image"/>
                                    <h4><span class="badge badge-light">Цена: {{ menuItem.price }} rub</span></h4>
                                    <ul class="actions inline-flex">
                                        <li>
                                            <router-link :to="{name: 'Meal', params: {'mealId': menuItem.id}}"
                                                         class="btn btn-outline-success">
                                                Посмотреть
                                            </router-link>
                                        </li>
                                    </ul>
                                </article>
                            </li>
                        </ul>
                        <h2 v-if="isChefOrders">
                            <router-link :to="{name: 'ChefOrders', params: {'chefId': user.id}}"
                                         class="list-group-item-action">
                                Мои заказы
                            </router-link>
                        </h2>
                        <ul v-if="isChefOrders">
                            <li class="list-group-item" v-for="order of chefOrders" :key="order.id">
                                <article class="box highlight">
                                    {{ order.meal.title }}
                                </article>
                            </li>
                        </ul>


                    </section>
                    <section v-else class="list-group">
                        <h2>Мои Заказы</h2>
                        <ul v-if="isOrder">
                            <li class="list-group-item" v-for="item of order" :key="order.id">
                                <router-link :to="{name: 'Meal', params: {'mealId': item.meal.id}}"
                                             class="list-group-item-action">
                                    <div>
                                        <span>{{ item.meal.title }}</span>
                                        <span>{{ item.quantity }}</span>
                                        <span>{{ item.item_price }}&#8381;</span>
                                    </div>
                                    <span>{{ STATUSES[item.status] }}</span>
                                </router-link>
                            </li>
                        </ul>

                    </section>
                </div>

                <div id="content" class="col-8 col-12-medium imp-medium">
                    <article class="box post">
                        <header>
                            <h2>Профиль</h2>
                        </header>
                        <form v-if="isUser">
                            <div class="avatar_preLoader__div">
                                <img v-if="avatarPreLoader" :src="avatarPreLoader" class="avatar_preLoader__img"/>
                                <img v-else :src="user.user.avatar" class="avatar_preLoader__img"/>
                            </div>

                            <div class="input-group input-group-sm mb-3">
                                <div class="input-group-prepend">
                                    <label class="input-group-text" for="imageChangeInput">Поменять</label>
                                </div>
                                <input id="imageChangeInput" type="file" @change="changeAvatar">
                            </div>

                            <div class="form-group">
                                <label for="username">Имя пользователя</label>
                                <input type="text" class="form-control" id="username" v-model="user.user.username">
                            </div>
                            <div class="form-group">
                                <label for="firstName">Имя</label>
                                <input type="text" class="form-control" id="firstName" v-model="user.user.first_name">
                            </div>
                            <div class="form-group">
                                <label for="lastName">Фамилия</label>
                                <input type="text" class="form-control" id="lastName" v-model="user.user.last_name">
                            </div>
                            <div class="form-group">
                                <label for="location">Адрес</label>
                                <input type="text" class="form-control" id="location" v-model="user.user.location"
                                       placeholder="not used yet">
                            </div>

                            <div class="form-group">
                                <label for="email">E-mail</label>
                                <input type="email" class="form-control" id="email" v-model="user.user.email">
                            </div>

                            <div class="form-group">
                                <label for="phone">Телефон</label>
                                <input type="text" class="form-control" id="phone" v-model="user.phone">
                            </div>

                            <div class="form-group">
                                <label for="exampleFormControlTextarea1">О себе</label>
                                <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"
                                          v-model="user.snippet"></textarea>
                            </div>
                            <button class="btn btn-primary" @click.prevent="updateUser(user.user.id)">Редактировать
                            </button>

                        </form>
                    </article>
                </div>
            </div>

        </div>


    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "Account",

        data() {
            return {
                user: null,
                userId: sessionStorage.getItem('userId'),
                categories: null,
                products: null,

                selectedCategoryId: '',
                currentSelectedProduct: '',
                currentSelectedProductWeight: '',
                mealTitle: '',
                mealPrice: '',
                mealSnippet: '',
                mealRecipe: '',
                mealImage: '',

                newProduct: false,
                productTitle: '',
                productEnergy: '',
                productProtein: '',
                productFat: '',
                productCarbohydrate: '',
                productImage: '',

                ingredients: [],

                avatarPreLoader: null,

                order: this.$parent.order,
                chefOrders: null,
                STATUSES: {
                    PRD: 'обрабатывается',
                    ACP: 'принят',
                    RJC: 'отклонен',
                    PD: 'оплачен',
                    RDY: 'готов к выдаче',
                    CND: 'отменен',
                }

            }
        },
        computed: {

            isUser() {
                return !!this.user
                // return this.user ? true : false
            },
            isCategories() {
                return !!this.categories
            },
            isProducts() {
                return !!this.products
            },
            isChefOrders() {
                return !!this.chefOrders
            },
            isOrder() {
                return !!this.order
            }
        },
        methods: {

            getUser(userId) {
                this.$parent.getJson(`users/${userId}/`)
                    .then(data => {
                        console.log(data);
                        this.user = data;
                        this.user.avatar = this.$parent.imgPath(this.user.avatar);
                        console.log(this.user);
                        if (this.user.is_producer) {
                            for (let item of this.user.menu) {
                                // console.log(item);
                                item.image = this.$parent.imgPath(item.image)
                            }
                            this.getChefOrders(this.user.id)
                        }
                    })
                    .catch(error => console.log(error))
            },

            updateUser() {
                let data = new FormData();

                data.append('user_data', JSON.stringify(this.user.user));
                data.append('profile_data', JSON.stringify({
                    is_producer: this.user.is_producer,
                    phone: this.user.phone,
                    snippet: this.user.snippet,
                    id: this.user.id
                }));
                data.append('avatar', this.user.user.avatar);

                this.$parent.putFile(`users/${this.userId}/`, data)
                    .then(data => {
                        this.avatarPreLoader = null;
                        this.getUser(this.userId);
                        console.log(data);
                    })
                    .catch(error => console.log(error))

            },

            addIngredient() {
                if (this.newProduct && this.productTitle && this.currentSelectedProductWeight) {
                    this.postProduct().then(data => {
                        this.ingredients.push(
                            {
                                'product': data.data.product,
                                'weight': this.currentSelectedProductWeight
                            }
                        );
                        this.currentSelectedProduct = '';
                        this.currentSelectedProductWeight = '';
                        this.newProduct = false;
                        this.productTitle = '';
                        this.productEnergy = '';
                        this.productProtein = '';
                        this.productFat = '';
                        this.productCarbohydrate = '';
                        this.productImage = '';
                        this.getUser(this.userId);
                        this.getProducts();
                    });

                }
                if (this.currentSelectedProduct && this.currentSelectedProductWeight) {
                    this.ingredients.push(
                        {
                            'product': this.currentSelectedProduct,
                            'weight': this.currentSelectedProductWeight
                        }
                    );
                    this.currentSelectedProduct = '';
                    this.currentSelectedProductWeight = '';
                }
            }
            ,

            delIngredient(ingredientIdx) {
                this.ingredients.splice(ingredientIdx, 1);
            }
            ,

            loadImage(image) {
                this.mealImage = image.target.files[0];
                console.log(this.mealImage);
            }
            ,

            changeAvatar(image) {
                console.log(image.target.files[0]);
                this.user.user.avatar = image.target.files[0];

                let reader = new FileReader();
                reader.onload = (event) => {
                    this.avatarPreLoader = this.$parent.imgPath(event.target.result);
                };
                reader.readAsDataURL(image.target.files[0]);
            },

            postMeal() {
                let ingrds = [];
                for (let item of this.ingredients) {
                    ingrds.push(
                        {
                            product_id: item.product.id,
                            weight: item.weight
                        }
                    )
                }
                let meal = {
                    user_id: this.userId,
                    title: this.mealTitle,
                    category: this.selectedCategoryId,
                    price: this.mealPrice,
                    snippet: this.mealSnippet,
                    recipe: this.mealRecipe,
                    ingredients: ingrds,
                };
                let data = new FormData();
                data.append('file', this.mealImage);
                data.append('newMeal', JSON.stringify(meal));
                this.$parent.postFile('meals/', data)
                    .then(data => {
                        console.log(data);
                        this.getUser(this.userId);
                    })

            },

            postProduct() {
                let product = {
                    title: this.productTitle,
                    protein: this.productProtein,
                    energy: this.productEnergy,
                    fat: this.productFat,
                    carbohydrate: this.productCarbohydrate
                };
                let data = new FormData();
                data.append('file', this.productImage);
                data.append('newProduct', JSON.stringify(product));
                return this.$parent.postFile('products/', data)
            },

            getOrders(userId) {
                this.$parent.getJson(`orders/?user_id=${userId}`)
                    .then(data => {
                        this.order = data.results
                    });
            },

            getChefOrders(chefId) {
                this.$parent.getJson(`orders/?chef_id=${chefId}`)
                    .then(data => {
                        this.chefOrders = data.results
                    });
            },

            getProducts() {
                this.$parent.getJson('products/')
                    .then(data => {
                        this.products = data;
                    })
                    .catch(error => console.log(error));
            }

        },
        mounted() {

            this.getUser(this.userId);
            // console.log('>>>>>>>>', this.user);
            this.$parent.getOrders(this.userId);
            // console.log('acc ord>>', this.order);

            this.categories = this.$parent.getJson('categories/')
                .then(data => {
                    this.categories = data.results;
                })
                .catch(error => console.log(error));

            this.getProducts();

        }

    }
</script>

<style scoped>
    .avatar_preLoader__div {
    }

    .avatar_preLoader__img {
        width: 200px;
        margin-bottom: 10px;
    }

    .meal_image {
        max-width: 150px;
    }
</style>

<template>
    <div class="form-wrap">

        <div class="form-group row">
            <div class="form-group col-md-offset-6">
                <input type="text" v-model="username" class="form-control" v-bind:class="{errorForm: validUserName,
                validForm: !isValid}" placeholder="Username">
                <p v-show="validUserName" class="error">Некорректный Username. Username должен состоять из латинских
                    букв и цифр и быть не короче 3 символовю</p>
            </div>
        </div>
        <div class="form-group row">
            <div class="form-group col-md-offset-6">
                <input type="password" v-model="password" class="form-control" v-bind:class="{errorForm: validPassword,
                validForm: !isValid}" placeholder="Пароль">
                <p v-show="validPassword" class="error">Пароль должен содержать не менее 6 символов,
                    иметь как минимум одну заглавную букву и одну цифру</p>
            </div>
        </div>
        <div class="form-group row">
            <div class="form-group col-md-offset-6">
                <input type="password" v-model="password2" class="form-control" v-bind:class="{errorForm: validPassword2,
                validForm: !isValid}" placeholder="Повторите пароль">
                <p v-show="validPassword2" class="error">Пароли не совпадают</p>
            </div>
        </div>
        <div class="form-group row">
            <div class="form-group col-md-offset-6">
                <input type="text" v-model="firstName" class="form-control" v-bind:class="{errorForm: validFirstName,
                validForm: !isValid}" placeholder="Имя">
                <p v-show="validFirstName" class="error">Некорректное имя</p>
            </div>
        </div>
        <div class="form-group row">
            <div class="form-group col-md-offset-6">
                <input type="text" v-model="lastName" class="form-control" v-bind:class="{errorForm: validLastName,
                validForm: !isValid}" placeholder="Фамилия">
                <p v-show="validLastName" class="error">Некорректные данные</p>
            </div>
        </div>

        <div class="input-group input-group-sm mb-3">
            <div class="input-group-prepend">
                <label class="input-group-text" for="imageInput">Image</label>
            </div>
            <input id="imageInput" type="file" @change="loadImage">
        </div>

        <div v-if="isProducer" class="form-group row">
            <div class="form-group col-md-offset-6">
                <input type="text" v-model="email" class="form-control" v-bind:class="{errorForm: validEmail,
                validForm: !isValid}" placeholder="E-mail">
                <p v-show="validEmail" class="error">Некорректный email</p>
            </div>
        </div>

        <div v-if="isProducer" class="form-group row">
            <div class="form-group col-md-offset-6">
                <input type="text" v-model="phone" class="form-control" v-bind:class="{errorForm: validPhone,
                validForm: !isValid}" placeholder="Телефон">
                <p v-show="validPhone" class="error">Некорректный телефон. Введите в формате +79999999999</p>
            </div>
        </div>

        <!--        Локация-->
        <yandex-map
                id="map"
                :settings="settings"
                :coords="[55.753994, 37.622093]"
                zoom="9"
                @click="onClick">
            <ymap-marker v-if="coords" markerId="1" marker-type="placemark" :coords="coords"
                         :properties="{iconCaption: address}"></ymap-marker>
        </yandex-map>
        <div class="form-row">
            <div class="col-3">
                <input type="text" class="form-control" placeholder="Country" v-model="country">
            </div>
            <div class="col-3">
                <input type="text" class="form-control" placeholder="City" v-model="city">
            </div>
        </div>
        <div class="form-row" style="margin-top: 10px">
            <div class="col-4">
                <input type="text" class="form-control" placeholder="Street" v-model="street">
            </div>
            <div class="col-1">
                <input type="text" class="form-control" placeholder="Home" v-model="home">
            </div>
            <div class="col-1">
                <input type="text" class="form-control" placeholder="Apartment" v-model="office">
            </div>
        </div>
        <div class="form-group">
            <div class="checkbox col-md-offset-6">
                <input v-model="isProducer" class="form-check-input" type="checkbox" id="isProducerChecker">
                <label class="form-check-label" for="isProducerChecker">
                    Зарегистрироваться как повар {{ isProducer }}
                </label>
            </div>
        </div>
        <button class="btn btn-primary" @click="reg" :disabled="isValid">Отправить</button>

    </div>
</template>

<script>
    import $ from 'jquery'
    import fs from 'fs'
    import {yandexMap, ymapMarker} from 'vue-yandex-maps'

    export default {
        name: "Registration",
        components: {yandexMap, ymapMarker},
        data() {
            return {
                settings: {
                    apiKey: '5ee87456-80f5-4483-bc7c-60f3b1ade485',
                    lang: 'ru_RU',
                    version: '2.1'
                },
                coords: '',
                address: '',
                country: '',
                city: '',
                street: '',
                home: '',
                office: '',

                username: '',
                password: '',
                password2: '',
                firstName: '',
                lastName: '',
                avatar: '',
                phone: '',
                email: '',
                isProducer: false,
            }
        },

        computed: {
            // getCoords() {
            //     if( this.city) {
            //         ymaps.geocode(this.city, {
            //         results: 1
            //     }).then(function (res) {
            //             let firstGeoObject = res.geoObjects.get(0);
            //                 this.coords = firstGeoObject.geometry.getCoordinates();
            //                 this.address = firstGeoObject.getAddressLine();
            //
            //             });
            //     }
            //         },
                    validUserName()
                {
                    if (this.username) {
                        return !/^[a-zA-Z0-9']{3,20}$/.test(this.username)
                    } else {
                        return false
                    }
                }
            ,

                validFirstName()
                {
                    if (this.firstName) {
                        return !/^[a-zA-Zа-яА-ЯёЁ']{2,20}$/.test(this.firstName)
                    } else {
                        return false
                    }
                }
            ,

                validLastName()
                {
                    if (this.lastName) {
                        return !/^[a-zA-Zа-яА-ЯёЁ']{2,20}$/.test(this.lastName)
                    } else {
                        return false
                    }
                }
            ,

                validPassword()
                {
                    if (this.password) {
                        return !/(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{6,}/.test(this.password)
                    } else {
                        return false
                    }
                }
            ,

                validPassword2()
                {
                    if (this.password) {
                        return !(this.password === this.password2)
                    } else {
                        return false
                    }
                }
            ,

                validEmail()
                {
                    if (this.email) {
                        return !/^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$/.test(this.email)
                    } else {
                        return false
                    }
                }
            ,

                validPhone()
                {
                    if (this.phone) {
                        return !/^\+7[\d]{3}[\d]{3}[\d]{4}$/.test(this.phone)
                    } else {
                        return false
                    }
                }
            ,

                isValid()
                {
                    if (this.isProducer) {
                        return !(this.username && this.password && this.password2 && this.firstName && this.lastName && this.email &&
                            this.phone && !this.validUserName && !this.validFirstName && !this.validLastName && !this.validPassword
                            && !this.validPassword2 && !this.validEmail && !this.validPhone)
                    } else {
                        return !(this.username && this.password && this.password2 && this.firstName && this.lastName &&
                            !this.validUserName && !this.validFirstName && !this.validLastName && !this.validPassword
                            && !this.validPassword2)
                    }
                }
            },

            methods: {

                onClick(e) {
                    this.coords = e.get('coords');
                    this.getAddress(this.coords);
                },
                getAddress(coords) {
                    this.address = 'поиск...';
                    ymaps.geocode(coords).then((res) => {
                        let firstGeoObject = res.geoObjects.get(0);

                        this.address = firstGeoObject.getAddressLine();
                        this.country = firstGeoObject.getCountry();
                        this.city = [firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas()].filter(Boolean).join(', ');
                        this.street = firstGeoObject.getThoroughfare() || firstGeoObject.getPremise();
                        this.home = firstGeoObject.getPremiseNumber();
                    });
                },

                loadImage(image) {
                    this.avatar = image.target.files[0];
                    console.log(this.avatar);
                },

                reg() {
                    let data = new FormData();

                    data.append('user_data', JSON.stringify({
                        username: this.username,
                        password: this.password,
                        password2: this.password2,
                        first_name: this.firstName,
                        last_name: this.lastName,
                        email: this.email
                    }));
                    data.append('profile_data', JSON.stringify({
                        is_producer: this.isProducer,
                        phone: this.phone,
                    }));
                    data.append('location', JSON.stringify({
                        country: this.country,
                        city: this.city,
                        street: this.street,
                        home: this.home,
                        office: this.office
                    }));
                    data.append('avatar', this.avatar);

                    this.$parent.postAuthFile('reg/', data)
                        .then(data => {
                            console.log(data);
                            sessionStorage.setItem('token', data.data.token);
                            sessionStorage.setItem('username', data.data.username);
                            sessionStorage.setItem('userId', data.data.id);
                            sessionStorage.setItem('avatar', data.data.avatar);
                            window.location = '/'
                        })
                        .catch(error => {
                            // alert(error.response.data);
                            console.log(error.response);
                            this.errorRegHandler(error.response)
                        })

                },

                errorRegHandler(data) {
                    console.log('in error handler');
                    console.log(this.data)
                }
            }
        }
</script>

<style scoped>

    #map {
        width: 600px;
        height: 600px;
    }

    .error {
        font-size: small;
        color: red;
    }

    .errorForm {
        border-color: red;
    }

    .validForm {
        border-color: green;
    }

</style>

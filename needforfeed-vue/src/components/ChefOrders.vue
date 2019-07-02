<template>
  <div class="container">
    <div class="row">

      <!-- Content -->
      <div id="content" class="col-12 col-12-medium imp-medium">

        <!-- Orders -->
        <article class="box post">
          <header>
            <h2>Заказы</h2>
          </header>

          <table class="table table-hover">
            <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Клиент</th>
              <th scope="col">Блюдо</th>
              <th scope="col">Количество</th>
              <th scope="col">Всего</th>
              <th scope="col">Статус</th>
              <th scope="col">Отказаться</th>
              <th scope="col">Принять</th>
              <th scope="col">Выполнен</th>
            </tr>
            </thead>
            <tbody v-if="isChefOrders" v-model="chefOrders">
            <tr v-for="(item, index) in chefOrders" :key="item.id">
              <th scope="row">{{index+1}}</th>
              <td>{{ item.consumer.username }}</td>
              <td>{{ item.meal.title }}</td>
              <td>{{item.quantity}}</td>
              <td>{{ item.item_price }}&#8381;</td>
              <td>{{ STATUSES[item.status] }}</td>
              <td>
                <button v-if="item.status!=='RDY'" class="button btn-danger" @click="rejectOrder(item)"></button>
              </td>
              <td>
                <button v-if="item.status!=='ACP'&&item.status!=='RDY'" class="button btn-success" @click="acceptOrder(item)"></button>
                <span v-if="item.status==='ACP'||item.status==='RDY'" class="fa fa-check" @click="setReadyOrder(item)"></span>
              </td>
              <td>
                <button v-if="item.status==='ACP'||item.status==='PD'" class="button btn-success" @click="setReadyOrder(item)"></button>
                <span v-if="item.status==='RDY'" class="fa fa-check" @click="setReadyOrder(item)"></span>
              </td>
            </tr>
            </tbody>
          </table>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "ChefOrders",

    data() {
      return {
        chefId: this.$route.params.chefId,
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
      isChefOrders() {
        return !!this.chefOrders
      },
    },

    methods: {
      getChefOrders(chefId) {
        this.$parent.getJson(`orders/?chef_id=${chefId}`)
          .then(data => {
            this.chefOrders = data.results
          });
      },

      rejectOrder(item) {
        let data = {
          id: item.id,
          consumer: item.consumer.id,
          chef: item.chef.id,
          meal: item.meal.id,
          quantity: item.quantity,
          status: 'RJC'
        };
        // console.log(data);
        this.$parent.putJson(`orders/${item.id}/`, data)
          .then(data => {
            // console.log(data);
            this.getChefOrders(this.chefId);
          })
      },
      acceptOrder(item) {
        let data = {
          id: item.id,
          consumer: item.consumer.id,
          chef: item.chef.id,
          meal: item.meal.id,
          quantity: item.quantity,
          status: 'ACP'
        };
        // console.log(data);
        this.$parent.putJson(`orders/${item.id}/`, data)
          .then(data => {
            // console.log(data);
            this.getChefOrders(this.chefId);
          })
      },
      setReadyOrder(item) {
        let data = {
          id: item.id,
          consumer: item.consumer.id,
          chef: item.chef.id,
          meal: item.meal.id,
          quantity: item.quantity,
          status: 'RDY'
        };
        // console.log(data);
        this.$parent.putJson(`orders/${item.id}/`, data)
          .then(data => {
            // console.log(data);
            this.getChefOrders(this.chefId);
          })
      }
    },

    mounted() {
      this.getChefOrders(this.chefId);
    }
  }
</script>

<style scoped>

</style>

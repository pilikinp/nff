<template>
  <!-- Main -->
  <!--<section id="main">-->
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
              <th scope="col">Блюдо</th>
              <th scope="col">Повар</th>
              <th scope="col">Стоимость</th>
              <th scope="col">Количество</th>
              <th scope="col">Всего</th>
              <th scope="col">Статус</th>
              <!--<th scope="col">Удалить</th>-->
              <th scope="col"></th>
            </tr>
            </thead>
            <tbody v-if="isOrder" v-model="order">
            <tr v-for="(item, index) in order" :key="item.id">
              <th scope="row">{{index+1}}</th>
              <td>{{ item.meal.title }}</td>
              <td>{{ item.chef.user.username }}</td>
              <td>{{ item.meal.price }}&#8381;</td>
              <td>
                <input v-if="item.status==='PRD'" type="number" min="1" v-model="item.quantity" @change="updateOrder(item)">
                <span v-else>{{ item.quantity }}</span>

              </td>
              <td>{{ item.item_price }}&#8381;</td>
              <td>
                {{ STATUSES[item.status] }}
              </td>
              <!--<td>-->
                <!--<button class="button btn-danger" @click="deleteOrder(item.id)">&times;</button>-->
              <!--</td>-->
              <td>
                <button v-if="item.status==='ACP'" class="button btn-success" @click="payOrder(item)">Оплатить</button>
                <button v-else-if="item.status==='PRD'" class="button btn-danger" @click="cancelOrder(item)">Отказаться</button>
                <button v-else-if="item.status==='RJC'||item.status==='CND'" class="button btn-danger" @click="deleteOrder(item.id)">Удалить</button>
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
    name: "Order",
    data() {
      return {
        userId: +sessionStorage.getItem('userId'),
        order: null,
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
      isOrder() {
        return !!this.order
      }
    },

    methods: {
      // getOrders() {
      //   this.order = this.$parent.order;
      //   console.log(this.order)
      // },
      getOrders(userId) {
        this.$parent.getJson(`orders/?user_id=${userId}`)
          .then(data => {
            this.order = data.results
          });
      },

      updateOrder(item) {
        console.log(item);
        let data = {
          id: item.id,
          consumer: item.consumer.id,
          chef: item.chef.id,
          meal: item.meal.id,
          quantity: item.quantity,
          status: item.status
        };
        // console.log(data);
        this.$parent.putJson(`orders/${item.id}/`, data)
          .then(data => {
            // console.log(data);
            this.getOrders(this.userId);
            this.$parent.getOrders(this.userId)
          })
      },

      deleteOrder(orderId) {
        this.$parent.deleteJson(`orders/${orderId}/`)
          .then(data => {
              // console.log(data);
              this.getOrders(this.userId);
              this.$parent.getOrders(this.userId)
            }
          )
      },

      // эмулирует оплату - меняет статус на оплачен
      payOrder(item) {
        let data = {
          id: item.id,
          consumer: item.consumer.id,
          chef: item.chef.id,
          meal: item.meal.id,
          quantity: item.quantity,
          status: 'PD'
        };
        // console.log(data);
        this.$parent.putJson(`orders/${item.id}/`, data)
          .then(data => {
            // console.log(data);
            this.getOrders(this.userId);
            this.$parent.getOrders(this.userId)
          })
      },

      cancelOrder(item) {
        let data = {
          id: item.id,
          consumer: item.consumer.id,
          chef: item.chef.id,
          meal: item.meal.id,
          quantity: item.quantity,
          status: 'CND'
        };
        // console.log(data);
        this.$parent.putJson(`orders/${item.id}/`, data)
          .then(data => {
            // console.log(data);
            this.getOrders(this.userId);
            this.$parent.getOrders(this.userId)
          })
      }

    },

    mounted() {
      this.getOrders(this.userId)

    }
  }
</script>

<style scoped>

  table input {
    text-align: center;
  }

  table button {
    max-width: 100px;
    margin: auto;
    padding: 0;
  }

</style>

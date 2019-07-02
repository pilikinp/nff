// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false;

Vue.filter('truncate', (text, length, byWords = true) => {
  if (byWords) {
    let truncatedList = text ? text.split(' ').slice(0, length) : [];
    if (/\W$/i.test(truncatedList[length - 1])) {
      truncatedList[length - 1] = truncatedList[length - 1].slice(0, -1)
    }
    let truncatedText = truncatedList ? truncatedList.join(' ') : '';
    let end = '...';
    return truncatedText + end
  }
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
});

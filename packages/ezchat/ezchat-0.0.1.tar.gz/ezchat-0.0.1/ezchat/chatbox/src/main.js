
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/main.less';

import 'bootstrap/dist/js/bootstrap';

import Vue from 'vue';

import App from './components/App/component.vue';


export const app = new Vue({
	el: '#top',
	// replace the content of <div id="top"></div> with App
	render: h => h(App)
});

window.app = app;

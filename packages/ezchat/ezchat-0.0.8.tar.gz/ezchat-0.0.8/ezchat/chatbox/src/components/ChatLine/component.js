
import format from 'date-fns/format';


export default {
	name: 'ChatLine',
	props: ['name', 'text', 'datetime', 'sid', 'refsid'],
	data() {
		return {
		};
	},
	created() {
	},
	computed: {
		timestamp: function () {
			return format(this.datetime, 'DD MMM HH:mm:ss');
		},
		panelStyle: function () {			
			if (this.name == 'Server') {
				return 'panel panel-warning';
			}
			else if (this.sid == this.refsid) {
				return 'panel panel-primary';
			}
			else {
				return 'panel panel-info';
			}
		},
	},
	methods: {
	},
};

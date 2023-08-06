
import io from 'socket.io-client';
import 'font-awesome/css/font-awesome.min.css';
import crypto from 'crypto-js';

import ChatLine from '../ChatLine/component.vue';


export default {
	name: 'ChatBox',
	components: {
		'chat-line': ChatLine
	},
	data() {
		return {
			hub: 'localhost',
			port: '5001',
			room: 'myr',
			password: 'nevermind',
			name: 'oli',
			sid: null,
			socket: null,
			socket2: null,
			connectDate: false,
			clients: [],
			message: '',
			errorMessage: null,
			lines: [],
		};
	},
	computed: {
		connectStatus: function () {
			return this.isConnected ? 'Connected' : 'Disconnected';
		},
		connectStatusIcon: function () {
			return this.isConnected ? 'fa fa-link' : 'fa fa-chain-broken';
		},
		connectStatusButtonType: function () {
			return this.isConnected ? 'btn btn-success' : 'btn btn-danger';
		},
		connectAction: function () {
			return this.isConnected ? 'Leave' : 'Enter';
		},
		connectActionClass: function () {
			return this.isConnected ? 'fa fa-sign-out' : 'fa fa-sign-in';
		},
		errorMessageStyle: function () {
			let css = 'alert alert-danger text-center';
			return this.errorMessage ? css + ' visible' : css + ' hidden';
		},
		isConnected: function () {
			console.log('isConnected');
			console.log((this.socket) ? this.socket.connected : false);

			return (this.socket) ? this.socket.connected : false;
		},
		isConnected2: function () {
			console.log('isConnected2');
			console.log((this.socket2) ? this.socket2.connected : false);

			return (this.socket2) ? this.socket2.connected : false;
		}
	},
	created() {
		console.log('created');
		let that = this;

		if (!this.isStorageEmpty()) {
			console.log('storage read from localStorage');
			let storage = that.getStorage();
			console.log(storage);

			that.hub = storage.hub;
			that.port = storage.port;
			that.name = storage.name;
			that.room = storage.room;
			that.password = storage.password;
			that.sid = storage.sid;
			that.connectDate = storage.connectDate;

			this.manageConnection();
		}

	},
	methods: {
		getStorage: function () {
			return (localStorage.ezchat) ? JSON.parse(localStorage.ezchat) : {};
		},
		isStorageEmpty: function () {
			return (!localStorage.ezchat);
		},
		putStorage: function (storage) {
			localStorage.ezchat = JSON.stringify(storage);
		},
		clearStorage: function () {
			localStorage.removeItem('ezchat');
		},
		encrypt: function (plaintext) {
			window.toto = crypto;
			let encrypted = crypto.AES.encrypt(plaintext, this.password).toString();
			console.log('plaintext = '+plaintext);
			console.log('encrypted = '+encrypted);
			// return plaintext;
			return encrypted;
		},
		decrypt: function (ciphertext) {
			window.toto = crypto;
			let decrypted = crypto.AES.decrypt(ciphertext, this.password).toString(crypto.enc.Utf8);
			console.log('ciphertext = '+ciphertext);
			console.log('decrypted = '+decrypted);
			// return ciphertext;
			return decrypted;
		},
		sendMessage: function () {
			let that = this;
			window.that = that;

			// socket std callback function
			let cb3 = function (res) {
				console.log('cb = ', JSON.stringify(res));
			};

			if (that.isConnected) {
				let data = {
					'room': that.room,
					'name': that.name,
					'text': that.encrypt(that.message),
					'sid': that.sid
				};
				that.socket.emit('msg', data, cb3);

				let line = {
					name: that.name,
					text: that.message,
					datetime: new Date(),
					refname: that.name
				};

				that.lines.unshift(line);
				that.lines = that.lines.slice(0);

				that.message = '';
			}
		},
		manageConnection: function () {
			let that = this;
			window.that = that;
			console.log('in manageConnection');

			if (this.isConnected) {
				// disconnect
				let that = this;
				window.that = that;
				console.log('in manageConnection / disconnect');
				console.log('socket');
				console.log(that.socket);

				let data = { 'sid': that.sid };
				that.socket.emit('leave', data);

				that.errorMessage = null;
				that.clients = [];
				that.sid = null;
				that.connectDate = null;

				that.clearStorage();
			}
			else {
				if (that.sid) {
					// re-connect to kill previous sid
					let that = this;
					window.that = that;
					console.log('in manageConnection / re-connect');

					// debug callback
					let cb = function (data) {
						console.log('cb = ', JSON.stringify(data));
					};

					// init socket
					let url_socket = 'http://' + this.hub + ':' + this.port + '/chat';
					that.socket2 = io.connect(url_socket);

					// socket connection triggers kill
					that.socket2.on('connect', function () {
						// destroy previous connection still up at server side and self disconnect
						console.log('in manageConnection / re-connect / sub-connect');
						let data = { 'sid': that.sid };
						that.socket2.emit('kill', data, cb);
						that.sid = null;
						console.log('in manageConnection / re-connect / end sub-connect');
					}, cb);

					// connect from scratch
					console.log('in manageConnection / re-connect / start connect');
					that.connect();
				}
				else {
					// clear errorMsg
					that.errorMessage = null;

					// clear chatroom
					console.log('in manageConnection / connect / clear lines');
					that.lines = [];

					// connect from scratch
					console.log('in manageConnection / connect / connect');
					that.connect();
				}
			}
		},
		connect: function () {
			let that = this;
			window.that = that;
			console.log('in connect');

			// debug callback
			let cb = function (data) {
				console.log('in debug connect');
				console.log('cb = ', JSON.stringify(data));
			};

			// join callback
			let cb1 = function (data) {
				console.log('in join callback');
				console.log('cb = ', JSON.stringify(data));

				that.sid = data.sid;
				if (!that.connectDate) {
					that.connectDate = data.datetime;
				}
				if (data.warning_msg) {
					that.errorMessage = data.warning_msg;
					// setTimeout(function resetErrorMsg() { that.errorMessage = null; }, 5000);
				}
				that.putStorage({
					hub: that.hub,
					port: that.port,
					name: that.name,
					room: that.room,
					password: that.password,
					sid: that.sid,
					connectDate: that.connectDate
				});

				that.socket.emit('clients', {}, cb);
			};

			// init socket
			let url_socket = 'http://' + this.hub + ':' + this.port + '/chat';
			this.socket = io.connect(url_socket);

			// socket connection triggers join
			this.socket.on('connect', function () {
				console.log('in connect / connect');
				let data = {
					'name': that.name,
					'room': that.room,
					'password': that.password
				};
				that.socket.emit('join', data, cb1);
			}, cb);

			// socket listening to 'status'
			this.socket.on('status', function (data) {
				console.log('new status: ', JSON.stringify(data));
				console.log(data);

				let clients = data.clients || [];
				that.clients = clients;
				for (let c of that.clients) {
					if (c.sid == that.sid) {
						c.name = 'Me';
						if (that.connectDate) {
							c.datetime = that.connectDate;
						}
					}
				}

				console.log('end new status');
			});

			// socket listening to 'msg'
			this.socket.on('msg', function (data) {
				console.log('new msg: ', JSON.stringify(data));
				console.log(data);

				let line = {
					name: data.name,
					sid: data.sid,
					text: (data.name == 'Server') ? data.text : that.decrypt(data.text),
					datetime: new Date(),
					refsid: that.sid
				};

				console.log('new line');
				console.log(line);

				that.lines.unshift(line);
				that.lines = that.lines.slice(0);

				console.log('end new msg');
			});
		}
	}
};
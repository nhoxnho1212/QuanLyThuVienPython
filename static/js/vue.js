new Vue({
    vuetify: new Vuetify(),
    data: {
        url_api: "http://localhost:8080/api/",
        valid: false,
        lastName: '',
        firstName: '',
        nameRules: [
            v => !!v || 'Name is required',
            v => (v && v.length <= 10) || 'Name must be less than 10 characters',
        ],
        email: '',
        emailRules: [
            v => !!v || 'E-mail is required',
            v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
        ],
        userName: '',
        userNameRules: [
          v => !!v || 'User name is required',
          v => (v && v.length >= 5) || 'User name must be greater than 5 characters',
          v => (v && v.length <= 100 || 'User name must be less than 100 characters'),
          v => /^[a-zA-Z0-9]([._](?![._])|[a-zA-Z0-9]){6,18}[a-zA-Z0-9]$/ || 'User name must be valid',
      ],
      showPwd: false,
      password: "",
      showConfirmPwd: false,
      passwordRules: [
        v => !!v || 'Password is required',
        v => (v && v.length >= 5) || 'User name must be greater than 5 characters',
      ],
      confirmPwd: "",
      checkbox: false,
      checkboxRules: [
        v => !!v || 'You must agree to continue!',
      ],
      isRememberMe: false
    },
    methods: {

    }

}).$mount('#app');
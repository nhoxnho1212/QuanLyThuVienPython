
var vmAdmin = new Vue({
    el:"#app",
    vuetify: new Vuetify(),
    mixins: [mixin],
    data: {
        dialog: false,
        dialogDelete: false,
        drawer: false,
        search: '',
        editedIndex: -1,
        editedItem: {
            firstname: '',
            lastName: '',
            email: '',
            role: 'user',
            avatar: '',
        },
        defaultItem: {
            firstname: '',
            lastName: '',
            email: '',
            role: 'user',
            avatar: '',
        },
        // user profile
        hasSaved: false,
        isEditing: null,
        model: null,

        tab: null,
        nameRules: [
            (v) => !!v || "Name is required",
            (v) => (v && v.length <= 10) || "Name must be less than 10 characters",
        ],
        emailRules: [
            (v) => !!v || "E-mail is required",
            (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
        ],
        showPwd: false,
        showConfirmPwd: false,
        passwordRules: [
            (v) =>
                ( ( v.length >= 5 || v.length < 1 ) ) || "User name must be greater than 5 characters",
        ],
        valid:false,
        password: "",
        confirmPwd: "",
        lastName: "",
        firstName: "",
        email: "",
        role: "",
        password: "",
        messageAlert: "",
        isAdd: false,
    },
    watcher: {
        isEditing: function(oldval, newval) {
            if (newval) {
                this.hasSaved = false;
            } else {
                this.hasSaved = true;
            }
        },
        dialog (val) {
            val || this.close()
        },
        dialogDelete (val) {
            val || this.closeDelete()
        },
    },
    computed: {
        formTitle () {
            return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
        },
        listRole() {
               switch (this.user.role) {
                   case 'USER_ROLE.admin':
                       return [{name: "user"}]
                       break;
                   case 'USER_ROLE.admin_root':
                       return [{name: "user"}, {name: "admin"}]
                   default:
                       return  ""
               }
        }
    },
    methods: {
        CheckIsAdd() {
          this.isAdd = true;
        },
        customFilter(item, queryText) {
            const textOne = item.name.toLowerCase();
            const searchText = queryText.toLowerCase();

            return (
                textOne.indexOf(searchText) > -1
            );
        },
        loadUserProfile() {
            if (this.firstName || this.firstName.trim() === "") {
                this.firstName = this.user['firstname'] ? this.user['firstname'] : '';
            }
            if (this.lastName || this.lastName.trim() === "") {
                this.lastName = this.user['lastname'] ? this.user['lastname'] : '';
            }
            if (this.email || this.email.trim() === "") {
                this.email =  this.user['email'] ? this.user['email'] : '';
            }
            if (this.role || this.role.trim() === "") {
                switch (this.user.role) {
                    case 'USER_ROLE.user':
                        this.role = 'user';
                        break;
                    case 'USER_ROLE.admin':
                        this.role = 'admin';
                        break;
                    case 'USER_ROLE.admin_root':
                        this.role = 'admin_root';
                        break;
                    default:
                        this.role = ""
                }
            }

        },
        save: async function(){
            this.messageAlert = "Your profile has been updated";
            let requestData = {
                firstname: this.firstName,
                lastname: this.lastName,
            }
            if (this.valid && this.password !== "" )
                requestData['password'] = this.password
            try  {
                let response = await fetch(URL_API_USER.UPDATE + '/'+ String(this.user.id), {
                    method: "PUT",
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json',
                        'x-access-token': this.token
                    },
                    body: JSON.stringify(requestData)
                });
                let status = await response.status;
                let payload = await response.json();
                if (status === 200) {
                    for (let key in payload.payload) {
                        this.user[key] = payload.payload[key];
                        console.log(key)
                    }


                } else {
                    this.messageAlert = payload.payload.error;
                }

                this.isEditing = !this.isEditing;
            } catch (err){
                this.messageAlert = "Internal Server Error";
            }
            this.hasSaved = true;
        },
        editItem: function (item) {

            this.dialog = true
            this.editedIndex =  this.contents.indexOf(item)
            this.editedItem =  Object.assign({}, item)


        },

        deleteItem (item) {
            this.editedIndex = this.contents.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialogDelete = true
        },

        deleteItemConfirm: async function () {
            try  {
                let response = await fetch(URL_API_USER.UPDATE +'/'+ String(this.editedItem['id']), {
                    method: "DELETE",
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json',
                        'x-access-token': this.token
                    }
                });
                let status = await response.status;
                if (status === 204) {
                    await this.contents.splice(this.editedIndex, 1)
                }

                else {
                }

            } catch (err){
            }

            this.closeDelete()
        },

        close () {
            this.dialog = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
            this.isAdd=false;
        },

        closeDelete () {
            this.dialogDelete = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },

        saveItem: async function() {
            if (this.editedIndex > -1) {
                try  {
                    this.editedItem['firstName'] =await this.editedItem['firstname']
                    this.editedItem['lastName'] = await this.editedItem['lastname']
                    let response = await fetch(URL_API_USER.UPDATE +'/'+ String(this.editedItem['id']), {
                        method: "PUT",
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                            'Content-Type': 'application/json',
                            'x-access-token': this.token
                        },
                        body: JSON.stringify(this.editedItem)
                    });
                    let status = await response.status;
                    let payload = await response.json();
                    if (status === 200) {
                        Object.assign(this.contents[this.editedIndex], this.editedItem)
                    }

                    else {
                    }

                } catch (err){
                }


            } else {
            try{
                let response = await fetch(URL_API_USER.UPDATE, {
                    method: "POST",
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json',
                        'x-access-token': this.token
                    },
                    body: JSON.stringify(this.editedItem)
                });
                let status = await response.status;
                let payload = await response.json();
                if (status === 200) {
                    this.contents.push(this.editedItem)
                }

                else {
                }

            } catch (err){
            }

            }
            this.close()
        },
    },

})


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
            role: 'NHAN_VIEN',
            employee_functions: 'NONE_FUNCTION',
            password: '',
            avatar: '',
        },
        defaultItem: {
            firstname: '',
            lastName: '',
            email: '',
            role: 'NHAN_VIEN',
            employee_functions: 'NONE_FUNCTION',
            password: '',
            avatar: '',
        },
        // user profile
        hasSaved: false,
        isEditing: null,
        model: null,

        tab: null,
        nameRules: [
            (v) => !!v || "Name is required",
            (v) => (v && v.length <= 50) || "Name must be less than 50 characters",
        ],
        emailRules: [
            (v) => !!v || "E-mail is required",
            (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
        ],
        showPwd: false,
        showConfirmPwd: false,
        passwordRules: [
            (v) =>
                ( ( v.length >= 5 || v.length < 1 ) ) || "Password must be greater than 5 characters",
        ],
        valid:false,
        password: "",
        confirmPwd: "",
        lastName: "",
        firstName: "",
        email: "",
        role: "",
        password: "",
        employeeFunctions:"",
        listEmplFunctions: [{name: 'THU_THU'}, {name: 'THU_KHO'}, {name: 'THU_QUY'}],
        messageAlert: "",

        isAdd: false,
        snackbar: false,
        timeout: 2000
    },
    watch: {
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
        isDiableEmployeeFunctions() {
            if (this.editedItem.role == "NHAN_VIEN")
                return true;
            return false;
        },
        formTitle () {
            return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
        },
        listRole() {
               switch (this.user.role) {
                   case 'USER_ROLE.MANAGER':
                       return [{name: "NHAN_VIEN"}]
                       break;
                   case 'USER_ROLE.admin_root':
                       return [{name: "NHAN_VIEN"}, {name: "MANAGER"}]
                   default:
                       return  ""
               }
        },

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
                    case 'USER_ROLE.NHAN_VIEN':
                        this.role = 'NHAN_VIEN';
                        break;
                    case 'USER_ROLE.MANAGER':
                        this.role = 'MANAGER';
                        break;
                    case 'USER_ROLE.admin_root':
                        this.role = 'admin_root';
                        break;
                    default:
                        this.role = ""
                }
            }
            if (this.employeeFunctions || this.employeeFunctions.trim() === "") {
                switch (this.user.employee_functions) {
                    case 'EMPLOYEE.THU_THU':
                        this.employeeFunctions = 'THU_THU';
                        break;
                    case 'USER_ROLE.THU_KHO':
                        this.employeeFunctions = 'THU_KHO';
                        break;
                    case 'USER_ROLE.THU_QUY':
                        this.employeeFunctions = 'THU_QUY';
                        break;
                    default:
                        this.employeeFunctions = "NONE_FUNCTION"
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
                    let payloadreq =  {
                        'firstname': await this.editedItem['firstname'],
                        'lastname':await this.editedItem['lastname'],
                        'email':await this.editedItem['email'],
                        'role':await this.editedItem['role'],
                        'password':await this.editedItem['password'],
                        'avatar':await this.editedItem['avatar'],
                    }
                    if (payloadreq.role === 'NHAN_VIEN')  {
                        payloadreq['employee_functions'] = this.editedItem['employee_functions']
                    } else {
                        payloadreq['employee_functions'] = "NONE_FUNCTION"
                    }
                    let response = await fetch(URL_API_USER.UPDATE +'/'+ String(this.editedItem['id']), {
                        method: "PUT",
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                            'Content-Type': 'application/json',
                            'x-access-token': this.token
                        },
                        body: JSON.stringify(payloadreq)
                    });
                    let status = await response.status;
                    let payload = await response.json();
                    if (status === 200) {
                        Object.assign(this.contents[this.editedIndex], this.editedItem)
                        this.messageAlert = await "User infomation updated !";
                        this.snackbar = true;
                    }
                    else {
                        this.messageAlert = await payload.error;
                        this.snackbar = true;
                    }

                } catch (err){
                    this.messageAlert = await "Internal Server Error";
                    this.snackbar = true;
                }


            } else {
            try{
                let payloadreq =  {
                    'firstname': await this.editedItem['firstname'],
                    'lastname':await this.editedItem['lastname'],
                    'email':await this.editedItem['email'],
                    'role':await this.editedItem['role'],
                    'password':await this.editedItem['password'],
                    'avatar':await this.editedItem['avatar'],
                }
                if (payloadreq.role === 'NHAN_VIEN')  {
                    payloadreq['employee_functions'] = this.editedItem['employee_functions']
                } else {
                    payloadreq['employee_functions'] = "NONE_FUNCTION"
                }
                let response = await fetch(URL_API_USER.UPDATE, {
                    method: "POST",
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json',
                        'x-access-token': this.token
                    },
                    body: JSON.stringify(payloadreq)
                });
                let status = await response.status;
                let payload = await response.json();
                if (status == 200) {
                    this.contents.push(await Object.assign({}, this.editedItem, {'id': payload.payload['id']}))
                    this.messageAlert = await "User created !";
                    this.snackbar = true;
                }
                else {
                    this.messageAlert = await payload.error;
                    this.snackbar = true;
                }

            } catch (err){
                this.messageAlert = await "Internal Server Error";
                this.snackbar = true;
            }

            }
            this.close()
        },
    },

})

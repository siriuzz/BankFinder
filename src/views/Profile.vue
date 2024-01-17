<template>
    <v-responsive>

        <v-row align-content="space-evenly" justify="center">
            <v-col md="6" cols="12">
                <v-card elevation="5" variant="outlined" class="ma-5 pa-5 text-center">
                    <v-card-title class="text-h4">Perfil</v-card-title>
                    <v-container v-if="user && !editProfile && !changePassword" class="d-flex flex-column w-90 ">
                        <v-chip-group column>
                            <v-chip class="" prepend-icon="mdi-email">
                                Nombre: {{ user.first_name }}
                            </v-chip>
                            <v-chip prepend-icon="mdi-account">
                                Nombre de usuario: {{ user.username }}
                            </v-chip>
                            <v-chip v-if="user.last_login" prepend-icon="mdi-calendar-lock-open" class="mb-3">
                                Último inicio de sesión: {{ parseDate }}
                            </v-chip>
                            <v-container class="d-flex justify-space-around">
                                <v-btn @click="editProfile = !editProfile">Editar perfil</v-btn>
                                <v-btn @click="changePassword = !changePassword">Cambiar contraseña</v-btn>
                            </v-container>
                        </v-chip-group>
    
    
                    </v-container>
                    <update-user-form :check-username="checkUsername" @cancel='cancelUpdate' :user="user" :updateUserValid="updateUserValid" :active="editProfile"/>
                    <!-- <v-container v-if="user && editProfile && !change_password" class="d-flex flex-column w-75 ">
                        
                        <v-form @submit.prevent ref="updateUserForm" v-model="updateUserValid"
                            validate-on="input">
                            <v-text-field label="Nombre" :rules="required" v-model="user.first_name" clearable
                                density="compact"></v-text-field>
                            <v-text-field label="Apellido" :rules="required" v-model="user.last_name" clearable
                                density="compact"></v-text-field>
                            <v-text-field label="Nombre de usuario" :rules="usernameRules" v-model="user.username"
                                @change="checkUsername" clearable density="compact"></v-text-field>
                            <v-container class="d-flex justify-space-around">
                                <v-btn :disabled="!updateUserValid">Guardar cambios
                                    <v-dialog activator="parent" width="auto" v-model="editProfileDialog">
                                        <v-card class="pr-5">
                                            <v-card-text>¿Estas seguro de que quieres guardar los cambios?</v-card-text>
                                            <v-container class="d-flex">
                                                <v-card-actions>
                                                    <v-btn block @click="updateProfile" type="submit"
                                                        variant='outlined'>Guardar</v-btn>
                                                    <v-btn block @click="editProfileDialog = false"
                                                        variant='outlined'>Cancelar</v-btn>
                                                </v-card-actions>
                                            </v-container>
                                        </v-card>
                                    </v-dialog>
                                </v-btn>
                                <v-btn @click="editProfile = !editProfile">Cancelar</v-btn>
                            </v-container>
                        </v-form>
                    </v-container> -->
                    <change-password-form @cancel="cancelUpdatePassword" :active="changePassword" :user="user" :valid="changePasswordValid"/>
                </v-card>
            </v-col>
        </v-row>
    </v-responsive>
</template>
    
<script>
import UpdateUserForm from '@/components/UpdateUser/UpdateUserForm.vue';
import ChangePasswordForm from '@/components/ChangePassword/ChangePasswordForm.vue'
export default {
    components:{
        UpdateUserForm,
        ChangePasswordForm
    },
    data() {
        return {
            url: `http://${import.meta.env.VITE_API_URL}`,
            user: {},
            updateUserValid: true,
            changePasswordValid: true,
            editProfile: false,
            changePassword: false,
            old_password: "",
            new_password: "",
            repeat_password: "",
            editProfileDialog: false,
            usernameTaken: false,
            changePasswordDialog: false,
            incorrectPassword: false,
            samePassword: false,

        }
    },
    methods: {
        validateUpdateUserForm() {
            this.$refs.updateUserForm.validate();
            console.log(updateUserValid)
        },
        cancelUpdate(cancel){
            this.editProfile = cancel
        },
        cancelUpdatePassword(cancel){
            this.changePassword = cancel
        },  
        getUserData() {
            this.$axios.get(`${this.url}/user-data`)
                .then(res => {
                    console.log(res)
                    this.user = res.data
                })
                .catch(err => {
                    console.error(err);
                    if (err.response.status == 403) this.$router.push('/login')
                });
        },
        updateProfile() {
            if (this.updateUserValid) {
                this.editProfileDialog = false;
                this.$axios.patch(`${this.url}/user/update`, {
                    'username': this.user.username,
                    'first_name': this.user.first_name,
                    'last_name': this.user.last_name
                }, {

                    headers: {
                        'X-CSRFToken': this.$cookies.get('csrftoken')
                    }
                })
                    .then(res => {
                        console.log(res)
                        // if (res.status == 200) this.$router.push('/login');
                    })
                    .catch(err => {
                        console.error(err);
                        // if (err.response.status == 403) this.$router.push('/login')
                    });
                this.editProfile = !this.editProfile
            }


        },
        updatePassword() {
            this.$refs.changePasswordForm.validate()
            if (this.changePasswordValid) {
                this.$axios.patch(`${this.url}/user/change_password`, {
                    'old_password': this.old_password,
                    'new_password': this.new_password,
                    'repeat_password': this.repeat_password,
                },
                    {
                        headers: {
                            'X-CSRFToken': this.$cookies.get('csrftoken')
                        }
                    }
                )
                    .then(res => {
                        console.log(res)
                        if (res.status == 200) this.$router.push('/login');
                        this.changePassword = !this.changePassword
                    })
                    .catch(err => {
                        console.error(err);
                        if (err.data.samePassword == true) this.samePassword = true;
                        else this.incorrectPassword = true;

                        this.$refs.changePasswordForm.validate();
                        this.changePasswordDialog = false;
                        // if (err.response.status == 403) this.$router.push('/login')
                    });
            }


        },
        async checkUsername() {
            this.$axios.get(
                `${this.url}/user/is-username-taken`, {
                params: {
                    username: this.user.username,
                },
            }
            ).then(res => {
                console.log(res);
                if (res.data.taken) return this.usernameTaken = true
            }).catch(err => {
                console.log(err);
            });
        },

        requiredField(value) {
            if (value.length > 0) return true
            return 'Este campo es obligatorio'
        }


    },
    computed: {
        parseDate() {
            if (this.user) {
                console.log(this.user.last_login);
                const newDate = new Date(this.user.last_login);
                const options = {
                    month: 'long',
                    day: 'numeric',
                    year: "numeric"
                };
                const language = 'es-ES'
                const finalDate = new Intl.DateTimeFormat(language, options).format(newDate)
                return finalDate

            }
        }
    },
    mounted() {
        this.getUserData()
    }

}

</script>
<template>
    <v-row align-content="space-evenly" justify="center">
        <v-col md="6" cols="12">
            <v-card elevation="5" rounded="pill" class="text-center">
                <v-card-title class="text-h4">Perfil</v-card-title>
                <v-container v-if="user && !edit_profile && !change_password" class="d-flex flex-column w-75 ">
                    <v-chip-group column>
                        <v-chip class="my-3 w-auto" prepend-icon="mdi-email">
                            Nombre: {{ user.first_name }}
                        </v-chip>
                        <v-chip class="my-3 w-auto" prepend-icon="mdi-email">
                            Apellido: {{ user.last_name }}
                        </v-chip>
                        <v-chip prepend-icon="mdi-account">
                            Nombre de usuario: {{ user.username }}
                        </v-chip>
                        <v-chip v-if="user.last_login" prepend-icon="mdi-calendar-lock-open" class="mb-3">
                            Último inicio de sesión: {{ parseDate }}
                        </v-chip>
                        <v-container class="d-flex justify-space-around">
                            <v-btn @click="edit_profile = !edit_profile">Editar perfil</v-btn>
                            <v-btn @click="change_password = !change_password">Cambiar contraseña</v-btn>
                        </v-container>
                    </v-chip-group>


                </v-container>

                <v-container v-if="user && edit_profile && !change_password" class="d-flex flex-column w-75 ">
                    <!-- <v-chip-group column>
                        <v-chip prepend-icon="mdi-account">
                            Nombre de usuario: {{ user.username }}
                        </v-chip>
                        <v-chip class="my-3 w-auto" prepend-icon="mdi-email">
                            Correo electrónico: {{ user.email }}
                        </v-chip>
                        <v-chip v-if="user.last_login" prepend-icon="mdi-calendar-lock-open"  class="mb-3">
                            Último inicio de sesión: {{ parseDate }}
                        </v-chip>
                        <v-container class="d-flex justify-space-around">
                            <v-btn>Editar perfil</v-btn>
                            <v-btn>Cambiar contraseña</v-btn>
                        </v-container>
                    </v-chip-group> -->
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
                            <v-btn @click="edit_profile = !edit_profile">Cancelar</v-btn>
                        </v-container>
                    </v-form>
                </v-container>
                <v-container v-if="user && !edit_profile && change_password" class="d-flex flex-column w-75 ">
                    <v-alert class="mb-3 bg-secondary">NOTA: Al cambiar de contraseña deberá volver a iniciar
                        sesión</v-alert>
                    <v-form fast-fail validate-on="input" v-model="changePasswordValid" ref="changePasswordForm">
                        <v-text-field label="Contraseña anterior" :rules='oldPasswordRules' v-model="old_password" clearable
                            density="compact" type="password"></v-text-field>
                        <v-text-field label="Contraseña nueva" :rules="passwordRules" v-model="new_password" clearable
                            density="compact" type="password"></v-text-field>

                        <v-text-field label="Repetir contraseña" :rules="repeatPasswordRules" v-model="repeat_password"
                            clearable density="compact" type="password"></v-text-field>
                        <v-container class="d-flex justify-space-around">
                            <v-btn :disabled="!changePasswordValid">Guardar contraseña
                                <v-dialog activator="parent" width="auto" v-model="changePasswordDialog">
                                    <v-card>
                                        <v-card-text>¿Estas seguro de que quieres cambiar tu contraseña?</v-card-text>
                                        <v-card-text>
                                            Al cambiar la contraseña, deberás iniciar sesión de nuevo
                                        </v-card-text>
                                        <v-card-actions>
                                            <v-container class="w-auto d-flex flex-row justify-space-around">
                                                <v-btn block @click="changePassword" width="100" variant='outlined'>Cambiar
                                                    contraseña</v-btn>
                                                <v-btn block @click="changePasswordDialog = false"
                                                    variant='outlined'>Cancelar</v-btn>
                                            </v-container>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                            </v-btn>
                            <v-btn @click="change_password = !change_password">Cancelar</v-btn>
                        </v-container>
                    </v-form>
                </v-container>
            </v-card>
        </v-col>
    </v-row>
</template>
    
<script>

export default {
    data() {
        return {
            url: `http://${import.meta.env.VITE_API_URL}`,
            user: {},
            updateUserValid: true,
            changePasswordValid: true,
            edit_profile: false,
            change_password: false,
            old_password: "",
            new_password: "",
            repeat_password: "",
            editProfileDialog: false,
            usernameTaken: false,
            changePasswordDialog: false,
            incorrectPassword: false,
            samePassword: false,
            required: [
                value => {
                    if (value.length > 0) return true
                    return 'Este campo es obligatorio'
                }
            ],
            usernameRules: [
                value => {
                    return this.requiredField(value);
                },
                value => {
                    if (value.length >= 3) return true
                    return 'Nombre de usuario demasiado corto'
                },
                () => {
                    if (!this.usernameTaken) return true
                    return 'Este nombre de usuario ya existe'
                }
            ],
            oldPasswordRules: [
                value => {
                    return this.requiredField(value);
                },
                () => {
                    if (this.incorrectPassword) return "Contraseña incorrecta"
                    return true
                }
            ],

            passwordRules: [
                value => {
                    return this.requiredField(value)
                },
                value => {
                    if (value.length >= 8) return true
                    return 'La contraseña debe contener al menos 8 caracteres'
                },
                value => {
                    let hasNumber = false;
                    let hasLetter = false;
                    let hasSpecialChar = false;

                    for (const char of value) {
                        if (!isNaN(char)) {
                            hasNumber = true;
                        } else if (char.match(/[a-zA-Z]/)) {
                            hasLetter = true;
                        } else if (char.match(/[!@#$%^&*(),.?":{}|<>]/)) {
                            hasSpecialChar = true;
                        }

                        if (hasNumber && hasLetter && hasSpecialChar) {
                            return true;
                        }
                    }

                    return 'La contraseña debe contener al menos un número, una letra y un simbolo';
                },
                value => {
                    if (value !== this.old_password) return true
                    return "La contraseña anterior y nueva son iguales"
                }
            ],
            repeatPasswordRules: [
                value => {
                    if (value.length > 0) return true
                    return 'Este campo es obligatorio.'
                },
                value => {
                    if (value === this.new_password) return true
                    return 'Las contraseñas no coinciden'
                }
            ]



        }
    },
    methods: {
        validateUpdateUserForm() {
            this.$refs.updateUserForm.validate();
            console.log(updateUserValid)
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
                this.edit_profile = !this.edit_profile
            }


        },
        changePassword() {
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
                        this.change_password = !this.change_password
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
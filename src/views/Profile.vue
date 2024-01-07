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
                    <v-text-field label="Nombre" v-model="user.first_name" clearable
                        density="compact"></v-text-field>
                    <v-text-field label="Apellido" v-model="user.last_name" clearable
                        density="compact"></v-text-field>
                    <v-text-field label="Nombre de usuario" v-model="user.username" clearable
                        density="compact"></v-text-field>

                    <v-container class="d-flex justify-space-around">
                        <v-btn @click="updateProfile">Guardar cambios</v-btn>
                        <v-btn @click="edit_profile = !edit_profile">Cancelar</v-btn>
                    </v-container>

                </v-container>
                <v-container v-if="user && !edit_profile && change_password" class="d-flex flex-column w-75 ">
                    <v-alert class="mb-3 bg-secondary">NOTA: Al cambiar de contraseña deberá volver a iniciar sesión</v-alert>
                    <v-text-field label="Contraseña anterior" v-model="old_password" clearable
                        density="compact" type="password"></v-text-field>
                    <v-text-field label="Contraseña nueva" v-model="new_password" clearable
                        density="compact" type="password"></v-text-field>

                    <v-text-field label="Repetir contraseña" v-model="repeat_password" clearable
                        density="compact" type="password"></v-text-field>


                    <v-container class="d-flex justify-space-around">
                        <v-btn @click="changePassword">Guardar contraseña</v-btn>
                        <v-btn @click="change_password = !change_password">Cancelar</v-btn>
                    </v-container>

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
            edit_profile: false,
            change_password: false,
            old_password: "",
            new_password: "",
            repeat_password: "",

        }
    },
    methods: {
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

            this.$axios.patch(`${this.url}/user/update`, {
                'username': this.user.username,
                'first_name':this.user.first_name,
                'last_name':this.user.last_name
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
        },
        changePassword() {
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
                })
                .catch(err => {
                    console.error(err);
                    // if (err.response.status == 403) this.$router.push('/login')
                });


            this.change_password = !this.change_password
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
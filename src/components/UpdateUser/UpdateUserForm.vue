<template>
    <v-container v-if="user && active" class="d-flex flex-column w-75 ">
        <v-form @submit.prevent ref="updateUserForm" validate-on="input">
            <v-text-field label="Nombre" :rules="required" v-model="user.first_name" clearable
                density="compact"></v-text-field>
            <v-text-field label="Nombre de usuario" :rules="usernameRules" v-model="user.username" @change="checkUsername"
                clearable density="compact" required></v-text-field>
            <v-container class="d-flex justify-space-around">
                <v-btn :disabled="!updateUserValid">Guardar cambios
                    <UpdateUserDialog />
                </v-btn>
                <v-btn @click="active = !active">Cancelar</v-btn>
            </v-container>
        </v-form>
    </v-container>
</template>

<script>
import UpdateUserDialog from "@/components/UpdateUser/UpdateUserDialog.vue";
export default {
    props: {
        user: Object,
        updateUserValid: Boolean,
        active: Boolean,
        checkUsername:Function

    },
    components: {
        UpdateUserDialog,
    },
    data() {
        return {

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
        }
    },
    methods: {
        emitCancel() {
            this.$emit('cancel', this.active)
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
                this.active = !this.active
            }


        },
        requiredField(value) {
            if (value.length > 0) return true
            return 'Este campo es obligatorio'
        }
    },
    watch: {
        active: 'emitCancel'
    }
}
</script>
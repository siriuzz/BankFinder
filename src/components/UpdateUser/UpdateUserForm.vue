<template>
    <v-container v-if="user && active" v-model="formValid" class="d-flex flex-column w-75 ">
        <v-form fast-fail @submit.prevent="this.active = !this.active" ref="updateUserForm" validate-on="input">
            <v-text-field label="Nombre" :rules="required" v-model="user.first_name" clearable
                density="compact"></v-text-field>
            <v-text-field label="Nombre de usuario" :rules="usernameRules" v-model="user.username" @input="checkUsername"
                clearable density="compact" required></v-text-field>
            <v-container class="d-flex justify-space-around">
                <v-btn :disabled="formValid && usernameTaken">Guardar cambios
                    <FormConfirmationDialog v-model="showDialog" :save="updateProfile" :active="showDialog"
                        @cancel="hideDialog" text="¿Estas seguro de que quieres guardar los cambios?" />
                </v-btn>
                <v-btn @click="active = !active">Cancelar</v-btn>
            </v-container>
        </v-form>
    </v-container>
</template>

<script>
// import UpdateUserDialog from "@/components/UpdateUser/UpdateUserDialog.vue";
import FormConfirmationDialog from "../FormConfirmationDialog.vue";
export default {
    props: {
        user: Object,
        updateUserValid: Boolean,
        active: Boolean

    },
    components: {
        // UpdateUserDialog,
        FormConfirmationDialog
    },
    data() {
        return {
            url: import.meta.env.VITE_API_URL,
            showDialog: false,
            usernameTaken: false,
            done:true,
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
            formValid:true
        }
    },
    methods: {
        hideDialog(cancel) {
            this.showDialog = cancel
        },
        emitCancel() {
            this.$emit('cancel', this.active? this.done:this.active)
        },
        updateProfile() {
            if (this.formValid) {
                this.editProfileDialog = false;
                this.$axios.patch(`http://${this.url}/user/update`, {
                    'username': this.user.username,
                    'first_name': this.user.first_name,
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
                this.showDialog = false;
                window.location.reload();
                // this.active = !this.active
            }


        },
        requiredField(value) {
            if (value.length > 0) return true
            return 'Este campo es obligatorio'
        },
        async checkUsername() {
            this.$axios.get(
                `http://${this.url}/user/is-username-taken`, {
                params: {
                    username: this.user.username,
                },
            }
            ).then(res => {
                console.log(res);
                if (res.data.taken) {
                    this.usernameTaken = true
                    this.$refs.updateUserForm.validate()
                } else {
                    this.usernameTaken = false
                    this.$refs.updateUserForm.resetValidation()
                    this.$refs.updateUserForm.validate()

                }
            }).catch(err => {
                console.log(err);
            });

        },
    },
    watch: {
        active: 'emitCancel',
        // username: {
        //     type:String,
        //     handler
        //     immediate:true,
        //     flush:"post"
        // }
    }
}
</script>
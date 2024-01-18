<template>
    <v-container v-if="user && active" class="d-flex flex-column w-75 ">
        <v-alert class="mb-3 bg-red">NOTA: Al cambiar de contraseña deberá volver a iniciar
            sesión</v-alert>
        <v-form fast-fail validate-on="input" ref="changePasswordForm" v-model="formValid">
            <v-text-field label="Contraseña anterior" :rules='oldPasswordRules' v-model="oldPassword" clearable
                density="compact" type="password"></v-text-field>
            <v-text-field label="Contraseña nueva" :rules="passwordRules" v-model="newPassword" clearable density="compact"
                type="password"></v-text-field>

            <v-text-field label="Repetir contraseña" :rules="repeatPasswordRules" v-model="repeatPassword" clearable
                density="compact" type="password"></v-text-field>
            <v-container class="d-flex justify-space-around">
                <v-btn :disabled="!valid">Guardar contraseña
                    <form-confirmation-dialog v-model="showDialog" @cancel="hideDialog" :save="updatePassword" :active="showDialog" text="¿Estas seguro que deseas cambiar tu contraseña?"/>
                </v-btn>
                <v-btn @click="active = !active">Cancelar</v-btn>
            </v-container>
        </v-form>
    </v-container>
</template>
<script>
// import ChangePasswordDialog from '@/components/ChangePassword/ChangePasswordDialog.vue'
import FormConfirmationDialog from '../FormConfirmationDialog.vue';
export default {
    props: {
        active: Boolean,
        user: Object,
        valid: Boolean
    },
    components: {
        // ChangePasswordDialog,
        FormConfirmationDialog
    },
    data() {
        return {
            url:import.meta.env.VITE_API_URL,
            oldPassword: '',
            newPassword: '',
            repeatPassword: '',
            showDialog:false,
            incorrectPassword:false,
            samePassword:false,
            formValid: true,
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
                    if (value !== this.oldPassword) return true
                    return "La contraseña anterior y nueva son iguales"
                }
            ],
            repeatPasswordRules: [
                value => {
                    if (value.length > 0) return true
                    return 'Este campo es obligatorio.'
                },
                value => {
                    if (value === this.newPassword) return true
                    return 'Las contraseñas no coinciden'
                }
            ]
        }

    },
    methods: {
        requiredField(value) {
            if (value.length > 0) return true
            return 'Este campo es obligatorio'
        },
        emitCancel() {
            this.$emit('cancel', this.active)
        },
        hideDialog(){
            this.showDialog=false;
        },
        updatePassword() {
            this.$refs.changePasswordForm.validate()
            if (this.formValid) {
                this.$axios.patch(`http://${this.url}/user/change_password`, {
                    'old_password': this.oldPassword,
                    'new_password': this.newPassword,
                    'repeat_password': this.repeatPassword,
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
                        if ('samePassword' in err.response.data) this.samePassword = true;
                        else if('incorrectPassword' in err.response.data) this.incorrectPassword = true;
                        
                        this.showDialog = false;
                        this.$refs.changePasswordForm.validate();
                        // if(this.samePassword) this.samePassword = false;
                        // else this.incorrectPassword = false;
                        // setTimeout(()=>{
                        //     console.log('timeout')
                        //     this.$refs.changePasswordForm.reset()},2000)
                        // // if (err.response.status == 403) this.$router.push('/login')
                    });
            }


        },
        resetOldPasswordField(){
            if(this.incorrectPassword) this.incorrectPassword = false;
            else if(this.samePassword) this.samePassword = false;
        }

    },
    watch:{
        active:'emitCancel',
        oldPassword:'resetOldPasswordField'
    }
}
</script>
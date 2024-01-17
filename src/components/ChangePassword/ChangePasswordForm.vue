<template>
    <v-container v-if="user && active" class="d-flex flex-column w-75 ">
        <v-alert class="mb-3 bg-secondary">NOTA: Al cambiar de contraseña deberá volver a iniciar
            sesión</v-alert>
        <v-form fast-fail validate-on="input" ref="changePasswordForm">
            <v-text-field label="Contraseña anterior" :rules='oldPasswordRules' v-model="oldPassword" clearable
                density="compact" type="password"></v-text-field>
            <v-text-field label="Contraseña nueva" :rules="passwordRules" v-model="newPassword" clearable density="compact"
                type="password"></v-text-field>

            <v-text-field label="Repetir contraseña" :rules="repeatPasswordRules" v-model="repeatPassword" clearable
                density="compact" type="password"></v-text-field>
            <v-container class="d-flex justify-space-around">
                <v-btn :disabled="!valid">Guardar contraseña
                    <change-password-dialog />
                </v-btn>
                <v-btn @click="active = !active">Cancelar</v-btn>
            </v-container>
        </v-form>
    </v-container>
</template>
<script>
import ChangePasswordDialog from '@/components/ChangePassword/ChangePasswordDialog.vue'
export default {
    props: {
        active: Boolean,
        user: Object,
        valid: Boolean
    },
    components: {
        ChangePasswordDialog
    },
    data() {
        return {
            oldPassword: '',
            newPassword: '',
            repeatPassword: '',
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
    },
    watch:{
        active:'emitCancel'
    }
}
</script>
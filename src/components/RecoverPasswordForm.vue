<template>
    <div class="d-flex align-center justify-center" style="height: 100vh">
        <v-sheet width="30%" class="mx-auto pa-5" rounded elevation="5">
            <v-card-title class="text-center text-h5 mb-5">Recuperar contraseña</v-card-title>
            <v-form ref="recoveryForm" @submit.prevent="sendEmail" validate-on=" input submit lazy" v-model="valid"
                :disabled="loading">
                <v-text-field v-model="email" label="Correo electrónico" type="email" :rules="emailRules"
                    required></v-text-field>
                <v-btn :loading="loading" type="submit" color="primary" block class="mt-2">Enviar correo de
                    recuperación</v-btn>
                <v-btn color="white" block class="mt-2" to="/login">Cancelar</v-btn>
            </v-form>
        </v-sheet>
    </div>
</template>
<script>
export default {
    data() {
        return {
            loading: false,
            apiUrl: import.meta.env.VITE_API_URL,
            email: '',
            valid: true,
            emailRules: [
                value => {
                    if (value) return true
                    return 'Este campo es obligatorio'
                },
                value => {
                    if (/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/i.test(value)) return true
                    return 'Correo electrónico inválido'
                }
            ],

        }
    },
    methods: {
        async sendEmail() {
            try {
                const response = await this.$axios.post(
                    `http://${this.apiUrl}/user/recover-password`,
                    {
                        email: this.email
                    }
                );
                // localStorage.setItem('token', response.data.token);
                if (response.status == 200) {
                    this.$router.push('/');
                }
            } catch (error) {
                console.error(error);
            }
        }
    }
}

</script>
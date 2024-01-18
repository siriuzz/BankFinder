<template>
    <v-dialog v-model="active" class="justify-center" transition="dialog-bottom-transition" width="auto">
        <v-card class="w-auto pa-10">
            <v-card-title class="text-center text-h3"><v-icon color="red" icon="mdi-alert-circle"></v-icon></v-card-title>
            <v-card-text>Para poder utilizar esta funcionalidad, debes tener una cuenta creada</v-card-text>
            <v-sheet class="d-flex justify-center my-4">
                <v-btn class="w-25" to="/register">Regístrate</v-btn>
            </v-sheet>
            <v-sheet class="d-inline-flex align-center">

                <v-card-subtitle>¿Ya tienes una cuenta?</v-card-subtitle>
                <v-btn variant="tonal" size="small" to="/login">Iniciar sesión</v-btn>
            </v-sheet>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    props: {
        openDialog: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
            active: false
        }
    },
    watch: {
        openDialog(value) {
            this.active = value;
        }
    },
    methods: {
        closeDialog() {
            // Close the dialog by updating the prop
            this.$emit('openDialog', false);
        },
    },
}
</script>
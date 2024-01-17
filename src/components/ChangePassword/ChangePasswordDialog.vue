<template>
    <v-dialog activator="parent" width="auto">
        <v-card>
            <v-card-text>¿Estas seguro de que quieres cambiar tu contraseña?</v-card-text>
            <v-card-text>
                Al cambiar la contraseña, deberás iniciar sesión de nuevo
            </v-card-text>
            <v-card-actions>
                <v-container class="w-auto d-flex flex-row justify-space-around">
                    <v-btn block @click="changePassword" width="100" variant='outlined'>Cambiar
                        contraseña</v-btn>
                    <v-btn block @click="active = false" variant='outlined'>Cancelar</v-btn>
                </v-container>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    props:{
        active:Boolean
    }
}
</script>
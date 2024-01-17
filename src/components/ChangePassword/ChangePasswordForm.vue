<template>
    <v-container v-if="user && !edit_profile && change_password" class="d-flex flex-column w-75 ">
        <v-alert class="mb-3 bg-secondary">NOTA: Al cambiar de contraseña deberá volver a iniciar
            sesión</v-alert>
        <v-form fast-fail validate-on="input" v-model="changePasswordValid" ref="changePasswordForm">
            <v-text-field label="Contraseña anterior" :rules='oldPasswordRules' v-model="old_password" clearable
                density="compact" type="password"></v-text-field>
            <v-text-field label="Contraseña nueva" :rules="passwordRules" v-model="new_password" clearable density="compact"
                type="password"></v-text-field>

            <v-text-field label="Repetir contraseña" :rules="repeatPasswordRules" v-model="repeat_password" clearable
                density="compact" type="password"></v-text-field>
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
                                    <v-btn block @click="changePasswordDialog = false" variant='outlined'>Cancelar</v-btn>
                                </v-container>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-btn>
                <v-btn @click="change_password = !change_password">Cancelar</v-btn>
            </v-container>
        </v-form>
    </v-container>
</template>
<script>
export default {
    props:{
        changePassword:Boolean
    }
}
</script>
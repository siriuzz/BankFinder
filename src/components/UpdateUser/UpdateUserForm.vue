<template>
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
        <v-form @submit.prevent ref="updateUserForm" validate-on="input">
            <v-text-field label="Nombre" :rules="required" v-model="user.first_name" clearable
                density="compact"></v-text-field>
            <v-text-field label="Nombre de usuario" :rules="usernameRules" v-model="user.username" @change="checkUsername"
                clearable density="compact"></v-text-field>
            <v-container class="d-flex justify-space-around">
                <v-btn :disabled="!updateUserValid">Guardar cambios
                    <UpdateUserDialog/>
                </v-btn>
                <v-btn @click="edit_profile = !edit_profile">Cancelar</v-btn>
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
        edit_profile: Boolean,

    },
    components: {
    UpdateUserDialog,
}
}
</script>
<template>
    <v-dialog activator="parent" width="auto" v-model="active">
        <v-card class="pr-5">
            <v-card-text>¿Estas seguro de que quieres guardar los cambios?</v-card-text>
            <v-container class="d-flex">
                <v-card-actions>
                    <v-btn block @click="updateProfile" type="submit" variant='outlined'>Guardar</v-btn>
                    <v-btn block @click="active = false" variant='outlined'>Cancelar</v-btn>
                </v-card-actions>
            </v-container>
        </v-card>
    </v-dialog>
</template>
<script>
export default{
    data(){
        return{
            active:false
        }
    },
    props:{
        updateProfile:Function
    }
}
</script>
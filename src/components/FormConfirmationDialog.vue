<template>
    <v-dialog activator="parent" width="auto">
        <v-card>
            <v-card-text>{{ text }}</v-card-text>
            <v-card-actions>
                <v-container class="w-auto d-flex flex-row justify-space-around">
                    <v-btn block @click="save" width="100" variant='outlined'>{{ saveBtnText }}</v-btn>
                    <v-btn block @click="cancelAction" variant='outlined'>Cancelar</v-btn>
                </v-container>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>

export default {
    props:{
        active:Boolean,
        text:String,
        save:Function,
        saveBtnText:{
            type:String,
            default:'Guardar'
        },

    },
    methods:{
        cancelAction(){
            this.$emit('cancel',!this.active)
        }
    }
}
</script>
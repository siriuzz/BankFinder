<template>
    <v-card elevation="3" width="50%" class="ma-4">
        <v-container class="text-center">
            <v-card-title class="text-h3 py-6">Calculadora</v-card-title>
        </v-container>
        <v-container class="d-flex flex-column">

            <v-container class="d-flex ">
                <v-container class="w-auto ">
                    <v-card-text class="text-subtitle-1">DOP</v-card-text>
                </v-container>
                <v-text-field type="number"  variant="solo"></v-text-field>

            </v-container>
                <v-container class="d-flex">
                    <v-container class="w-auto">
                        <v-select density="compact"></v-select>
                    <!-- <v-card-text class="text-subtitle-1">DOP</v-card-text> -->

                    </v-container>
                    <v-text-field type="number" variant="solo"></v-text-field>

                </v-container>
        </v-container>
    </v-card>
</template>
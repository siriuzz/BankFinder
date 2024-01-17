<template>
    <v-card elevation="0" border width="55%" class="ma-4">
        <v-container class="text-center">
            <v-card-title class="text-h3 py-4">Calculadora</v-card-title>
        </v-container>
        <v-container class="py-0">
            <v-container class="h-1 py-0 w-25">
                <div class="text-subtitle-1 text-medium-emphasis">Modo</div>
                <v-select v-model="modeValue" :items="mode" item-text="title" item-value="value" variant="solo" hide-details
                    density="compact"></v-select>

            </v-container>
        </v-container>
        <v-container class="d-flex pa-0 ma-0">
            <v-container class="d-flex ">
                <!-- <v-container class="w-auto align-center">
                    <v-card-text class="text-subtitle-1">Monto</v-card-text>
                </v-container> -->
                <v-container class="h-1">
                    <div class="text-subtitle-1 text-medium-emphasis">Monto</div>

                    <v-text-field type="number" @input="convert" v-model="amount" hide-details prefix="$" variant="solo"
                        label="" density="compact"></v-text-field>
                </v-container>
            </v-container>
            <v-container class="d-flex ">
                <v-container class="h-1">
                    <div class="text-subtitle-1 text-medium-emphasis">De</div>
                    <v-select ref="fromSelect" :readonly="modeValue == 0" v-model="fromCurr" :items="currencies"
                        variant="solo" hide-details density="compact"></v-select>
                </v-container>
            </v-container>
            <v-sheet class="d-flex justify-center align-center pt-4">

                <v-icon icon="mdi-swap-horizontal"></v-icon>

            </v-sheet>
            <v-container class="d-flex ">
                <v-container class="">
                    <div class="text-subtitle-1 text-medium-emphasis">A</div>
                    <v-select ref="toSelect" v-model="toCurr" :readonly="modeValue == 1" :items="currencies" variant="solo"
                        hide-details density="compact"></v-select>
                    <!-- <v-card-text class="text-subtitle-1">DOP</v-card-text> -->
                </v-container>

            </v-container>

        </v-container>
        <v-container v-if="toCurr && amount && fromCurr">
            <v-sheet v-if="modeValue == 0">
                <v-sheet class="text-h6 font-weight-light">

                    {{ amount }} DOP
                </v-sheet>
                <v-sheet class="text-h5 font-weight-bold">

                    Resultado: {{ result }} {{ toCurr }}
                </v-sheet>
            </v-sheet>
            <v-sheet v-if="modeValue == 1">
                <v-sheet class="text-h6 font-weight-light">

                    {{ amount }} {{ fromCurr }}
                </v-sheet>
                <v-sheet class="text-h5 font-weight-bold">

                    Resultado: {{ result }} DOP
                </v-sheet>
            </v-sheet>
        </v-container>
    </v-card>
</template>
<script>

export default {
    data() {
        return {
            amount: '',
            fromCurr: 'DOP',
            toCurr: '',
            currencies: [],
            result: 0,
            mode: [{ title: 'Compra', value: 0 }, { title: 'Venta', value: 1 }],
            modeValue: 0,
        }
    },
    props: {
        exchanges: Array
    },
    methods: {
        convert() {
            let convertRate = 0;
            let found = false;

            const keyLookUp = this.modeValue == 0 ? this.toCurr : this.fromCurr;
            for (let i = 0; i < this.exchanges.length; i++) {
                const obj = this.exchanges[i]
                if (obj.currency.currency_code == keyLookUp) found = true;
                // console.log(obj.currency.currency_code, found)
                if (found) {
                    if (this.modeValue == 0) convertRate = obj.selling_at;
                    else if (this.modeValue == 1) convertRate = obj.buying_at;
                    break;
                }
            }
            console.log(this.amount, convertRate)
            if (this.modeValue == 0) this.result = (parseFloat(this.amount) / parseFloat(convertRate)).toFixed(2);
            else this.result = (parseFloat(this.amount).toFixed(2) * parseFloat(convertRate)).toFixed(2);
        },
        getCurrencies() {
            // console.log('holaaaaa')
            const arr = this.exchanges;
            if (this.exchanges) {
                console.log(arr);
                for (let i in arr) {
                    console.log(arr[i].currency.currency_code)
                    this.currencies.push(arr[i].currency.currency_code)
                }
            }
        },
        switchModes() {
            console.log("este es el valor" + this.modeValue)
            if (this.modeValue == 0) {
                this.fromCurr = "DOP"
                this.toCurr = ""
            } else {
                this.toCurr = "DOP"
                this.fromCurr = ""

            }
        },
        validateAmount() {
            if (parseFloat(this.amount) < 0) this.amount = 0
        }
    },
    watch: {
        exchanges: {
            handler: 'getCurrencies', // Call the method when 'exchanges' changes
            immediate: true, // Call the method immediately on component creation
        },
        modeValue: 'switchModes',
        toCurr: 'convert',
        fromCurr: 'convert',
        amount: {
            handler: 'validateAmount',
            immediate: true,
            flush:'post'
        }
    },

}
</script>
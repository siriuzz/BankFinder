<template>
    <v-responsive>
        <v-sheet class="px-5 text-h5 font-weight-bold">
            Sucursales
            <v-slide-group>
                <v-slide-group-item v-for="branch in branches" :key="branch.branch_id">
                    <v-card class="ma-1 d-flex flex-column flex-md-0-1 " elevation="3">
                        <v-card-title >{{ branch.branch_name }}</v-card-title>
                        <v-card-text >
                            Ubicación: {{ branch.location }} <br/>
                            Contacto: {{ branch.branch_contact_number }}<br/>
                            Hora de apertura: {{ branch.opening_hour }}<br/>
                            Hora de cierre: {{ branch.closing_hour  }}<br/>
                        </v-card-text>


                    </v-card>

                </v-slide-group-item>
            </v-slide-group>
        </v-sheet>
    </v-responsive>
</template>
<script>
export default {
    props: {
        branches: Array
    },
    data() {
        return {

        }
    },
    computed: {
        parseTime() {
            const hoursArr = [this.branches[0].opening_hour, this.branches[0].closing_hour]
            console.log(this.branches.opening_hour)
            for(const hour in hoursArr) {
                

                const baseDate = new Date("1970-01-01"); // Use a specific date, such as "1970-01-01"

                // Extract hours, minutes, and seconds from the time string
                const [hours, minutes, seconds] = hour.split(":").map(Number);

                // Set the time on the base date
                baseDate.setHours(hours);
                baseDate.setMinutes(minutes);
                baseDate.setSeconds(seconds);

                // Format the time as "7pm" or "6am"
                const formattedTime = baseDate.toLocaleTimeString([], { hour: "numeric", minute: "2-digit", hour12: true });

                return formattedTime
            }
        }
    }
}
</script>
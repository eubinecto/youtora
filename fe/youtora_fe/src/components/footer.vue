<template>
    <div id="Foot" class="overflow-auto">
        <b-pagination
                v-model="currentPage"
                :total-rows="rows"
                :per-page="this.$store.state.search.perPage"
                align="center"
        />
    </div>
</template>

<script>
    export default {
        name: 'Foot',
        data() {
            return {
                rows: 60,
                currentPage: 1,
            }
        },
        methods: {

        },
        watch: {
            // currentPage: function(val) {
            //     //do something when the data changes.
            //     if (val) {
            //         this.$store.commit('SET_CURRENT_PAGE', val)
            //         console.log(this.$store.state.currentPage)
            //     }
            // }
        }
    }
</script>

<style>

</style>
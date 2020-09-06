<template>
    <div id="generalSearchPagination" class="overflow-auto">
<!--        <b-pagination-->
<!--                v-model="currentPage"-->
<!--                :total-rows="this.$store.state.videoTotalCount"-->
<!--                :per-page="this.$store.state.search.perPage"-->
<!--                align="center"-->
<!--        />-->
    </div>
</template>

<script>
    export default {
        name: 'generalSearchPagination',
        data() {
            return {
                // currentPage: 1
            }
        },
        methods: {

        },
        watch: {
            // currentPage: function(val) {
            //     //do something when the data changes.
            //     if (val) {
            //         this.$store.commit('SET_CURRENT_PAGE', val)
            //         this.$store.dispatch('SEARCH_VIDEOS')
            //     }
            // }
        }
    }
</script>

<style>

</style>
<template>
    <div id="generalSearch">
        <general-search-bar/>
        <general-search-video-list/>
        <general-search-pagination v-if="$store.state.generalSearch.videoQueryResult.length > 0"/>
    </div>
</template>

<script>
    import generalSearchPagination from "./generalSearchPagination";
    import generalSearchVideoList from "./generalSearchVideoList";
    import generalSearchBar from "./generalSearchBar";

    export default {
        name: 'generalSearchRouter',
        components: {
            generalSearchBar,
            generalSearchPagination,
            generalSearchVideoList
        },
        data () {
            return {

            }
        },
        beforeMount() {
            this.$store.commit('generalSearch/SET_SEARCH_QUERY', this.$route.query.query)
            this.$store.dispatch('generalSearch/SEARCH_VIDEOS')
        }
    }
</script>

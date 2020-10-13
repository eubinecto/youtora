<template>
    <div id="generalSearch">
        <general-search-bar/>
        <general-search-video-list/>
        <general-search-pagination/>
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
        }
    }
</script>

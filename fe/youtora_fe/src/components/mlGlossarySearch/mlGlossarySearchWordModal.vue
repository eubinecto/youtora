<template>
    <div id="mlWordModal">
        <b-modal
                size="xl"
                scrollable
                ref="mlModal"
                :ok-only=true
                ok-title="Close"
                ok-variant="success"
                @hide="$emit('modal-hide')"
                :title-html="this.modalWord.charAt(0).toUpperCase() + this.modalWord.slice(1)">

            <div class="referenceLink mb-4" style="font-size: 75%">
                <span><i>Reference :</i></span>
                <a :href="this.credit">{{ this.credit }}</a>
            </div>

            <div class="wordDescription">
                <span v-html="this.modalDesc"></span>
            </div>

            <br/>
            <div class="spinner-grow text-info" role="status" v-if="modalLoading === true" style="margin-top: 20%">
                <span class="sr-only">Loading...</span>
            </div>
            <ml-glossary-search-result v-if="modalLoading === false"/>
            <ml-glossary-search-pagination v-if="modalLoading === false"/>
        </b-modal>
    </div>
</template>

<script>
    import mlGlossarySearchPagination from "./mlGlossarySearchPagination";
    import mlGlossarySearchResult from "./mlGlossarySearchResult";
    export default {
        name: 'mlWordModal',
        components:{
            mlGlossarySearchResult,
            mlGlossarySearchPagination
        },
        props: {
            modalShow: Boolean,
            modalWordId: String,
        },
        data () {
            return {

            }
        },
        methods: {
            setModal: function() {
                this.$store.commit('mlGlossary/SET_SEARCH_QUERY', this.modalWord)
                this.$store.dispatch('mlGlossary/SEARCH_WORD')
            },
            imageResize: function(htmlString) {
                return htmlString.split('<img src="').join('<img style="width: 500px%; height: auto; padding: 10px" src="')
            },
            addHyperEndpoint: function(htmlString) {
                // return this.imageResize(htmlString).split('<a href="#').join('<a href="https://developers.google.com/machine-learning/glossary/#')
                return this.imageResize(htmlString).split('<a href="#').join('<a href="#ml_gloss|')
            },
        },
        watch: {
            '$route': function () {
                if (this.$route.hash.length > 0) {
                    this.$store.commit('mlGlossary/SET_WORD_ID', this.$route.hash.slice(1))
                    this.$store.dispatch('mlGlossary/SEARCH_WORD_DETAIL')
                }
            },
            modalShow: function(val) {
                if (val) {
                    this.$refs['mlModal'].show()
                } else {
                    this.$refs['mlModal'].hide()
                    this.$router.push({path: '/mlGlossarySearch'})
                }
            },
        },
        computed: {
            modalDesc() {
                return this.addHyperEndpoint(this.$store.state.mlGlossary.wordDesc)
            },
            credit() {
                return this.$store.state.mlGlossary.wordCredit
            },
            modalWord () {
                return this.$store.state.mlGlossary.searchQuery
            },
            modalLoading() {
                return this.$store.state.mlGlossary.isModalLoading
            }
        },
        beforeMount() {
            if (this.$route.hash.length > 0) {
                this.$store.commit('mlGlossary/SET_WORD_ID', this.$route.hash.slice(1))
                this.$store.dispatch('mlGlossary/SEARCH_WORD_DETAIL')

            }

        },




    }

</script>

<style>


</style>
<template>
    <div id="mlWordBucket">
        <div class="spinner-grow text-info" role="status" v-if="isLoading === true" style="margin-top: 20%">
            <span class="sr-only">Loading...</span>
        </div>
        <div v-if="isLoading === false">
            <b-card-group v-for="alphabet in Object.keys(alphabetGlossaries)" :key="alphabet">
                <b-card align="left">
                    <h3>{{ alphabet.toUpperCase() }}</h3>
                    <b-card-group>
                        <div v-for="item in alphabetGlossaries[alphabet]" :key="item._id">
                            <b-card class="border-white">
                                <b-button
                                        @click="onModal(item)"
                                >
                                    {{ item.word.charAt(0).toUpperCase() + item.word.slice(1) }}
                                </b-button>
                            </b-card>
                        </div>
                    </b-card-group>
                </b-card>
            </b-card-group>
        </div>

        <ml-glossary-search-word-modal
                @modal-hide="this.offModal"
                :modal-show="this.modalShow"
                :modal-word-id="this.modalWordId"
        />

    </div>
</template>

<script>
    import mlGlossarySearchWordModal from "./mlGlossarySearchWordModal";

    export default {
        name: 'mlWordBucket',
        components:{
            mlGlossarySearchWordModal
        },
        data() {
            return {
                modalShow: false,
                modalWordId: '',
            }
        },
        methods: {
            offModal: function () {
                this.modalShow = false
                this.$store.commit('mlGlossary/CLEAR_RESULTS')
            },
            onModal: function(itemObj) {
                this.modalShow = true
                this.modalWordId = itemObj._id
                this.$store.commit('mlGlossary/SET_WORD_ID', this.modalWordId)
                this.$store.dispatch('mlGlossary/SEARCH_WORD_DETAIL')

                this.$router.push({path: '/MLGlossarySearch', hash: '#'+this.modalWordId})
            },
            getAlphabetGlossary: function() {
                const glossaries = this.glossaries
                var glossaryDict = {
                    'a': [],
                    'b': [],
                    'c': [],
                    'd': [],
                    'e': [],
                    'f': [],
                    'g': [],
                    'h': [],
                    'i': [],
                    'j': [],
                    'k': [],
                    'l': [],
                    'm': [],
                    'n': [],
                    'o': [],
                    'p': [],
                    'q': [],
                    'r': [],
                    's': [],
                    't': [],
                    'u': [],
                    'v': [],
                    'w': [],
                    'x': [],
                    'y': [],
                    'z': []

                }
                for (let i = 0; i < glossaries.length; i++) {
                    var curWord = glossaries[i].word
                    curWord = curWord.charAt(0).toUpperCase() + curWord.slice(1)
                    var firstChar = curWord.charAt(0).toLowerCase()

                    glossaryDict[firstChar].push(glossaries[i])
                }

                return glossaryDict
            },
            getGlossaryList: function () {
                this.$store.dispatch('mlGlossary/SEARCH_GLOSSARY')
            },

        },
        beforeMount: function () {
            this.getGlossaryList()
        },
        mounted() {
            if (this.$route.hash.length > 0) {
                this.modalWordId = this.$route.hash.slice(1)
                this.modalShow = true
            }
        },
        computed: {
            isLoading() {
                return this.$store.state.mlGlossary.isLoadingGlossaries
            },
            glossaries() {
                return this.$store.state.mlGlossary.glossaryList
            },
            alphabetGlossaries(){
                return this.getAlphabetGlossary()
            }
        }
    }
</script>

<style>

</style>
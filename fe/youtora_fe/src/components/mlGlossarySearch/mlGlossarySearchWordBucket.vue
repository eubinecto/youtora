<template>
    <div id="mlWordBucket">

        <b-card-group v-for="alphabet in Object.keys(alphabetGlossaries)" :key="alphabet">
            <b-card align="left">
                <h3>{{ alphabet.toUpperCase() }}</h3>
                <b-card-group>
                    <div v-for="item in alphabetGlossaries[alphabet]" :key="item._id">
                        <b-card class="border-white">
                            <b-button @click="setModal(item)">{{ item.word.charAt(0).toUpperCase() + item.word.slice(1) }}</b-button>
                        </b-card>
                    </div>
                </b-card-group>
            </b-card>
        </b-card-group>

        <b-modal size="xl" v-model="modalShow" :title-html="this.modalWord.charAt(0).toUpperCase() + this.modalWord.slice(1)">
            <div class="referenceLink mb-4" style="font-size: 75%">
                <span><i>Reference :</i></span>
                <a :href="this.credit">{{ this.credit }}</a>
            </div>

            <div class="wordDescription">
                <span v-html="this.modalDesc"></span>
            </div>


            <br/>

            <ml-glossary-search-result/>
            <ml-glossary-search-pagination/>
        </b-modal>
    </div>
</template>

<script>
    import mlGlossarySearchPagination from "./mlGlossarySearchPagination";
    import mlGlossarySearchResult from "./mlGlossarySearchResult";

    export default {
        name: 'mlWordBucket',
        components:{
            mlGlossarySearchResult,
            mlGlossarySearchPagination
        },
        data() {
            return {
                modalShow: false,
                modalWord: '',
                modalDesc: '',
                credit: ''
            }
        },
        methods: {
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
            setModal: function(item) {
                this.modalShow = !this.modalShow
                this.modalWord = item.word
                this.modalDesc = this.addHyperEndpoint(item.desc.desc_raw)
                this.credit = item.credit

                this.$store.commit('mlGlossary/SET_SEARCH_QUERY', this.modalWord)
                this.$store.dispatch('mlGlossary/SEARCH_WORD')
            },
            addHyperEndpoint: function(htmlString) {
                return htmlString.split('<a href="#').join('<a href="https://developers.google.com/machine-learning/glossary/#')
            },
            replaceHypertoButton: function(htmlString) {
                const linkTag = new RegExp("<a href=\"#(.+?)\">", "gi")
                const linkCloseTag = new RegExp("</a>", "gi")

                const buttonOpen = htmlString.toString().replace(linkTag, '<b-button @click="onNewModal(\''+'$1'+'\')">')
                const buttonClose = buttonOpen.toString().replace(linkCloseTag, '</b-button>')
                return buttonClose
            },
            onNewModal: function(newModalString) {
                this.modalShow = false
                const firstChar = newModalString.charAt(0).toLowerCase()
                const targetList = this.alphabetGlossaries[firstChar]

                for (var i = 0; i < targetList.length ; i++) {
                    if (targetList[i].word.includes(newModalString)) {
                        try {
                            this.setModal(targetList[i])
                        } catch (err) {
                            console.log(err)
                        }

                    }
                }

            },

        },
        beforeMount: function () {
            this.getGlossaryList()
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
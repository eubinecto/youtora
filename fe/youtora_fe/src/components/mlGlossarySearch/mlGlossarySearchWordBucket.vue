<template>
    <div id="mlWordBucket">

        <b-card-group v-for="alphabet in Object.keys(alphabetGlossaries)" :key="alphabet">
            <b-card align="left">
                <h3>{{ alphabet.toUpperCase() }}</h3>
                <b-card-group>
                    <div v-for="item in alphabetGlossaries[alphabet]" :key="item._id">
                        <b-card>
                            <b-button @click="setModal(item)">{{ item.word }}</b-button>
                        </b-card>
                    </div>
                </b-card-group>
            </b-card>
        </b-card-group>
        <b-modal v-model="modalShow" :title="this.modalWord">
            description: <br/>
            {{ this.modalDesc }}
        </b-modal>
    </div>
</template>

<script>
    export default {
        name: 'mlWordBucket',
        data() {
            return {
                modalShow: false,
                modalWord: '',
                modalDesc: ''
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
                    var curWord = glossaries[i].word.replace(/ /g, "")
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
                this.modalDesc = item.desc_raw
            }
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
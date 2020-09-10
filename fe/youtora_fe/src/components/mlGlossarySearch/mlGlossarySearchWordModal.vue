<template>
    <div id="mlGlossaryModal">

        <b-modal id="modal-scrollable" scrollable title="Scrollable Content"
                size="xl" v-model="modalShow"
                 :ok-only=true
                 ok-title="Close"
                 :lazy=true
                 @ok="hidingModal"
                 @hide="hidingModal"
                 :title-html="this.getOrgWord(this.targetWord).charAt(0).toUpperCase() +
                 this.getOrgWord(this.targetWord).slice(1)">

            <div class="referenceLink mb-4" style="font-size: 75%">
                <span><i>Reference :</i></span>
                <a :href="this.targetCredit">{{ this.targetCredit }}</a>
            </div>

            <div class="wordDescription">
                <span v-html="this.targetDesc"></span>
            </div>

            <br/>
            <div class="spinner-grow text-info" role="status" v-if="isLoadingVideos === true" style="margin-top: 40%">
                <span class="sr-only">Loading...</span>
            </div>
            <ml-glossary-search-result v-if="isLoadingVideos === false"/>
            <ml-glossary-search-pagination v-if="isLoadingVideos === false"/>
        </b-modal>
    </div>
</template>

<script>
    import mlGlossarySearchPagination from "./mlGlossarySearchPagination";
    import mlGlossarySearchResult from "./mlGlossarySearchResult";

    export default {
        name: 'mlGlossaryModal',
        components: {
            mlGlossarySearchPagination,
            mlGlossarySearchResult
        },
        props: {

        },
        beforeMount () {
            this.getGlossaryList()
        },
        data() {
            return {
                modalShow: true,
                targetWord: this.$route.params.word,
                targetDesc: '',
                targetCredit: ''
            }
        },
        methods: {
            imageResize: function(htmlString) {
                return htmlString.split('<img src="').join('<img style="width: 500px%; height: auto; padding: 10px" src="')
            },
            addHyperEndpoint: function(htmlString) {
                return this.imageResize(htmlString).split('<a href="#').join('<a href="https://developers.google.com/machine-learning/glossary/#')
            },
            getGlossaryList: function () {
                this.$store.commit('mlGlossary/SET_SEARCH_QUERY', this.getOrgWord(this.targetWord))
                this.$store.dispatch('mlGlossary/SEARCH_GLOSSARY')

                this.getDesc(this.getOrgWord(this.targetWord))
                this.getCredit(this.getOrgWord(this.targetWord))
                console.log(this.targetCredit)
                console.log(this.targetDesc)
                this.$store.dispatch('mlGlossary/SEARCH_WORD', this.getOrgWord(this.targetWord))
            },
            getOrgWord: function(convWord) {
                return convWord.split('_').join(' ')
            },
            getDesc: function(targetWord) {
                const firstChar = targetWord.charAt(0).toLowerCase()
                const charList = this.$store.state.mlGlossary.glossaryDict[firstChar]
                for (var i=0; i < charList.length; i++) {
                    if (charList[i].word === targetWord) {
                        this.targetDesc = this.addHyperEndpoint(charList[i].desc.desc_raw)
                        break
                    }
                }
            },
            getCredit: function (targetWord) {
                const firstChar = targetWord.charAt(0).toLowerCase()
                const charList = this.$store.state.mlGlossary.glossaryDict[firstChar]
                for (var i=0; i < charList.length; i++) {
                    if (charList[i].word === targetWord) {
                        this.targetCredit = charList[i].credit
                        break
                    }
                }
            },
            hidingModal: function() {
                console.log(this.$store.state.mlGlossary.glossaryDict)
                this.modalShow = false
                this.$router.push({path: '/MLGlossarySearch'})

            }
        },
        mounted() {

        },
        computed: {
            isLoadingVideos() {
                return this.$store.state.mlGlossary.isLoadingVideos
            },
        }
    }

</script>

<style>


</style>
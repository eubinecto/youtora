<template>
    <div id="mlWordModal">
        <b-modal
                size="xl"
                ref="mlModal"
                :ok-only=true
                ok-title="Close"
                ok-variant="success"
                @hide="$emit('modal-hide')"
                :title-html="this.modalWord.charAt(0).toUpperCase() + this.modalWord.slice(1)">
            {{ this.modalShow }}
            {{ this.modalWordId }}

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
                modalWord: '',
                modalDesc: '',
                credit: ''
            }
        },
        methods: {
            setModal: function(item) {
                this.modalWord = item.word
                this.modalWordId = item._id
                this.modalDesc = this.addHyperEndpoint(item.desc.desc_raw)
                this.credit = item.credit

                this.$store.commit('mlGlossary/SET_SEARCH_QUERY', this.modalWord)
                this.$store.dispatch('mlGlossary/SEARCH_WORD')
            },
            imageResize: function(htmlString) {
                return htmlString.split('<img src="').join('<img style="width: 500px%; height: auto; padding: 10px" src="')
            },
            addHyperEndpoint: function(htmlString) {
                return this.imageResize(htmlString).split('<a href="#').join('<a href="https://developers.google.com/machine-learning/glossary/#')
            },
            replaceHypertoButton: function(htmlString) {
                const linkTag = new RegExp("<a href=\"#(.+?)\">", "gi")
                const linkCloseTag = new RegExp("</a>", "gi")

                const buttonOpen = this.imageResize(htmlString).toString().replace(linkTag, '<b-button @click="onNewModal(\''+'$1'+'\')">')
                const buttonClose = buttonOpen.toString().replace(linkCloseTag, '</b-button>')
                return buttonClose
            },
        },
        watch: {
            modalShow: function(val) {
                if (val) {
                    this.$refs['mlModal'].show()
                } else {
                    this.$refs['mlModal'].hide()
                    this.$router.push({path: '/mlGlossarySearch'})
                }
            }
        }

    }

</script>

<style>


</style>
<template>
    <div id="mlWordBucket">
        <div class="spinner-grow text-info" role="status" v-if="isLoading === true" style="margin-top: 40%">
            <span class="sr-only">Loading...</span>
        </div>
        <div class="loaded" v-if="isLoading === false">
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
        </div>

        <router-view/>

    </div>
</template>

<script>
    export default {
        name: 'mlWordBucket',
        components:{
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
            getModalWord: function (orgString) {
                return orgString.split(' ').join('_')
            },
            getGlossaryList: function () {
                this.$store.dispatch('mlGlossary/SEARCH_GLOSSARY')
            },
            setModal: function(item) {
                this.modalWord = item.word

                // this.$store.commit('mlGlossary/SET_TARGET_CREDIT', item.credit)
                // this.$store.commit('mlGlossary/SET_TARGET_DESC', this.addHyperEndpoint(item.desc.desc_raw))
                //
                // this.$store.commit('mlGlossary/SET_SEARCH_QUERY', this.modalWord)
                // this.$store.dispatch('mlGlossary/SEARCH_WORD')
                this.$router.push({path: '/MLGlossarySearch/'+this.getModalWord(item.word)})
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
            alphabetGlossaries(){
                return this.$store.state.mlGlossary.glossaryDict
            }
        }
    }
</script>

<style>

</style>
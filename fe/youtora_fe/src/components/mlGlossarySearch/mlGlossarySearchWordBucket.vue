<template>
    <div id="mlWordBucket">
        <b-card-group>
            <div v-for="item in glossaries" :key="item._id">
                <b-card>
                    <b-button @click="setModal(item)">{{ item.word }}</b-button>
                </b-card>
            </div>
            <b-modal v-model="modalShow" :title="this.modalWord">
                description: <br/>
                {{ this.modalDesc }}
            </b-modal>
        </b-card-group>
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
            }
        }
    }
</script>

<style>

</style>
<template>
    <div id="mlWordBucket">
        {{ this.$store.state.glossaryList }}
    </div>
</template>

<script>
    export default {
        name: 'mlWordBucket',
        props: {

        },
        methods: {
            getGlossaryList: function() {
                this.$store.dispatch('SEARCH_GLOSSARY')
            }
        },
        mounted() {
            this.getGlossaryList()
        },
        data() {
            return {
                glossary: this.$store.state.glossaryList
            }
        }
    }
</script>

<style>

</style>
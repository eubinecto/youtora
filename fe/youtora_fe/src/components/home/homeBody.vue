<template>
    <div id="homeBody">
        <b-form @submit="onSubmit">
            <b-form-group id="input-group-2" label-for="input-2" class="ml-4 mr-4 mt-4">
                <b-input-group>
                    <b-form-input
                            id="input-2"
                            v-model="query"
                            required
                            placeholder="Search Here"
                    ></b-form-input>
                    <b-input-group-append>
                        <b-button type="submit" variant="info"><b-icon icon="search"></b-icon></b-button>
                    </b-input-group-append>
                </b-input-group>
            </b-form-group>
        </b-form>

    </div>
</template>

<script>
    export default {
        name: 'homeBody',
        data() {
            return {
                query: '',
            }
        },
        watch: {
            query: function (val) {
                //do something when the data changes.
                if (val) {
                    this.$store.commit('generalSearch/SET_SEARCH_QUERY', val)
                }
            },
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()

                this.$store.commit('generalSearch/SET_PER_PAGE', 5)
                this.$store.commit('generalSearch/SET_SEARCH_LANGUAGE', 'en')
                this.$store.commit('generalSearch/SET_SEARCH_QUERY', this.query)
                this.$store.commit('generalSearch/SET_CHAN_LANG', 'en')
                this.$store.dispatch('generalSearch/SEARCH_VIDEOS')
                this.$router.push({path: '/generalSearch'})
            },
        }
    }
</script>

<style>

</style>
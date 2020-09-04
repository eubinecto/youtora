<template>
    <div id="generalSearchBar">
        <b-form @submit="onSubmit" @reset="onReset" v-if="show">

            <b-form-group id="input-group-2" label="Search Bar" label-for="input-2">
                <b-form-input
                        id="input-2"
                        v-model="form.query"
                        required
                        placeholder="Search Here"
                ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-3" label="Target Language:" label-for="input-3">
                <b-form-radio-group
                        id="langId"
                        v-model="lang"
                        :options="optLang"
                        class="mb-3"
                        value-field="item"
                        text-field="name"
                        name="langId"
                ></b-form-radio-group>
            </b-form-group>

            <b-form-group label="perPageRadio">
                <b-form-radio-group
                        id="perPage"
                        v-model="perPage"
                        :options="optPerPage"
                        class="mb-3"
                        value-field="item"
                        text-field="name"
                        name="perPage"
                ></b-form-radio-group>
            </b-form-group>

            <b-button type="submit" variant="primary">Submit</b-button>
        </b-form>
    </div>
</template>

<script>
    export default {
        name: 'generalSearchBar',

        data() {
            return {
                perPage: 5,
                optPerPage : [
                    {item: 3, 'name': 3},
                    {item: 5, 'name': 5},
                    {item: 10, 'name': 10},
                ],
                form: {
                    query: '',
                },
                lang:'en',
                optLang:[
                    {item: 'ko', 'name': 'Korean'},
                    {item: 'en', 'name': 'English'},
                    {item: 'fr', 'name': 'French'},
                    {item: 'jp', 'name': 'Japanese'},
                ],
                show: true
            }
        },
        watch: {
            perPage: function(val) {
                //do something when the data changes.
                if (val) {
                    this.$store.commit('SET_PER_PAGE', val)
                }
            },
            lang: function(val) {
                //do something when the data changes.
                if (val) {
                    this.$store.commit('SET_SEARCH_LANGUAGE', val)
                }
            },
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()

                this.$store.commit('SET_PER_PAGE', this.perPage)
                this.$store.commit('SET_SEARCH_LANGUAGE', this.lang)
                this.$store.commit('SET_SEARCH_QUERY', this.form.query)

                this.$store.dispatch('SEARCH_VIDEOS')
            },
            onReset(evt) {
                evt.preventDefault()
                // Reset our form values
                this.perPage = 5
                this.form.query = ''
                this.lang = 'en'

                // Trick to reset/clear native browser form validation state
                this.show = false
                this.$nextTick(() => {
                    this.show = true
                })
            }
        }
    }
</script>

<style>

</style>

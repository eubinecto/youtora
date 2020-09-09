<template>
    <div id="generalSearchBar">
        <b-form @submit="onSubmit" @reset="onReset" v-if="show">
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

            <b-card-group style="font-size: 100%; font-weight: bold" class="mt-0">
                <b-card class="border-white">
                    <b-form-group id="input-group-3" label="Subtitle Language:" label-for="input-3">
                        <b-form-radio-group
                                id="langId"
                                v-model="lang"
                                :options="optLang"
                                class="mb-3"
                                value-field="item"
                                text-field="name"
                                button-variant="outline-info"
                                buttons
                                name="langId"
                        ></b-form-radio-group>
                    </b-form-group>
                </b-card>

                <b-card class="border-white">
                    <b-form-group id="input-group-4" label="Channel Language:" label-for="input-3">
                        <b-form-radio-group
                                id="chan_lang"
                                v-model="chan_lang"
                                :options="chan_opt_lang"
                                class="mb-3"
                                value-field="item"
                                text-field="name"
                                button-variant="outline-info"
                                buttons
                                name="chan_lang"
                        ></b-form-radio-group>
                    </b-form-group>
                </b-card>
            </b-card-group>

            <b-card-group style="font-size: 100%; font-weight: bold" class="mt-0">
                <b-card class="border-white">
                    <b-form-group id="input-group-5" label="Subtitle Search by" label-for="input-3">
                        <b-form-radio-group
                                id="ccType"
                                v-model="cc_type"
                                :options="cc_opt_type"
                                class="mb-3"
                                value-field="item"
                                text-field="name"
                                button-variant="outline-info"
                                buttons
                                name="ccType"
                        ></b-form-radio-group>
                    </b-form-group>
                </b-card>

                <b-card class="border-white">
<!--                    <b-form-group id="input-group-6" label="Channel Language:" label-for="input-3">-->
<!--                        <b-form-radio-group-->
<!--                                id="chan_lang"-->
<!--                                v-model="chan_lang"-->
<!--                                :options="chan_opt_lang"-->
<!--                                class="mb-3"-->
<!--                                value-field="item"-->
<!--                                text-field="name"-->
<!--                                button-variant="outline-info"-->
<!--                                buttons-->
<!--                                name="chan_lang"-->
<!--                        ></b-form-radio-group>-->
<!--                    </b-form-group>-->
                </b-card>
            </b-card-group>

<!--            <b-card class="border-white">-->
<!--                <b-button type="submit" variant="primary">Submit</b-button>-->
<!--                <b-button type="reset" variant="danger">Reset</b-button>-->
<!--            </b-card>-->

        </b-form>

        <b-card-group v-if="this.$store.state.generalSearch.videoQueryResult.length > 0">
            <b-card style="font-size: 100%; font-weight: bold" class="border-white">
                <b-form-group label="per_page" class="ml-4 mr-4">
                    <b-form-select
                            style="width: 30%"
                            id="perPage"
                            v-model="perPage"
                            :options="optPerPage"
                            value-field="item"
                            text-field="name"
                            name="perPage"
                    ></b-form-select>
                </b-form-group>
            </b-card>
        </b-card-group>
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

                query: this.$store.state.generalSearch.search.query,

                lang:'',
                optLang:[
                    {item: '', 'name': 'All'},
                    {item: 'ko', 'name': 'Korean'},
                    {item: 'en', 'name': 'English'},
                    {item: 'fr', 'name': 'French'},
                    {item: 'jp', 'name': 'Japanese'},
                ],
                chan_lang: '',
                chan_opt_lang:[
                    {item: '', 'name': 'All'},
                    {item: 'ko', 'name': 'Korean'},
                    {item: 'en', 'name': 'English'},
                    {item: 'fr', 'name': 'French'},
                    {item: 'jp', 'name': 'Japanese'},
                ],
                cc_type: '',
                cc_opt_type: [
                    {item: '', 'name': 'All'},
                    {item: 'auto', 'name': 'Auto'},
                    {item: 'man', 'name': 'Manual'},
                ],

                show: true
            }
        },
        watch: {
            query: function(val) {
                //do something when the data changes.
                if (val) {
                    this.$store.commit('generalSearch/SET_SEARCH_QUERY', val)
                }
            },
            perPage: function(val) {
                //do something when the data changes.
                if (val) {
                    this.$store.commit('generalSearch/SET_PER_PAGE', val)
                    this.$store.dispatch('generalSearch/SEARCH_VIDEOS')
                }
            },
            lang: function(val) {
                //do something when the data changes.
                if (val) {
                    this.$store.commit('generalSearch/SET_SEARCH_LANGUAGE', val)

                    if (this.$store.state.generalSearch.videoQueryResult.length > 0 || this.query.length > 0) {
                        this.$store.dispatch('generalSearch/SEARCH_VIDEOS')
                    }
                }
            },
            chan_lang: function (val) {
                this.$store.commit('generalSearch/SET_CHAN_LANG', val)

                if (this.$store.state.generalSearch.videoQueryResult.length > 0 || this.query.length > 0) {
                    this.$store.dispatch('generalSearch/SEARCH_VIDEOS')
                }
            },
            cc_type: function (val) {
                this.$store.commit('generalSearch/SET_CC_TYPE', val)

                if (this.$store.state.generalSearch.videoQueryResult.length > 0 || this.query.length > 0) {
                    this.$store.dispatch('generalSearch/SEARCH_VIDEOS')
                }
            },
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()

                this.$store.commit('generalSearch/SET_PER_PAGE', this.perPage)
                this.$store.commit('generalSearch/SET_SEARCH_LANGUAGE', this.lang)
                this.$store.commit('generalSearch/SET_SEARCH_QUERY', this.query)
                this.$store.commit('generalSearch/SET_CHAN_LANG', this.chan_lang)
                this.$store.dispatch('generalSearch/SEARCH_VIDEOS')
            },
            onReset() {
                // Reset our form values
                this.perPage = 5
                this.query = ''
                this.lang = 'en'
                this.chan_lang = 'en'
                this.$store.commit('generalSearch/CLEAR_SEARCH')
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

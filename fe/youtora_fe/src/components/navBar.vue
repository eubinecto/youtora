<template>
    <div id="navBar">
<!--        top navigation bar -->
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">Youtora</b-navbar-brand>
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        </b-navbar>


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
                <b-form-select
                        id="input-3"
                        v-model="form.lang"
                        :options="langs"
                        required
                ></b-form-select>
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
            <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>

    </div>
</template>

<script>
    export default {
        name: 'NavBar',
        props: {

        },
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
                    lang: null,
                },
                langs: [{ text: 'Select One', value: null }, 'ko', 'en', 'fr', 'jp'],
                show: true
            }
        },
        watch: {
            perPage: function(val) {
                    //do something when the data changes.
                    if (val) {
                        this.$store.commit('SET_PER_PAGE', val)

                    }
                }
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()

                this.$store.commit('SET_PER_PAGE', this.perPage)
                this.$store.commit('SET_SEARCH_LANGUAGE', this.form.lang)
                this.$store.commit('SET_SEARCH_QUERY', this.form.query)

                this.$store.dispatch('SEARCH_VIDEOS')
            },
            onReset(evt) {
                evt.preventDefault()
                // Reset our form values
                this.form.email = ''
                this.form.name = ''
                this.form.food = null
                this.form.checked = []
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
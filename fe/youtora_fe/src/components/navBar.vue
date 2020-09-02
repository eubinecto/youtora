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
                        v-model="form.perPage"
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
        <b-card class="mt-3" header="Form Data Result">
            <pre class="m-0">{{ form }}</pre>
        </b-card>

    </div>
</template>

<script>
    export default {
        name: 'NavBar',

        data() {
            return {
                optPerPage : [
                    {item: '10', 'name': '10'},
                    {item: '20', 'name': '20'},
                    {item: '30', 'name': '30'},
                ],
                form: {
                    query: '',
                    lang: null,
                    perPage: '10',
                },
                langs: [{ text: 'Select One', value: null }, 'Korean', 'English'],
                show: true
            }
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()
                alert(JSON.stringify(this.form))
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
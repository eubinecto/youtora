<template>
    <div id="navBar">
<!--        top navigation bar -->
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="/home">Youtora</b-navbar-brand>
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item href="/generalSearch">General Search</b-nav-item>
                    <b-nav-item href="/MLGlossarySearch">ML Glossary Search</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
    export default {
        name: 'NavBar',
        props: {

        },

    }
</script>

<style>

</style>
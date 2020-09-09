<template>
    <div id="homeView" class="homeView">
        <main>
            <div class="homeBody">
                <home-body/>
            </div>
        </main>


        <footer class="footer">
            <div class="container">
                <home-footer class="homeFoot"/>
            </div>
        </footer>


    </div>
</template>

<script>
    import homeFooter from "./homeFooter";
    import homeBody from "./homeBody";
    export default {
        name: 'homeView',
        components: {
            homeBody,
            homeFooter
        },
        data() {
            return {

            }
        }
    }
</script>

<style>
    /* Sticky footer styles
    -------------------------------------------------- */
    .footer {
        position: absolute;
        bottom: 0;
        width: 100%;
        /* Set the fixed height of the footer here */
        height: 70px;
        line-height: 30px; /* Vertically center the text there */
        background-color: #f5f5f5;
    }


    /* Custom page CSS
    -------------------------------------------------- */
    /* Not required for template or sticky footer method. */

    body > .container {
        padding: 60px 15px 0;
    }

    .footer > .container {
        margin-top: 5px;
        text-align: left;
        margin-left: 0;
        padding-right: 15px;
        padding-left: 15px;
    }


</style>
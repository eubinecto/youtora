<template>
    <div id="homeView" class="homeView">
        <div class="homeSearchBar">
            <home-body/>
        </div>


        <div class="footMain">
            <div class="container">
                <home-footer class="homeFoot"/>
            </div>
        </div>


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
    .footMain {
        position: absolute;
        bottom: 0;
        width: 100%;
        /* Set the fixed height of the footer here */
        height: 70px;
        line-height: 30px; /* Vertically center the text there */
        padding: 1rem 1rem 5rem;
        background-color: #f5f5f5;
    }


    /* Custom page CSS
    -------------------------------------------------- */
    /* Not required for template or sticky footer method. */
    .homeSearchBar{
        position: fixed;
        width: 600px;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    body > .container {
        padding: 60px 15px 0;
    }

    .footMain > .container {
        margin-top: 5px;
        text-align: left;
        margin-left: 0;
        padding-right: 15px;
        padding-left: 15px;
    }


</style>
<template>
    <div id="mlGlossarySearch">
        <p>
            ML GLOSSARY SEARCH
        </p>
        <HelloWorld/>
        <ml-glossary-search-pagination/>
    </div>
</template>

<script>
import HelloWorld from "../HelloWorld";
import mlGlossarySearchPagination from "./mlGlossarySearchPagination";

    export default {
        name: 'mlGlossarySearch',
        components: {
            HelloWorld,
            mlGlossarySearchPagination
        },
        data() {

        },
    }
</script>
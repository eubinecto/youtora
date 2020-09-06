<template>
    <div id="mlGlossarySearch">
        <p>
            ML GLOSSARY SEARCH
        </p>
        <mlGlossarySearchWordBucket

        />
        <ml-glossary-search-pagination/>
    </div>
</template>

<script>
import mlGlossarySearchWordBucket from "./mlGlossarySearchWordBucket";
import mlGlossarySearchPagination from "./mlGlossarySearchPagination";

    export default {
        name: 'mlGlossarySearch',
        components: {
            mlGlossarySearchWordBucket,
            mlGlossarySearchPagination
        },
        data() {

        },
    }
</script>
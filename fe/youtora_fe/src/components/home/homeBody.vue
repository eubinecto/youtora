<template>
    <section id="homeBody">
        <span>
            <b-field class="searchBox">
                <b-autocomplete size="is-medium"
                                expanded
                                v-model="searchQuery"
                                icon="magnify"
                                :placeholder="$t('searchBar.searchBarPlaceHolder')"
                                @select="option => selected = option"
                                @keyup.enter="onClickSearch"
                />
                <p class="control" v-if="searchQuery">
                    <button @click="onClickClearSearch" class="button  is-medium "><i class="fas fa-times"></i></button>
                </p>
                <br/>
            </b-field>
        </span>
    </section>
</template>

<script>
    export default {
        name: 'homeBody'
    }
</script>

<style>

</style>
<script lang="ts">
    import {Card} from "nunui";
    import Provider from "$lib/Provider.svelte";
    import api from "$utils/api";

    let list = [];
    api('/api/mark').then(r => list = r.list)
</script>

<Provider api="mark" let:api block="12" key>
    {#each list || [] as item}
        <a href="/view/{item.paper}">
            <Card outlined ripple>
                <p style="margin: 0">{item.preview}</p>
            </Card>
        </a>
    {/each}
</Provider>

<style lang="scss">
  a {
    text-decoration: none;
    color: var(--on-surface);
  }
</style>
<script lang="ts">
    import Expand from "$lib/Expand.svelte";

    type Section = {
        title: string;
        top: number;
        children: Section[];
    }

    export let sections: Section[], active: Section[] = [], all = false;

    function scroll(top: number) {
        return () => {
            window.scrollTo({top: top - 60, behavior: 'smooth'})
        }
    }
</script>

{#if sections}
    {#each sections as section}
        <Expand show={active.includes(section) || all}>
            <p class:active={active.includes(section) && all} on:click={scroll(section.top)}>{section.title}</p>
        </Expand>
        <div>
            {#each section.children || [] as child}
                <svelte:self sections={[child]} {active} {all}/>
            {/each}
        </div>
    {/each}
{/if}

<style lang="scss">
  div {
    padding-left: 12px;
  }

  p {
    margin: 0;
    padding: 6px 0;
    cursor: pointer;
  }

  .active {
    color: var(--secondary);
  }
</style>
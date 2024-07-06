<script lang='ts'>
    export let size = 18, line = 1, width, loaded = false, margin = 5, first = false, style = '';
    let hide = loaded;

    $: _line = Math.max(+Math.round(line) || 10, 0);

    $: if (loaded) {
        setTimeout(() => hide = true, 620);
    } else hide = false;
</script>

<main class='container {$$props.class}' style:min-height="{loaded ? 0 : ((+size) + (+margin)) * _line}px" {style}>
    {#if !hide}
        <div class='content preload' class:hide={loaded} style:--sh="{size}px" style:--mg="{margin}px"
             style:--w="{width}%">
            {#if _line}
                {#if width}
                    {#each Array(_line) as _, i}
                        <div class={i || first ? 'skeleton' : 'line'} style:--d="{i / _line * 0.4}s">
                        </div>
                    {/each}
                {:else}
                    {#each Array(_line) as _, i}
                        <div class={i || first ? 'skeleton' : 'line'} style:--d="{i / _line * 0.4}s"
                             style:--w="{(line > 1 ? (i === line - 1 ? 40 : Math.random () * 15 + 85) : 100)}%">
                        </div>
                    {/each}
                {/if}
            {/if}
        </div>
    {/if}
    {#key _line}
        <div class="content" class:hide={!loaded}>
            <slot/>
        </div>
    {/key}
</main>

<style lang='scss'>
  .hide {
    opacity: 0 !important;
  }

  main {
    position: relative;
    display: grid;
    grid-template-columns: 100%;
    width: 100%;
  }

  .preload {
    position: absolute;
    pointer-events: none;
    user-select: none;
  }

  .content {
    transition: opacity 0.6s ease-in-out;
    grid-row-start: 1;
    grid-column-start: 1;
    opacity: 1;
    width: 100%;
  }

  .line {
    width: var(--w);
    height: var(--sh);
    margin-bottom: var(--mg);
    overflow: hidden;
    border-radius: 12px;
  }

  .skeleton {
    background: var(--primary-light1);
    width: var(--w);
    height: var(--sh);
    margin-bottom: var(--mg);
    overflow: hidden;
    border-radius: 12px;
    animation: fade;
    animation-duration: 1s;
    animation-fill-mode: forwards;
    animation-delay: var(--d);
    animation-iteration-count: infinite;
    opacity: 0.2;
  }

  @keyframes fade {
    0% {
      opacity: 0.2;
    }
    20% {
      opacity: 1;
    }
    80% {
      opacity: 1;
    }
    100% {
      opacity: 0.2;
    }
  }
</style>
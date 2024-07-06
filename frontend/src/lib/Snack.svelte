<script lang="ts">
    import {Button, Icon} from "nunui";
    import {getStoreRaw} from "$utils/state";
    import {cubicInOut} from "svelte/easing";
    import {fade} from "svelte/transition";
    import {beforeNavigate} from "$app/navigation";

    const snack = getStoreRaw("snack"), snackStore = snack.store;
    let highlight = false;

    $: ({icon, timestamp, duration, title, message, dismissible, actions, component, scrim, props} = $snackStore);

    $: if (timestamp && dismissible && duration) {
        let _ts = timestamp;
        setTimeout(() => {
            if (_ts === timestamp) snack.del();
        }, duration);
    }

    beforeNavigate(({cancel}) => {
        if (timestamp && !dismissible) {
            highlight = true;
            cancel()
            setTimeout(() => highlight = false, 100);
        }
    });

    function snackbar(node, {duration} = {duration: 800}) {
        return {
            duration,
            css: t => {
                const eased = cubicInOut(t);

                return `
					transform: scale(${eased * 0.2 + 0.8}) translateY(${(eased - 1) * 20}px);
					opacity: ${eased};
				`
            }
        };
    }

    function close() {
        snack.del();
    }
</script>

{#key timestamp}
    {#if timestamp && scrim}
        <div class="scrim" transition:fade|global on:click={() => dismissible && snack.del()}></div>
    {/if}
    {#if highlight}
        <div class="scrim" out:fade on:click={() => dismissible && snack.del()}></div>
    {/if}
    <div class="container">
        {#if timestamp}
            {#key timestamp}
                <main transition:snackbar|global>
                    {#if component}
                        <svelte:component this={component} {close} {...props}/>
                    {:else}
                        <div style="display: flex;">
                            {#if icon}
                                <div style="width: 48px;position: relative;top: 4px;">
                                    <Icon {icon} size="36"/>
                                </div>
                            {/if}
                            <div style="flex: 1;">
                                <h3>{title}</h3>
                                <p>{message}</p>
                                {#if actions}
                                    <br>
                                    <span>
                                    {#each actions as action}
                                        <Button transparent small
                                                on:click={() => (action.handler || close)(close)}>{action.label}</Button>
                                    {/each}
                                </span>
                                {/if}
                            </div>
                        </div>
                    {/if}
                </main>
            {/key}
        {/if}
    </div>
{/key}

<style lang="scss">
  .container {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    pointer-events: none;
    z-index: 200;

    max-height: calc(100vh - 24px);
    overflow: auto;
  }

  main {
    pointer-events: initial;
    background: radial-gradient(circle at 80% 80%, var(--secondary-light5), var(--secondary-light3));
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
    margin: 12px;
    padding: 12px;
    border-radius: 12px;
    position: absolute;
    min-width: 300px;
    max-width: 90vw;
  }

  h3 {
    margin: 10px 0;
    font-size: 1.2rem;
    font-weight: 500;
  }

  p {
    font-size: 1rem;
  }

  .scrim {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background: #000000;
    opacity: 0.8;
    z-index: 199;

    &.hl {
      background: #ffffff;
      opacity: 0.6;
    }
  }

  span {
    float: right;
    margin-top: -10px;

    & > :global(*) {

      margin-left: 8px;
    }
  }
</style>
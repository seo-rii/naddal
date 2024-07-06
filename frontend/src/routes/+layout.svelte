<script lang="ts">
    import {ThemeProvider} from "nunui";
    import {windowWidth, pageScroll, leftNav, navHeight, darkMode} from "$stores/ui";
    import Nav from "$lib/Nav.svelte";
    import {page} from "$app/stores";
    import {fly} from "svelte/transition";


    let primary, secondary, surface, onSurface, onSecondary;
    $: {
        if ($darkMode) {
            [primary, secondary, surface, onSurface, onSecondary] = ["#5256a4", "#464186", "#1e202a", "#fff", "#fff"];
        } else {
            [primary, secondary, surface, onSurface, onSecondary] = ["#2c2963", "#514daf", "#eff2f6", "#13131f", "#13131f"];
        }
    }
</script>

<svelte:head>
    {#if $darkMode}
        <style>
            html, body {
                background: #1e202a;
            }
        </style>
    {:else}
        <style>
            html, body {
                background: #eff2f6;
            }
        </style>
    {/if}
</svelte:head>

<svelte:window bind:innerWidth={$windowWidth} bind:scrollY={$pageScroll}/>
<ThemeProvider {primary} {secondary} {surface} {onSurface} {onSecondary}>
    <Nav/>
    <main class:leftNav={$leftNav} style:padding-top="{$navHeight}px">
        {#key $page.url.toString()}
            <div in:fly={{y: 10}}>
                <slot/>
            </div>
        {/key}
    </main>
</ThemeProvider>

<style lang="scss">
  @import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css");

  :root {
    --nav: 70px;
  }

  main {
    color: var(--on-surface);

    &.leftNav {
      margin-left: var(--nav);

      div {
        padding: 12px;

        & > :global(main) {
          animation: fade 0.5s cubic-bezier(0.4, 0, 0.2, 1);
          padding: 0 12px;
        }
      }
    }
  }

  @keyframes fade {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
    }
  }

  :global(h1) {
    font-weight: 400;
    margin: 0.6em 0 0.3em 0
  }


  :global(html, body, body > div, body > div > main) {
    height: 100%;
    margin: 0;
    padding: 0;
    font: normal 250 16px "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, "Helvetica Neue", "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
    scroll-behavior: smooth;
    color: var(--on-surface);

    transition: background-color 0.3s ease, color 0.3s ease;
  }
</style>
<script lang="ts">
    import text from "./text";
    import {browser} from "$app/environment";
    import Toolbar from "$lib/Toolbar.svelte";
    import {onMount, tick} from "svelte";

    let raw = text, container;
    let result: Section[] = [];

    type Section = {
        title: string;
        top: number;
        children: Section[];
    }

    async function parseSection(container) {
        if (!container) return;
        let current: Section = {title: '', children: [], top: 0};
        let sections = [];

        function traverse(node: HTMLElement) {
            const top = (node?.getBoundingClientRect && node?.getBoundingClientRect()?.top || 0) + window.scrollY;
            if (node.nodeName === 'H1') {
                current = {title: node.textContent.trim(), children: [], top};
                sections.push(current);
            } else if (node.nodeName === 'H2') {
                current.children.push({
                    title: node.textContent.trim(),
                    children: [], top
                });
            } else if (node.nodeName === 'H3') {
                current.children[current.children.length - 1].children.push({
                    title: node.textContent.trim(),
                    children: [], top
                });
            }
            node.childNodes.forEach(traverse);
        }

        await tick();
        container.childNodes.forEach(traverse);
        if (JSON.stringify(sections) !== JSON.stringify(result)) result = sections;
    }

    $: container && parseSection(container);

    onMount(() => {
        const intv = setInterval(() => {
            parseSection(container);
        }, 1000);
        return () => clearInterval(intv);
    })
</script>

<Toolbar sections={result}/>

<main bind:this={container}>
    {@html raw}
</main>

<style lang="scss">
  main {
    :global(h1) {
      position: sticky;
      top: 0;
      background: var(--surface);
      height: 46px;
      z-index: 1;

      font-size: 2em;
      font-weight: 300;
    }

    :global(h2) {
      position: sticky;
      top: 46px;
      background: var(--surface);
      font-size: 1.4em;
      font-weight: 300;
      height: 30px;
      border-bottom: solid 1px var(--primary-light1);
    }

    :global(table) {
      border-collapse: collapse;
    }

    :global(table th), :global(table td) {
      border: solid 1px var(--primary-light1);
      padding: 12px;
    }
  }
</style>
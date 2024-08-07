<script lang="ts">
    import text from "./text";
    import Toolbar from "$lib/Toolbar.svelte";
    import {onMount, tick} from "svelte";
    import TipTap from "@seorii/tiptap"
    // @ts-ignore
    import {v4 as uuid} from "uuid";
    import api from "$utils/api";
    import {Button, Card, IconButton} from "nunui";

    export let data;

    let editable = false;

    let raw = '', _raw = '', container, editor, marks = [];
    let result: Section[] = [], title;

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

    $: parseSection(container);
    let lock = Date.now(), scrollY;

    onMount(() => {
        const intv = setInterval(() => {
            if (lock < Date.now()) parseSection(container);
        }, 1000);
        const intv2 = setInterval(() => {
            const _sel = window.getSelection().toString();
            if (_sel) {
                sel = _sel;
            }
        }, 100)
        api('/api/paper/' + data.id).then((data) => {
            raw = _raw = data.raw;
            window.id = data;
        });
        return () => {
            clearInterval(intv);
            clearInterval(intv2);
        }
    })

    async function update(raw) {
        _raw = raw;
        await tick();
        if (!container) return;
        const _marks = Array.from(container.querySelectorAll('mark')).map(i => {
            const id = uuid();
            return {
                id,
                preview: i.textContent,
                paper: data.id,
            }
        })
        marks = _marks;
        await api('/api/mark/' + data.id, {marks})
        await api('/api/paper/' + data.id, {raw}, 'PATCH')
    }

    $: if (_raw !== raw) {
        update(raw);
    }

    $: {
        let _ = scrollY;
        lock = Date.now() + 100;
    }

    let showTranslation = false, translation = '', sel = null;

    async function translate() {
        showTranslation = true;
        translation = '번역하는 중...'
        translation = (await api('/api/translation', {raw: sel})).raw;
    }

    async function ask() {
        window.ask = sel + '에 대해서 설명해 줘.';
    }

    let cont: HTMLElement;
    $: if (cont) {
        const intv = setInterval(() => {
            const rect = cont && cont.getBoundingClientRect();
            if (!rect || rect.height === 0) {
                clearInterval(intv);
                showTranslation = false;
            }
        })
    }
</script>

<svelte:window bind:scrollY/>
<Toolbar sections={result} bind:editable/>

<main bind:this={container}>
    {#if raw}
        <TipTap bind:body={raw} mark {editable} bubbleOverride={showTranslation}
                sanitize={{allowedTags: [], allowedAttributes: {}}}>
            <svelte:fragment slot="bubble">
                <IconButton icon="translate" size="small" on:click={translate}/>
                <IconButton icon="question_mark" size="small" on:click={ask}/>
            </svelte:fragment>
            <svelte:fragment slot="bubbleOverride">
                <div bind:this={cont} style:min-height="1px"></div>
                <div>
                    <Card primary flat>{sel}</Card>
                    <Card secondary flat>{translation}</Card>
                </div>
                <div>
                    <Button small outlined on:click={() => showTranslation = false}>닫기</Button>
                </div>
            </svelte:fragment>
        </TipTap>
    {/if}
</main>

<style lang="scss">
  main {
    :global(*) {
      max-width: 100%;
    }

    :global(h1 br) {
      display: none;
    }

    :global(h2 br) {
      display: none;
    }

    :global(h1) {
      position: sticky;
      top: 0;
      background: var(--surface);
      height: 46px;
      z-index: 2;

      font-size: 2em;
      font-weight: 300;
    }

    :global(h2) {
      position: sticky;
      top: 46px;
      z-index: 1;
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
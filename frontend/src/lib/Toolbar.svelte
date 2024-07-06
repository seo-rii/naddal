<script lang="ts">
    import Section from "$lib/Section.svelte";
    import {Hoverable, IconButton} from "nunui";

    type Section = {
        title: string;
        top: number;
        children: Section[];
    }

    export let editable;
    export let setting, sections: Section[];
    let scrollY, active = [];

    function getActiveSection(sections: Section[], scrollY: number): Section[] {
        if (sections.length === 0) return [];
        let activeSection = sections[0];
        for (let i = 0; i < sections.length; i++) {
            if (sections[i].top > scrollY + 70) break;
            activeSection = sections[i];
        }
        if (activeSection.children.length > 0) {
            return [activeSection, ...getActiveSection(activeSection.children, scrollY)];
        }
        return [activeSection];
    }

    $: if(sections?.length) active = getActiveSection(sections, scrollY);
</script>

<svelte:window bind:scrollY/>

<main>
    <p style="margin: 0;padding-bottom: 6px;border-bottom: solid 1px var(--primary-light3)">
        <IconButton icon="edit" size="small" on:click={() => editable = !editable} active={editable}/>
    </p>
    <Hoverable let:hovering>
        <Section {sections} {active} all={hovering}/>
    </Hoverable>
</main>

<style lang="scss">
  main {
    position: fixed;
    z-index: 10;
    right: 12px;
    padding: 12px;
    top: 12px;
    width: 200px;
    background: var(--primary-light1);
    border-radius: 12px;

    max-height: calc(100vh - 24px);
    overflow: auto;
  }
</style>

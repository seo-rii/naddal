<script lang="ts">
    import {tweened} from "svelte/motion";
    import {cubicInOut} from "svelte/easing";

    export let x = false, y = !x, style = "", show = true;
    let clientHeight = 0, clientWidth = 0, height = tweened(0, {duration: 300, easing: cubicInOut}),
        width = tweened(0, {duration: 300, easing: cubicInOut});

    $: if (y) height.set(show ? clientHeight : 0);
    $: if (x) width.set(show ? clientWidth : 0);
</script>

<main style="{style};{x ? `width: ${$width}px;` : ''}{y ? `height: ${$height}px;` : ''}">
    <div bind:clientHeight bind:clientWidth class:x class:y>
        <slot/>
    </div>
</main>

<style lang="scss">
  main {
    div {
      position: absolute;

      &.y {
        width: 100%;
      }

      &.x {
        height: 100%;
      }
    }

    overflow: hidden;
    position: relative;
  }
</style>
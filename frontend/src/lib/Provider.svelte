<script lang="ts" context="module">
    import {browser} from '$app/environment';
    import api from "$utils/api";

    const cache: any = {};

    if (browser) {
        window.addEventListener('authRefresh', () => {
            for (const key in cache) {
                delete cache[key];
            }
        });

        window.addEventListener('clear', ({detail}: any) => {
            for (const prefix of detail) {
                for (const key in cache) {
                    if (key.startsWith(prefix)) {
                        delete cache[key];
                    }
                }
            }
        });
    }
</script>

<script lang="ts">
    import {createEventDispatcher, onMount, setContext, tick} from "svelte";
    import {type Writable, writable} from "svelte/store";
    import Skeleton from "$$/Skeleton.svelte";

    export let type: string = Object.keys($$restProps)[0], defaultValue = {};

    const dispatch = createEventDispatcher();
    const object = writable(<any>defaultValue);

    export let id: number = $$restProps[type], postfix = '', url = '', local = true, reload = false, block = false,
        load = true, loaded = false, mounted = false, store: Writable<any> = (<any>object)?.store || object,
        rerender = false;
    let ts = Date.now(), c = 0, getc = () => c, inc = () => ++c;

    setContext(type, object);
    $: key = url || ((id || postfix) ? `/${type}/${id}${postfix}` : `/${type}`);
    $: id = $$restProps[type];

    const clear = (prefix: string) => {
        for (const key in cache) {
            if (key.startsWith(prefix)) {
                delete cache[key];
            }
        }
        ts++;
    }

    $: if (reload) clear(key);

    $: if (browser && key !== undefined && load && mounted) {
        void ts;
        tick().then(async () => {
            inc();
            let _c = getc();
            await tick();
            object.update(o => ({...o, loading: true}));
            await tick();
            if (cache[key]) {
                loaded = false;
                cache[key].then(async (r: any) => {
                    await tick();
                    await tick();
                    r.loaded = true;
                    dispatch('load', r);
                    await tick();
                    await tick();
                    if (_c === getc()) object.set(r);
                    await tick();
                    await tick();
                    loaded = true;
                    if (r.error) {
                        const e = r.error;
                        if ((e.code >= 400 && e.code < 500) || e.code === 503) clear(key);
                    }
                });
            } else {
                loaded = false;
                cache[key] = new Promise(resolve => {
                    api(key).then(async (r: any) => {
                        dispatch('load', r);
                        r.loaded = true;
                        //r._ts = ts;
                        await tick();
                        await tick();
                        if (_c === getc()) object.set(r);
                        await tick();
                        await tick();
                        loaded = true;
                        resolve(r);
                    }).catch(async (error) => {
                        const e = {error};
                        dispatch('load', e);
                        await tick();
                        await tick();
                        if (_c === getc()) object.set(e);
                        await tick();
                        await tick();
                        loaded = true;
                        resolve(e);
                    })
                });
            }
        });
    }

    onMount(() => {
        const refresh = () => tick().then(() => setTimeout(() => ts++, 10));
        tick().then(() => mounted = true);
        window.addEventListener('authRefresh', refresh);
        window.addEventListener('clear', refresh);
        return () => {
            window.removeEventListener('authRefresh', refresh);
            window.removeEventListener('clear', refresh);
        }
    })

    $: data = $store;
</script>


{#if block === false || (block === true && loaded)}
    {#if rerender}
        {#key loaded}
            <slot {data} {...{[type]: data}} {loaded}/>
        {/key}
    {:else}
        <slot {data} {...{[type]: data}} {loaded}/>
    {/if}
{:else}
    <Skeleton line={block} size='38.89' width='100' margin='38.89' first {loaded}>
        {#if loaded}
            <slot {data} {...{[type]: data}} {loaded}/>
        {/if}
    </Skeleton>
{/if}
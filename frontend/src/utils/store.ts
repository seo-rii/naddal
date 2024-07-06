import {writable} from "svelte/store";
import {browser} from "$app/environment";

export function savable(name: string, defaultValue: any = null) {
    const store = writable(browser ? JSON.parse(localStorage[name] || JSON.stringify(defaultValue)) : defaultValue);
    store.subscribe(val => browser && (localStorage[name] = JSON.stringify(val)))
    return store;
}

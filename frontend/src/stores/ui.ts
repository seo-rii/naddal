import {browser} from "$app/environment";
import {derived, writable} from "svelte/store";
import {savable} from "$utils/store";

export const theme = savable('theme', 'auto');
export const darkMode = derived(theme, ($theme: string) => $theme === 'dark' || ($theme === 'auto' && browser && window.matchMedia('(prefers-color-scheme: dark)').matches));

export const windowWidth = writable(0);
export const isMobile = derived([windowWidth], ([$windowWidth]) => $windowWidth < 800);
export const leftNav = derived([isMobile], ([$isMobile]) => !$isMobile);
export const navHeight = derived([leftNav], ([$leftNav]) => $leftNav ? 0 : 60);


export const pageScroll = writable(0);

export const viewerOption = savable('viewerOption', {
    size: 16
})
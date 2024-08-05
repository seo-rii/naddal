import {browser} from "$app/environment";
import {tick} from "svelte";
//@ts-ignore
import {get_current_component} from "svelte/internal";

export const endpoint = import.meta.env.DEV ? 'http://localhost:80' : 'https://api-naddal.seorii.page'

export default function api(path: string, data: any = undefined, method = 'POST'): Promise<any> {
    if (!browser) return new Promise<{ data: any }>(() => null)
    let comp
    try {
        comp = get_current_component()
    } catch (e) {
    }
    if (comp && comp?.$$?.root?.parentElement !== document.body)
        return new Promise(async (resolve, reject) => {
            setTimeout(
                () =>
                    tick()
                        .then(() => api(path, data, method))
                        .then(resolve)
                        .catch(reject),
                10
            )
        })
    return new Promise(async (resolve, reject) => {
        fetch(endpoint + path, {
            method: data ? method : 'GET',
            body: data ? JSON.stringify(data) : undefined,
            redirect: 'follow',
            referrerPolicy: 'no-referrer',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => res.json()).then((res) => {
            if (import.meta.env.DEV) {
                if (!path.startsWith('/gets')) console.log('API Request', path, res)
                else console.log('API Requests', JSON.parse(decodeURIComponent(atob(path.split('=')[1]))), res)
            }
            if (!res.error) resolve(res.data)
            else reject({
                ...res,
                toString: () => `APIError(${res.code}): ${res.error}${res.trace ? '\n' + res.trace : ''}`
            })
        }).catch(reject)
    })
}

export function refresh(...detail: any[]) {
    const refresh = new CustomEvent('clear', {detail});
    window.dispatchEvent(refresh);
}
import {writable, get, type Writable} from "svelte/store";
import {tweened} from "svelte/motion";
import {getContext, setContext} from "svelte";
import {browser} from "$app/environment";

export interface GlobalStorage<T = any> {
    store: Writable<T>;
    size: () => number;
    set: (value: T, upd?: boolean) => void;
    get: () => T;
    update: (fn: (value: T) => T) => void;
    del: (id?: number, delay?: number) => void;
    create: (value?: T) => T;
    initList: () => Writable<T[]>;
    activate: (id: number) => void;
    findIndex: (f: (value: T) => boolean) => number;
    clear: (delay?: number) => void;
}

function getStoList(list: any, last?: boolean) {
    list = Array.from(list);
    if (list.length === 0) return null;
    if (last) return list[list.length - 1];
    return list[0];
}

export function global(name: string, defaultValue: any = null, tweenOptions: any = null, last = false): GlobalStorage {
    let cnt = 0, listStore: Writable<any[]> | null = null, rc: any = {};
    const store = tweenOptions ? tweened(defaultValue, tweenOptions) : writable(defaultValue as any),
        data = new Map(),
        storage = {
            data,
            store,
            listStore,
            size() {
                return data.size;
            },
            set(id: number, value: any, upd = true) {
                if (!data.has(id)) return;
                data.set(id, value);
                if (upd) store.set(getStoList(data.values(), last) || defaultValue);
                listStore?.set?.(Array.from(data.values()));
            },
            get(id?: number) {
                if (!data.size) return defaultValue;
                if (id === undefined) id = getStoList(data.keys(), last);
                return data.get(id);
            },
            update(fn: (value: any) => any, id = getStoList(data.keys(), last)) {
                if (!data.size) return;
                if (!data.has(id)) return;
                storage.set(id, fn(data.get(id)));
            },
            async del(id?: number, delay = 0) {
                if (id === undefined) id = getStoList(data.keys(), last);
                rc[id] = (rc[id] || 0) - 1;
                await new Promise(r => setTimeout(r, 0));
                if (rc[id] > 0) return;
                if (delay === -1) {
                    data.delete(id);
                    store.set(getStoList(data.values(), last) || defaultValue);
                    listStore?.set?.(Array.from(data.values()));
                } else setTimeout(() => {
                    let l = data.delete(id);
                    store.set(getStoList(data.values(), last) || defaultValue);
                    listStore?.set?.(Array.from(data.values()));
                }, delay);
            },
            create(value: any = defaultValue, activate = false, _id = undefined) {
                if (_id) {
                    const tid = storage.findIndex((v: any) => v?.id === _id);
                    if (tid !== -1) {
                        setTimeout(() => storage.activate(tid), 100);
                        const tv = data.get(tid);
                        rc[tid] = (rc[tid] || 0) + 1;
                        if (tv) return {
                            id: tid,
                            store,
                            set: (value: any, upd = true) => storage.set(tid, value, upd),
                            del: (delay = 200) => storage.del(tid, delay),
                            update: (fn: (value: any) => any) => storage.update(fn, tid),
                        }
                    }
                }
                const id = cnt++;
                rc[id] = (rc[id] || 0) + 1;
                data.set(id, value || defaultValue);
                store.set(getStoList(data.values(), last) || defaultValue);
                listStore?.set?.(Array.from(data.values()));
                return {
                    id,
                    store,
                    set: (value: any, upd = true) => storage.set(id, value, upd),
                    del: (delay = 200) => storage.del(id, delay),
                    update: (fn: (value: any) => any) => storage.update(fn, id),
                };
            },
            clear(delay?: number) {
                data.clear();
                setTimeout(() => !Array.from(data.keys()).length && store.set(defaultValue), delay);
                listStore?.set?.(Array.from(data.values()));
            },
            initList() {
                if (listStore) return listStore;
                listStore = writable(Array.from(data.values()));
                return listStore;
            },
            activate(id: number) {
                if (!data.has(id)) return;
                store.set(data.get(id));
            },
            findIndex(f: any) {
                for (const i of data.keys()) if (f(data.get(i))) return i;
                return -1;
            }
        }
    setContext(name, storage);
    return storage;
}

export function newSetting<T>(name: string, settingPromise: Promise<T> | undefined | null = undefined, defaultSetting: T = <T>{}, sync: ((setting: T) => any) | undefined = undefined) {
    let store = writable(defaultSetting), loaded = writable(false), _loaded = false, once = false;
    store.subscribe((setting) => {
        if (_loaded) {
            loaded.set(true);
            if (once) sync?.(setting);
            once = true;
        }
    });

    const _get = (field?: string) => () => {
        if (field) return (<any>get(store))[field];
        return get(store);
    };

    const upd = (field: string, value: any) => () => {
        store.set({
            ...get(store),
            [field]: value
        });
    }

    const delta = (field: string, value: any, def: any) => () => {
        store.set({
            ...get(store),
            [field]: +(((<any>get(store))?.[field] || def) + value).toFixed(2)
        });
    }

    const handle = (field: string, cb: (value: any) => any) => {
        let last: any = undefined;
        store.subscribe((setting: any) => {
            if (!setting) return;
            const val = field ? setting?.[field] : setting;
            if (!field || last !== val) {
                cb(val);
                last = val;
            }
        });
    }

    setTimeout(() => {
        if (settingPromise) settingPromise.then((setting) => {
            for (const i in defaultSetting) {
                if (setting[i] === undefined) setting[i] = defaultSetting[i];
            }
            _loaded = true;
            store.set(setting);
        }).catch(_ => _);
    });

    const res = {...store, get: _get, loaded, upd, delta, handle};
    setContext(name, res);
    return res;
}

export function getSetting<T = any>(name: string) {
    return getContext<T>(name);
}

export function getList<T = any>(name: string) {
    return (<GlobalStorage>getContext<T>(name))?.initList?.()
}

export function getStore<T = any>(name: string) {
    return (<GlobalStorage>getContext<T>(name))?.store || getContext<T>(name)
}

export function getStoreRaw<T = any>(name: string) {
    return (<GlobalStorage>getContext<T>(name))
}

export const newStore = (name: string, value: any = null, activate = false, id = undefined) => <GlobalStorage>(<any>getContext(name)).create(value, activate, id);

export function savable(name: string, defaultValue: any = null) {
    let value = defaultValue;
    try {
        value = browser ? JSON.parse(localStorage[name] || JSON.stringify(defaultValue)) : defaultValue;
    } catch (e) {
    }
    const store = writable(value);
    store.subscribe(val => browser && (localStorage[name] = JSON.stringify(val)))
    return store;
}
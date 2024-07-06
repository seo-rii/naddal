interface SnackOption {
    icon?: string;
    title?: string;
    message?: string;
    duration?: number;
    dismissible?: boolean;
    component?: any;
    actions?: any[];
    scrim?: boolean;
    props?: any;
}

let lastTs = 0;

export default async function newSnack(snack: SnackOption, force = true) {
    while (1) {
        if (window.snack) break;
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    lastTs = Date.now();
    if (force) {
        while (window.snack.size()) {
            if (window.snack.get().dismissible) window.snack.del(undefined, -1);
            await new Promise(resolve => setTimeout(resolve, Math.max(810 - Date.now() + lastTs, 50)));
            lastTs = Date.now();
        }
    }
    if (snack.dismissible === undefined) snack.dismissible = true;
    if (snack.scrim === undefined) snack.scrim = !snack.dismissible;
    const {id} = window.snack.create(Object.assign({
        icon: '',
        title: '',
        message: '',
        duration: snack.dismissible ? 3000 : 0,
        dismissible: true,
        timestamp: Date.now(),
        scrim: false,
        props: {}
    }, snack));
    return () => window.snack.del(id);
}

export function ask(title: string, message: string = '이 작업은 되돌릴 수 없어요.', action = '삭제', icon = 'live_help') {
    const ret = new Promise<void>((resolve, reject) => {
        newSnack({
            dismissible: false,
            title, message,
            icon,
            actions: [
                {
                    label: action,
                    handler: async () => {
                        resolve();
                        window.snack.del();
                    }
                },
                {
                    label: '취소', handler: () => {
                        reject();
                        window.snack.del();
                    }
                },
            ]
        }, true);
    });
    ret.cancel = (i) => {
        i?.(() => window.snack.del());
        return ret;
    }
    return ret;
}
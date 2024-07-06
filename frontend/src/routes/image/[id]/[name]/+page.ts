import {redirect} from "@sveltejs/kit";
import {endpoint} from "$utils/api";

export function load({url: {pathname}}: any) {
    redirect(302, endpoint + pathname);
}
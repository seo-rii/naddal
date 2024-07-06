<script lang="ts">
    import {page, navigating} from '$app/stores';
    import {leftNav, navHeight, theme} from '$stores/ui';
    import {fade} from 'svelte/transition';
    import {IconButton, List, OneLine, CircularProgress, Icon} from 'nunui';
    import {browser} from '$app/environment';

    $: links = [
        {
            icon: 'home',
            text: '메인',
            path: '/'
        },
        {
            icon: {auto: 'autopay', light: 'light_mode', dark: 'dark_mode'}[$theme],
            text: {auto: '자동 테마', light: '밝은 테마', dark: '다크 테마'}[$theme],
            handler: () => {
                $theme = {auto: 'light', light: 'dark', dark: 'auto'}[$theme];
            },
            separate: true,
        }
    ];

    let expandable,
        expand = false,
        over = null,
        _over = null,
        _exp = false,
        open = false,
        anim = false;
    let overI = -1,
        _overI = -1;

    $: {
        if (overI !== -1) over = links[overI];
        else over = null;
    }

    $: {
        if (_overI !== -1) _over = links[_overI];
        else _over = null;
    }

    $: {
        void $navigating;
        expand = expandable = false;
        _overI = -1;
        open = false;
    }

    $: if (!expandable) _overI = -1;

    $: {
        _exp = expandable;
        if (!_over) _exp = false;

        if (_exp) setTimeout(() => (expand = _exp), 600);
        else setTimeout(() => (expand = _exp), 200);
    }

    $: {
        if (_over) overI = _overI;
        else setTimeout(() => (overI = _overI), 500);
    }

    $: {
        if ($leftNav) setTimeout(() => (anim = true), 200);
        else anim = false;
    }

    $: if (!$leftNav) expand = true;
</script>

<nav
        class:leftNav={$leftNav}
        class:topNav={!$leftNav}
        style:--height={$navHeight + 'px'}
        class:expand={expand && over?.extra}
        class:anim
        style:--nav={$leftNav ? '70px' : '260px'}
        on:mouseenter={() => (expandable = true)}
        on:mouseleave={() => ((expandable = false), (_overI = overI = -1))}
>
    <div class="menu">
        {#if !$leftNav}
            <IconButton icon="menu" on:click={() => (open = true)}/>
        {/if}
        <a class="logo" href="/" on:mouseenter={() => (_overI = -1)}><Icon icon="fluorescent" size="32"/></a>
        {#if $leftNav}
            {#each links as link, i}
                <a
                        class:separate={link.separate}
                        href={link.path}
                        on:click={(e) => {
						if (link.handler) {
							e.preventDefault();
							link.handler();
						}
					}}
                >
                    <IconButton
                            flat
                            icon={link.icon}
                            label={link.text}
                            on:mouseenter={() => (_overI = i)}
                            active={_over === link ||
							$page.url.pathname === link.path ||
							$page.url.pathname.startsWith(link.path + '/')}
                    />
                </a>
            {/each}
        {/if}
        {#if !$leftNav}
            <div style="width: 20px;margin-right: 10px;">
                {#if !browser || $navigating}
                    <div transition:fade={{ duration: 300 }}>
                        <CircularProgress indeterminate size="20"/>
                    </div>
                {/if}
            </div>
        {/if}
    </div>
    <div class="scrim" class:open on:click={() => (open = false)}></div>
    <div class="side" class:open>
        <div class="close">
            <IconButton icon="menu_open" on:click={() => (open = false)}/>
        </div>
        <List>
            {#each links as link}
                {@const {path, handler, text, icon, active} = link}
                <a
                        href={path}
                        on:click={(e) => {
						if (handler) {
							e.preventDefault();
							handler();
						}
					}}
                >
                    <OneLine
                            title={text}
                            {icon}
                            round
                            active={active ||
							_over === link ||
							$page.url.pathname === path ||
							$page.url.pathname.startsWith(path + '/')}
                    />
                </a>
            {/each}
        </List>
    </div>
    <div class="divider"></div>
    {#if over && over.extra}
        <div class="extra" in:fade={{ duration: 300 }}>
            <List>
                {#each over.extra as {text, icon, path, handler, active}}
                    <a
                            href={path}
                            on:click={(e) => {
							if (handler) {
								e.preventDefault();
								handler();
							}
						}}
                    >
                        <OneLine
                                title={text}
                                {icon}
                                round
                                active={active ||
								$page.url.pathname === path ||
								$page.url.pathname.startsWith(path + '/')}
                        />
                    </a>
                {/each}
            </List>
        </div>
    {/if}
</nav>

<style lang="scss">
  .separate {
    margin-top: auto !important;
    margin-bottom: 15px;
  }

  nav {
    position: fixed;
    background: var(--primary-light2);
    color: var(--on-surface);
    z-index: 101;

    &.leftNav .menu {
      padding-left: 4px;
      width: calc(var(--nav) - 4px);
      overflow-y: scroll;

      &::-webkit-scrollbar {
        width: 4px;
      }

      &::-webkit-scrollbar-track {
        background: var(--primary-light2);
      }

      &::-webkit-scrollbar-thumb {
        background: var(--primary-light2);
        transition: all 0.2s ease;
      }

      &:hover {
        &::-webkit-scrollbar-thumb {
          background: var(--primary);
          transition: all 0.2s ease;
        }
      }
    }

    .menu {
      background: var(--primary-light2);
      display: flex;
      align-items: center;
      width: var(--nav);
      height: 100%;
      z-index: 101;
      position: absolute;
      transition: all 0.3s ease-in-out;
    }

    .logo {
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    &.anim {
      transition: all 0.3s ease-in-out;
    }

    &.leftNav {
      overflow: hidden;

      .side,
      .scrim {
        display: none;
      }

      .menu {
        flex-direction: column;
      }

      height: 100%;
      width: var(--nav);

      .menu > :global(*) {
        margin-top: 15px;
      }

      .logo {
        height: unset;
        width: 100%;
      }

      &.expand {
        width: 320px;
        border-radius: 0 12px 12px 0;

        .divider {
          opacity: 1;
        }
      }

      .divider {
        position: absolute;
        left: var(--nav);
        top: 0;
        height: 100%;
        width: 1px;
        background: var(--primary-light4);
        opacity: 0;
        transition: all 0.3s ease-in-out;
      }

      .extra {
        position: absolute;
        right: 0;
        top: 0;
        height: calc(100% - 20px);
        width: 220px;
        transition: all 0.3s ease-in-out;
        padding: 10px;
        z-index: 100;
      }
    }

    &.topNav {
      .scrim {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.2);
        z-index: 101;
        opacity: 0;
        pointer-events: none;
        transition: all 0.3s ease-in-out;

        &.open {
          opacity: 1;
          pointer-events: all;
        }
      }

      .side {
        --width: 300px;
        position: fixed;
        width: calc(var(--nav) - 20px);
        left: calc(-1 * var(--nav));
        top: 0;
        height: 100%;
        background-color: var(--primary-light2);
        border-radius: 0 12px 12px 0;
        transition: all 0.3s ease-in-out;
        font-size: 18px;
        z-index: 102;
        padding: 10px;

        &.open {
          left: 0;
        }

        .close {
          margin: 0 0 10px 10px;
        }
      }

      .menu {
        flex-direction: row;
        justify-content: space-between;
        height: var(--height);
        width: calc(100% - 20px);
        padding: 0 10px;
      }

      width: 100%;
    }

    a {
      text-decoration: none;
      color: var(--on-surface);
    }
  }
</style>
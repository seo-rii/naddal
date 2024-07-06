<script lang="ts">
    import {Button, CircularProgress, Icon, Input} from "nunui";
    import Expand from "$lib/Expand.svelte";
    import {onMount, tick} from "svelte";
    import api from "$utils/api";
    import {browser} from "$app/environment";

    async function getAnswer(question: string): Promise<string> {
        return (await api('/api/chat', {
            refer: [],
            body: question,
        })) || '답변이 없어요.';
    }

    function ask() {
        if (!value) return;
        let ask = value;
        value = '';
        showHistory = true;
        const arr = [ask];
        history = [...history, arr];
        scrollToBottom();
        getAnswer(ask).then(answer => {
            arr[1] = answer;
            history = [...history];
            scrollToBottom();
        });
    }

    async function scrollToBottom() {
        await tick();
        await new Promise(resolve => setTimeout(resolve, 10));
        if (!container) return;
        container.scrollTop = container.scrollHeight;
    }

    let focus = false, value = '', showHistory = false, container: HTMLElement;
    let history = [];
    let clientHeight;

    $: {
        let _ = [showHistory];
        scrollToBottom();
    }

    if (browser) onMount(() => {
        const intv = setInterval(() => {
            if (window.ask) {
                value = window.ask;
                window.ask = '';
                ask();
            }
        }, 100);
    })
</script>

<div style:height="{clientHeight + 12}px"></div>
<main bind:clientHeight>
    <Expand>
        {#if true}
            <div class="row" style="padding-bottom: 0">
                <div style="width: 24px"></div>
                <Button small outlined>전체 파일 참고</Button>
                <Button small outlined={!showHistory} on:click={() => showHistory = !showHistory} icon="history">대화 내역
                </Button>
            </div>
        {/if}
    </Expand>
    <Expand>
        {#if showHistory}
            <div class="container" bind:this={container}>
                {#each history as [q, a]}
                    <div class="row">
                        <div style="width: 24px"></div>
                        <div style="width: 100%">
                            <div class="question">{q}</div>
                            <div class="answer">
                                <div style="margin-bottom: 12px">
                                    <Icon auto_awesome/>
                                </div>
                                {#if a}
                                    {@const lines = a.split('[Output end]').map(i => i.split('참고문헌:')).flat().map(i => i.trim()).filter(i => i.length > 0)}
                                    {#each lines as line, i}
                                        <p>{line}</p>
                                        {#if i < lines.length - 1}
                                            <hr>
                                        {/if}
                                    {/each}
                                {:else}
                                    <CircularProgress indeterminate size="24"/>
                                {/if}
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </Expand>
    <div class="row">
        <Icon auto_awesome style="margin-right: 12px"/>
        <div class="input">
            <Input plain round fullWidth placeholder="아무거나 물어보세요!" trailingIcon="input" on:focus={() => focus = true}
                   on:blur={() => setTimeout(() => focus = false, 10)} bind:value on:submit={ask}
                   trailingHandler={ask}/>
        </div>
    </div>
</main>

<style lang="scss">
  main {
    position: fixed;
    bottom: 0;
    left: var(--nav);
    width: calc(100vw - var(--nav) - 48px);
    margin: 24px;
    background: var(--primary-light1);
    border-radius: 36px;
    z-index: 20;

    display: flex;
    flex-direction: column;
  }

  .input {
    flex: 1;
    border-radius: 100px;
    background: var(--primary-light2);
  }

  .row {
    display: flex;
    align-items: center;
    padding: 12px;
    width: calc(100% - 24px);

    & > :global(*) {
      margin-right: 12px !important;
    }
  }

  .question {
    background: var(--secondary-light2);
    margin-left: auto;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 12px;
    width: fit-content;
  }

  .answer {
    background: var(--secondary-light4);
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 12px;
    width: fit-content;
  }

  .container {
    overflow-y: auto;
    max-height: 50vh;
    scroll-behavior: smooth;
  }

  hr {
    border: none;
    border-top: solid 1px var(--secondary-light3);
    margin: 12px 0;
  }
</style>
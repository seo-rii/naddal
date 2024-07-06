<script>
    import {Button, Card} from "nunui";
    import Provider from "$lib/Provider.svelte";
    import {selectFile} from "$utils/file";
    import newSnack from "$utils/snack";
    import {refresh} from "$utils/api";

    async function upload() {
        const {name, blob} = await selectFile();
        const base64 = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
        const close = await newSnack({
            icon: 'cloud_upload',
            title: '파일 업로드 중...',
            message: '잠시만 기다리세요.',
            dismissible: false,
            scrim: true,
        })

        await api('/api/paper', {
            file_name: name,
            file_data: base64.split(',')[1]
        })
        close();

        newSnack({
            icon: 'cloud_done',
            title: '파일 업로드 완료',
            message: '파일이 성공적으로 업로드되었습니다.',
            timeout: 3000,
        });
        refresh('/api')
    }
</script>

<title>낮달</title>
<main>
    <h1>환영합니다!</h1>

    <div class="row">
        <Button small outlined icon="attach_file" on:click={upload}>파일 업로드</Button>
        <Button small outlined icon="public">arxiv에서 가져오기</Button>
    </div>

    <br>
    <h1>최근 논문</h1>
    <Provider api="paper" let:data block="12">
        <div class="list">
            {#each data.list || [] as item}
                <a href="/view/{item.id}">
                    <Card outlined ripple>
                        <p style="margin: 0">{item.title}</p>
                    </Card>
                </a>
            {/each}
        </div>
    </Provider>
</main>

<style lang="scss">
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
  }

  .list {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
  }

  a {
    text-decoration: none;
    color: initial;
  }

  p {
    margin: 0 0 4px 0;
  }
</style>
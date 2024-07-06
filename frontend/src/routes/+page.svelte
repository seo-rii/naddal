<script>
    import ChatBox from "$lib/ChatBox.svelte";
    import {Button} from "nunui";
</script>

<main>
    <h1>환영합니다!</h1>

    <div class="row">
        <Button small outlined icon="attach_file">파일 업로드</Button>
        <Button small outlined icon="public">arxiv에서 가져오기</Button>
    </div>

    <a href="/view/abc">test</a>
</main>

<style lang="scss">
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
  }
</style>
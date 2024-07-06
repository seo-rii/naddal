<script lang="ts">
    import {Icon, Input} from "nunui";
</script>

<main>
    <div class="row">
        <Icon auto_awesome style="margin-right: 12px"/>
        <div class="input">
            <Input plain round fullWidth placeholder="아무거나 물어보세요!" trailingIcon="input"/>
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
    background: var(--primary-light3);
    border-radius: 100px;

    display: flex;
    flex-direction: column;
  }

  .input {
    flex: 1;
    border-radius: 100px;
    background: var(--primary-light1);
  }

  .row {
    display: flex;
    align-items: center;
    padding: 12px;
    width: calc(100% - 24px);
  }
</style>
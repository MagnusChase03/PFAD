<script >
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import Button from './components/Button.vue'
import FileUpload from './components/FileUpload.vue'
import Form from './components/Form.vue'
import LineGraph from './components/LineGraph.vue'
import ModelGetForm from './components/ModelGetForm.vue'
import { defineComponent } from 'vue'
import { darkTheme, NConfigProvider,NText } from 'naive-ui'

  export default defineComponent({
    setup() {
      return {
        darkTheme
      }
    },
    components: {
    NConfigProvider,
    FileUpload,
    NText,
    Form,
    ModelGetForm,
    LineGraph
  }
  })
</script>

<template>
  <n-config-provider :theme="darkTheme">
    <!-- <App /> -->
     <div>
        <header>
          <h1><NText>Upload CSV</NText></h1>
        </header>
        <FileUpload/>
     </div>
    <div>
      <header>
      <h1>Or enter current data...</h1>
      </header>
      <Form/>
    </div>
    <div>
      <header>
        <h1>Get Model</h1>
      </header>
      <ModelGetForm/>
    </div>
  </n-config-provider>
    <LineGraph class="graph"/>

  <!-- <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView /> -->

</template>

<style scoped>
.graph
{
  background-color: white;
  padding: 10px;
  border-radius: 3px;
}
/* header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
} */
</style>

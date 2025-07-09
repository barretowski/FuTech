<template>
    <div class="consulta-jogador">
      <h2>Consulta de Estatísticas do Jogador</h2>
  
      <label for="liga-select">Selecione a Liga:</label>
      <select id="liga-select" v-model="ligaSelecionada">
        <option value="">-- Escolha uma liga --</option>
        <option v-for="liga in ligas" :key="liga.id" :value="liga.id">
          {{ liga.nome }}
        </option>
      </select>
  
      <label for="input-jogador">Nome do Jogador:</label>
      <input
        id="input-jogador"
        v-model="nomeJogador"
        type="text"
        placeholder="Digite o nome do jogador"
      />
  
      <button @click="buscarEstatisticas" :disabled="!ligaSelecionada || !nomeJogador">
        Buscar
      </button>
  
      <div v-if="carregando">Carregando...</div>
  
      <div v-if="erro" class="erro">{{ erro }}</div>
  
      <div v-if="dadosJogador">
        <h3>Resultados para {{ dadosJogador.jogador }}</h3>
        <p><strong>Time:</strong> {{ dadosJogador.time }}</p>
        <p><strong>Campeonato:</strong> {{ dadosJogador.campeonato }} ({{ dadosJogador.temporada }})</p>
        <p><strong>Média de Faltas:</strong> {{ dadosJogador.media_faltas.toFixed(2) }}</p>
        <p><strong>Média de Desarmes:</strong> {{ dadosJogador.media_desarmes.toFixed(2) }}</p>
        <p><strong>Média de Chutes:</strong> {{ dadosJogador.media_chutes.toFixed(2) }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  const ligas = ref([]);
  const ligaSelecionada = ref("");
  const nomeJogador = ref("");
  const dadosJogador = ref(null);
  const carregando = ref(false);
  const erro = ref(null);
  
  async function carregarLigas() {
    try {
      const res = await fetch("http://localhost:8000/ligas");
      ligas.value = await res.json();
    } catch {
      erro.value = "Erro ao carregar ligas.";
    }
  }
  
  async function buscarEstatisticas() {
    erro.value = null;
    dadosJogador.value = null;
    carregando.value = true;
  
    try {
      const url = new URL("http://localhost:8000/jogador");
      url.searchParams.append("jogador", nomeJogador.value);
      url.searchParams.append("liga", ligaSelecionada.value);
      url.searchParams.append("temporada", "2023");
  
      const res = await fetch(url.toString());
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erro na busca.");
      }
  
      dadosJogador.value = await res.json();
    } catch (e) {
      erro.value = e.message;
    } finally {
      carregando.value = false;
    }
  }
  
  onMounted(() => {
    carregarLigas();
  });
  </script>
  
  <style scoped>
  .consulta-jogador {
    max-width: 600px;
    margin: auto;
    font-family: Arial, sans-serif;
  }
  label {
    display: block;
    margin-top: 1em;
  }
  select,
  input {
    padding: 0.5em;
    margin-top: 0.5em;
    width: 100%;
  }
  button {
    margin-top: 1em;
    padding: 0.6em 1em;
  }
  .erro {
    color: red;
    margin-top: 1em;
  }
  </style>
  
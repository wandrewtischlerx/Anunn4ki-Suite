

<img src="https://raw.githubusercontent.com/wandrewtischlerx/Anunn4ki-Suite/main/anunn4ki.PNG" alt="Anunn4ki-Suite">


<h1>Annun4ki Suite v0.3</h1>

---

Anunn4ki Suite é uma ferramenta avançada desenvolvida por Wandrew Tischler, projetada para realizar uma varredura de portas abertas e identificar a presença de serviços específicos usando IPs aleatórios de ranges pré-definidas. O software emprega uma interface colorida que destaca os resultados para uma visualização clara e imediata. Aproveitando a capacidade de múltiplas threads, o Anunn4ki Suite garante um desempenho otimizado ao executar suas tarefas de verificação simultaneamente. Ele realiza testes de conexão de forma eficaz, avaliando a disponibilidade de portas e a presença de serviços, proporcionando assim uma análise abrangente e eficiente das redes monitoradas.

O Anunn4ki Suite é especialmente projetado para identificar portas e serviços específicos que possam ser alvos de testes de segurança, como vulnerabilidades de 0day ou exploits conhecidos. O software permite que os usuários configurem e especifiquem serviços de interesse, facilitando a detecção de redes que podem ser exploradas em avaliações de segurança. Essa capacidade é essencial para realizar testes de determinados metodos.
<h2>Instalação:</h2>

```
git clone https://github.com/wandrewtischlerx/Anunn4ki-Suite
cd Anunn4ki-Suite
pip install -r requirements.txt
```

<h2>Funções</h2>

1. Buscar Apenas Portas Abertas
Esta opção testa se uma porta específica está aberta em múltiplos IPs gerados aleatoriamente. Se a porta estiver aberta, o script coleta e exibe o banner do serviço (se disponível) associado a essa porta.

2. Buscar Serviços e Suas Versões
Esta opção verifica se um serviço específico está rodando em uma porta definida para múltiplos IPs gerados aleatoriamente. Se o serviço estiver encontrado, o script identifica e exibe o banner, incluindo a versão do serviço se for fornecida, mostrando apenas os banners que correspondem à versão especificada.

<h2>Contribuições:</h2>

Contribuições são bem-vindas! Para sugerir melhorias ou reportar problemas, por favor abra uma issue ou envie um pull request.

<h2>Licença:</h2>

Este projeto está licenciado sob a MIT License (https://opensource.org/licenses/MIT).

---

Aproveite o Anunn4ki Suite para detectar portas abertas e identificar serviços específicos com precisão. Otimize suas análises de rede e aumente a eficiência dos seus testes de segurança com esta ferramenta avançada!

Desenvolvido por Wandrew Tischler

HTML para MP4

Cole o código HTML de uma animação, escolha a duração e baixe o vídeo em MP4.

O programa abre o HTML num navegador invisível (Chromium), grava a tela pelo tempo que você escolher e converte a gravação para MP4.

O que tem na pasta
Arquivo	Para que serve
app.py	O programa principal, com a tela de colar o HTML
render_cli.py	Converte um arquivo HTML pela linha de comando (usado pelo GitHub Actions)
animacao.html	Animação de exemplo para testar
requirements.txt	Lista das bibliotecas Python necessárias
.devcontainer/	Configuração para o GitHub Codespaces
.github/workflows/	Configuração para o GitHub Actions
Como usar no GitHub Codespaces
Primeira vez
No repositório, clique em Code, na aba Codespaces, e em Create codespace on main.
No terminal que aparece embaixo, rode os comandos abaixo, um de cada vez:
cd html2mp4
pip install -r requirements.txt
playwright install --with-deps chromium

O último comando demora um pouco, porque baixa o navegador usado para gravar.

Ligue o programa:
python app.py
Abra a tela do programa. Se aparecer um aviso com o botão Abrir no navegador, clique nele. Se não aparecer, vá na aba Portas (ao lado de Terminal), procure a porta 5000 e clique no ícone de globo.
Gerando um vídeo
Cole o código HTML na caixa.
Escolha a duração em segundos e o tamanho do vídeo.
Clique em Gerar MP4 e espere. A gravação leva um pouco mais que a duração escolhida.
Quando o vídeo aparecer, confira a prévia e clique em Baixar MP4.
Nas próximas vezes

A instalação já foi feita, então só precisa:

cd html2mp4
python app.py
Reiniciar ou parar o programa
Parar: clique no terminal e aperte Ctrl+C.
Reiniciar: pare e rode python app.py de novo. Depois aperte F5 na página do programa.
Erro "Address already in use": o programa antigo ainda está rodando. Rode pkill -f app.py e depois python app.py.
Terminal travado: feche-o pela lixeira, abra outro com o + e rode cd html2mp4 e python app.py.
Cuidados com a cota

O GitHub dá um número limitado de horas gratuitas de Codespaces por mês. Quando terminar de usar, pare o codespace (menu do Codespaces, Stop current codespace). Ele também pausa sozinho depois de cerca de 30 minutos sem uso. Para ver quanto já gastou, acesse github.com/settings/billing.

Como usar no GitHub Actions

Esta opção não tem a caixa de colar. Você coloca o HTML num arquivo do repositório e o GitHub gera o vídeo.

Coloque o seu HTML na raiz do repositório, por exemplo minha-animacao.html.
Vá na aba Actions, escolha HTML para MP4 e clique em Run workflow.
Preencha o nome do arquivo, a duração e o tamanho, e confirme.
Quando terminar, abra a execução e baixe o animacao-mp4 na seção Artifacts. Ele vem dentro de um zip com o MP4.
Como usar no seu computador

Precisa de Python 3.9 ou mais novo.

pip install -r requirements.txt
playwright install chromium
python app.py

Depois abra http://localhost:5000 no navegador.

Limites e dicas
Duração máxima: 120 segundos por vídeo. Para aumentar, abra o app.py, troque o número em MAX_DURATION = 120 e também o max="120" do campo de duração na tela. Depois reinicie o programa.
Você define a duração. O programa não descobre sozinho quando a animação termina. Escolha um tempo que cubra a animação inteira.
Quadros por segundo: a gravação sai em 25 quadros por segundo. Fica bom para a maioria das animações, mas movimentos muito rápidos podem parecer menos fluidos.
Sem som. O vídeo sai sem áudio.
Internet: fontes e imagens que vêm da internet carregam normalmente, mas o computador ou o codespace precisa estar online.
Não feche a aba enquanto o vídeo estiver sendo gravado, principalmente nos vídeos mais longos.
Animações que começam com um clique (por exemplo, esperando o usuário apertar um botão) não funcionam, porque ninguém clica durante a gravação. A animação precisa começar sozinha ao abrir a página.
Problemas comuns
Problema	O que fazer
command not found: playwright	Rode pip install -r requirements.txt de novo, dentro da pasta html2mp4
Erro dizendo que falta o navegador (Executable doesn't exist)	Rode playwright install --with-deps chromium
A porta 5000 não aparece em Portas	Pare com Ctrl+C e rode HOST=0.0.0.0 python app.py
-------------------------------------------------------------
# 🎬 Animador HTML → MP4

Cole o código HTML de uma animação, escolha a duração e baixe o vídeo em **MP4**.

[![Abrir no GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/SEU_USUARIO/Animador_HTML)

> Troque `SEU_USUARIO` no link acima pelo seu nome de usuário do GitHub. Depois disso, o botão abre o projeto direto no Codespaces.

---

## ⚡ Início rápido

No terminal do Codespaces, copie e cole **tudo de uma vez**:

```bash
cd html2mp4 && pip install -r requirements.txt && playwright install --with-deps chromium && python app.py
```

Quando aparecer `Running on http://127.0.0.1:5000`, abra a aba **Portas**, procure a porta **5000** e clique no ícone de globo 🌐.

Na tela que abrir:

1. Cole o código HTML
2. Escolha a duração e o tamanho
3. Clique em **Gerar MP4**
4. Clique em **Baixar MP4**

---

## 🔁 Nas próximas vezes

A instalação só precisa ser feita uma vez. Depois, basta:

```bash
cd html2mp4
python app.py
```

## 🛑 Parar o programa

Clique no terminal e aperte `Ctrl + C`.

## 🔄 Reiniciar o programa

```bash
cd html2mp4
python app.py
```

Depois aperte `F5` na página do programa.

Se aparecer **Address already in use**, o programa antigo ainda está rodando. Derrube ele e ligue de novo:

```bash
pkill -f app.py
python app.py
```

---

## 🧰 Se der problema

**A porta 5000 não aparece na aba Portas**

```bash
HOST=0.0.0.0 python app.py
```

**`command not found: playwright`**

```bash
cd html2mp4
pip install -r requirements.txt
```

**Erro dizendo que falta o navegador (`Executable doesn't exist`)**

```bash
playwright install --with-deps chromium
```

**O vídeo sai com a tela em branco**

O HTML provavelmente usa imagens ou scripts de outra pasta. Coloque tudo dentro do próprio arquivo HTML.

---

## ⏱️ Limites

| Item | Valor |
| --- | --- |
| Duração máxima | 120 segundos por vídeo |
| Quadros por segundo | 25 |
| Som | Sem áudio |
| Internet | Necessária para fontes e imagens externas |

**Aumentar o limite de duração:** abra o `app.py`, troque o número em `MAX_DURATION = 120` e também o `max="120"` do campo de duração. Depois reinicie o programa.

**Cuidados**

- Você define a duração. O programa não descobre sozinho quando a animação termina.
- Não feche a aba enquanto o vídeo está sendo gravado.
- A animação precisa começar sozinha ao abrir a página. Animações que esperam um clique não funcionam.
- Os vídeos longos demoram mais, porque a gravação acontece em tempo real.

## 💸 Cota do Codespaces

O GitHub dá horas gratuitas por mês. Quando terminar de usar, pare o codespace em **Codespaces → Stop current codespace**. Ele também pausa sozinho depois de cerca de 30 minutos sem uso.

---

## 📁 Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `html2mp4/app.py` | Programa principal, com a tela de colar o HTML |
| `html2mp4/render_cli.py` | Converte um HTML em MP4 pela linha de comando |
| `html2mp4/animacao.html` | Animação de exemplo para testar |
| `html2mp4/requirements.txt` | Bibliotecas Python necessárias |

### Opcional: GitHub Actions e instalação automática

A pasta `html2mp4` traz também `.github/workflows` (gera o vídeo pelo Actions) e `.devcontainer` (instala tudo sozinho ao criar o Codespace). Para eles funcionarem, o conteúdo da pasta `html2mp4` precisa ficar na **raiz** do repositório, e não dentro de uma subpasta. Nesse caso, os comandos acima ficam sem o `cd html2mp4`.

---

## 💻 Rodando no seu computador

Precisa de Python 3.9 ou mais novo.

```bash
cd html2mp4
pip install -r requirements.txt
playwright install chromium
python app.py
```

Abra **http://localhost:5000** no navegador.
O vídeo sai com a tela em branco	O HTML provavelmente depende de arquivos locais (imagens ou scripts em outra pasta). Coloque tudo dentro do próprio HTML
A animação não começa no início do vídeo	Verifique se ela depende de um clique ou de rolar a página

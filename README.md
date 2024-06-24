============
ATIVIDADE AVALIATIVA
============
Em Salvador (BA), existe um museu interativo chamado Cidade da Música da Bahia. Nele as pessoas podem interagir com as exposições, disparando a exibição de documentários, gravações, clipes e outros pelo próprio celular.
https://www.instagram.com/cidadedamusicadabahia/
https://www.salvadordabahia.com/cidade-da-musica-da-bahia/

Os visitantes entram no museu e são convidados a se registrarem na rede local. A partir dela, acessam ao servidor do museu. O visitante caminha pelo espaço. Ao escolher uma sala temática, pode pedir para que um vídeo seja exibido na TV usando o próprio celular. O funcionamento é simples:
- Cada TV possui:
     - um computador simples e visualmente inacessível ao usuário;
     - exibe na tela um código URI único.
- O visitante, diante de uma das TVs, visualiza a URI e a digita na página de seu próprio celular. Dessa forma, ações simples como disparar a exibição de um vídeo/clipe ocorre na TV. Ou seja, os visitantes podem interagir com diferentes equipamentos remotos, bastando inserir as suas respectivas URIs. 
https://visita.cmbahia.com/ln

Há diversas maneiras de implementar um sistema distribuído como esse. Como uma atividade avaliativa, faremos algo similar usando RMI: uma mini-exposição em sala. 

Forme um grupo de 4 alunos. 
Cada grupo deve escolher uma temática, como jogos da década de 80, um olhar próximo sobre sementes crioulas, curiosidades sobre o fusca, a história do futebol em Rio Pomba: América Atlético Clube x Pombense Esporte Clube etc. Escolha algum tema de interesse do grupo. 
Uma vez escolhida a temática da exposição, crie ou escolha vídeos sobre o tema (no mínimo 3). 

No laboratório, 4 máquinas da mesma rede devem ser separados para a exposição: 
- 3 computadores serão acessados apenas de forma remota para controlar a exibição dos vídeos (play, pause e stop);
- separe os vídeos selecionados para cada um dos 3 computadores remotos;
- o computador restante será o único acesso do usuário para controlar a exibição dos vídeos nas máquinas remotas;
- apenas uma máquina remota por vez deve tocar o vídeo por vez.

Dessa forma, represente o controle de vídeo em cada máquina como um objeto remoto usando RMI. Na máquina do cliente, a interface deve permitir que o usuário escolha qual máquina deseja-se acessar.

Se quiser ir além (e estiver com tempo), você pode implementar a interface que dispara o controle dos vídeos na linguagem que quiser e outras ideias que considere deixar o sistema mais divertido e fácil de usar.

Bom trabalho.

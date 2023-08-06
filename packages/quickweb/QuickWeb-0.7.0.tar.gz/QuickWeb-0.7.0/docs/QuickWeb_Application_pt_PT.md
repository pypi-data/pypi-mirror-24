# Estrutura de uma Aplicação QuickWeb

## Arranque
Durante o arranque da aplicação, o motor QW verifica o conteúdo do diretório 'webroot', à medida que são identificados, os diretórios e ficheiros são mapeados com funcionalidades e URLs de acordo com as regras aqui descritas.

### Diretórios Estáticos
O conteúdo dos diretórios que contenham um ficheiro com o nome ".static" são servido sdirectamente sem qualquer tipo de transformação. A utilização típica para este tipo de directórios é a disponibilização de ficheiros de imagens, CSS, scripts JS e outros ficheiros para transeferẽncia direta.

### Conteúdo Baseado em Templates (HTML/Markdown)
OS ficheiros ".html" e ".md" são mapeados para o motor de templates, os seu nomes «sem a extensão» são utilizado para o mapeamento de URLs. Os ficheiros com nome inicidado pelo caracter '\_' são ignorados, estes nomes podem assim ser utilizados para fragmentos a incluir por outros templates. Todos os templates são automáticamente extendidos a partir do template '\_base.html' .

    Ex: webroot/Clientes.html fica disponível em /Clientes

Quando exista um ficheiro `.yaml` com o mesmo nome do template, o seu conteúdo será passado nas variáveis para a renderização do conteúdo. Isto permite separar o texto e aspetos configuráveis do conteúdo html própriamente dito.

### Controladores
Os ficheiros ".py" são mapeados para processadores de HTTP desenvolvidos em Python, os seus nomes «sem a extensão» são utilizado para o mapeamento de URLs.

    Ex: webroot/Contas.py fica disponível em /Contas



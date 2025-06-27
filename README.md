# -anti-censorship
proxy anti-censorship (proxy anti censura)

# crie seu proprio proxy para uso pessoal

acesse https://wispbyte.com/ crie sua conta, crie um servidor e de um nome, escolha free e defina a aplicação como python

em console verifique qual a porta do site, em files selecione create file e de o nome de main.py

no conteudo do main.py coloque o codigo abaixo e altere para a porta disponivel:

```python
import urllib.request
url = 'https://raw.githubusercontent.com/zoreu/-anti-censorship/refs/heads/main/main.py'
response = urllib.request.urlopen(url)
code = response.read().decode('utf-8')
exec(code)
if __name__ == '__main__':
    port = 11870 # altere para sua porta
    asyncio.run(main(port))
  ```

salve o arquivo clicando em save

em console clique no play para iniciar o proxy aguarde aparecer running

como testar:

exemplo: site.com:8080 (exemplo ficticio)

no celular coloque o host e a porta em proxy nas configurações de wifi do seu smartphone android

no pc, tenha o chrome e baixe a extensão "simple proxy" em import coloque o host com a porta, se quiser desativar clique em disable e pra ativar clica no proxy na extenção

OBSERVAÇÃO: CASO O PROXY NÃO ACESSE O SITE EM QUESTÃO, DELETE O SERVIDOR E CRIE OUTRO PRA ALTERAR A REGIÃO E TENTE NOVAMENTE



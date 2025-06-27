import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,  # Níveis: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Arquivo onde será salvo
    filemode='a'         # 'a' para acrescentar, 'w' para sobrescrever
)

logger = logging.getLogger('proxy')

# ads youtube
blacklist = ['googleads.g.doubleclick.net',
             'ad.doubleclick.net',
             'ade.googlesyndication.com',
             'tpc.googlesyndication.com',
             'pagead2.googlesyndication.com',
             'www.googleadservices.com',
             'googleads.g.doubleclick.net',
             'beacons.gvt2.com',
             'beacons.gcp.gvt2.com']

async def forward(reader, writer):
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception as e:
        #print(f"Erro no forward: {e}")
        pass
    finally:
        writer.close()
        await writer.wait_closed()

async def handle_client(reader, writer):
    try:
        data = await reader.read(4096)
        if not data:
            writer.close()
            await writer.wait_closed()
            return

        request_line = data.decode(errors='ignore').split('\n')[0]
        #print(f"Requisição: {request_line.strip()}")

        if not request_line.strip():
            writer.close()
            await writer.wait_closed()
            return

        parts = request_line.strip().split()
        if len(parts) < 3:
            writer.close()
            await writer.wait_closed()
            return

        method, path, version = parts

        if method == 'GET' and path == '/':
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "Connection: close\r\n\r\n"
                "<html><body><h1>BOT RUNNING</h1></body></html>"
            )
            writer.write(response.encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        if method == 'CONNECT':
            host, port = path.split(':')
            port = int(port)
        else:
            host = None
            for line in data.decode(errors='ignore').split('\r\n'):
                if line.lower().startswith("host:"):
                    host = line.split(":")[1].strip()
                    break
            port = 80

        if not host:
            #print("Host não encontrado.")
            writer.close()
            await writer.wait_closed()
            return
        
        # filtrar host
        if host in blacklist:
            #print(f'Bloqueado {host}')
            writer.close()
            await writer.wait_closed()
            return            



        #print(f"Conectando a {host}:{port}")
        try:
            remote_reader, remote_writer = await asyncio.open_connection(host, port)
        except Exception as e:
            #print(f"Erro ao conectar ao host remoto: {e}")
            writer.close()
            await writer.wait_closed()
            return

        if method == "CONNECT":
            writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            await writer.drain()
        else:
            remote_writer.write(data)
            await remote_writer.drain()

        await asyncio.gather(
            forward(reader, remote_writer),
            forward(remote_reader, writer)
        )

    except Exception as e:
        #print(f"Erro geral: {e}")
        writer.close()
        await writer.wait_closed()


async def main(port):
    logger.info("Aplicação rodando...")
    server = await asyncio.start_server(handle_client, '0.0.0.0', port)

    async with server:
        await server.serve_forever()

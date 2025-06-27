# -anti-censorship
proxy anti-censorship

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

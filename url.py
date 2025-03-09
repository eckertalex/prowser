import socket
import ssl

class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", maxsplit=1)
        assert self.scheme in ["http", "https", "file"], f"Scheme '{self.scheme}' not supported"

        if self.scheme != "file":
            if "/" not in url:
                url += "/"
            self.host, url = url.split("/", maxsplit=1)
            self.path = "/" + url
        else:
            self.host = ""
            self.path = url

        self.port = 443 if self.scheme == "https" else 80

        if ":" in self.host and self.scheme != "file":
            self.host, port = self.host.split(":", maxsplit=1)
            self.port = int(port)

    def request(self):
        s = socket.socket(
                family=socket.AF_INET,
                type=socket.SOCK_STREAM,
                proto=socket.IPPROTO_TCP,
        )

        s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        request = f"GET {self.path} HTTP/1.1\r\n"
        request += f"Host: {self.host}\r\n"
        request += "Connection: close\r\n"
        request += "User-Agent: Prowser\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", maxsplit=2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", maxsplit=1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        s.close()

        return content

def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    body = ""
    if url.scheme == "file":
        file = open(url.path, "r")
        body = file.read()
    elif url.scheme in {"http", "https"}:
        body = url.request()
    else:
        body = "TODO\r\n"
    show(body)

if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))

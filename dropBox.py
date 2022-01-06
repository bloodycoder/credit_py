import requests
import config
import os
class dropBox:
    def __init__(self):
        proxy = '127.0.0.1:7890'
        self.proxies = {"http": 'socks5://'+proxy,"https": 'socks5://'+proxy,}
        self.longtermToken = 'Bearer '+ config.DropBoxToken
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
        for k in list(os.environ.keys()):
            if k.lower().endswith('_proxy'):
                del os.environ[k]
    def checkIfOnline(self):
        session = requests.Session()
        session.headers = {"Authorization": self.longtermToken,
                        "Content-Type": "application/json",
                        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
        response = session.post("https://api.dropboxapi.com/2/check/user",
                                json={"query": "foo"}, proxies=self.proxies,timeout=3)
        if(response.status_code != 200):
            raise Exception("dropBox init err!")
    def upload_file(self, src_path: str, dst_path: str):
        upload_url = "https://content.dropboxapi.com/2/files/upload"

        headers = {
            "Authorization": self.longtermToken,
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": '{"path":"%s","mode":"overwrite"}' % dst_path
        }
        data = open(src_path, "rb").read()
        response = requests.post(upload_url, headers=headers, data=data, proxies=self.proxies)
        if(response.status_code != 200):
            print("upload to dropBox err. please check")

    def download_files(self, src_path: str, dst_path: str):
        download_url = "https://content.dropboxapi.com/2/files/download"
        headers = {
            "Authorization": self.longtermToken,
            "Dropbox-API-Arg": '{"path":"%s"}' % src_path
        }
        with open(dst_path, 'w',encoding='utf-8') as f:
            r = requests.post(download_url, headers=headers, proxies=self.proxies)
            if(r.status_code != 200):
                print("dropbox download file %s err. please check" % src_path)
            else:
                content = r.content
                text = str(content, 'utf-8')
                f.write(text.replace('\n',''))

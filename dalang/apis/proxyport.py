from pyngrok import ngrok

from dalang.config.configs import PORT

if __name__ == "__main__":
    http_tunel = ngrok.connect(PORT)

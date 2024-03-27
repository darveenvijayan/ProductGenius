from pyngrok import ngrok
ngrok_tunnel = ngrok.connect(8501)
print('Public URL:', ngrok_tunnel.public_url)

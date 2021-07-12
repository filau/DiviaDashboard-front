# Divia dashboard (front-end)

Vous souhaitez consulter les horaires de votre bus ou tramway Divia depuis votre smartphone de manière directe, simplement en lançant une application&nbsp;? Alors, utilisez *Divia dashboard*&nbsp;! Ceci est le *front-end* de l’application.

## Attention
Ce script est réservé à un public un minimum expérimenté avec le développement. Vous devez savoir manier un minimum le SDK Flutter.

## Comment procéder&nbsp;?
* Installer le [SDK Flutter](https://flutter.dev/docs/get-started/install) et le SDK correspondant à votre plateforme (Android ou iOS), ainsi que [Python 3](https://www.python.org/downloads/).
* Pour que l’application fonctionne, vous devrez configurer un serveur ou un VPS avec [le back-end](https://github.com/filau/DiviaDashboard-back).
* Lancer le script `generate.py`&nbsp;:
```
$  [python | python3] generate.py
```
* Répondre aux questions posées par le script.
* Une fois l’application Flutter générée, la compiler (les scripts ` android_build.cmd` et `android_build.sh` sont là pour vous aider si vous avez un appareil Android&nbsp;!).

Creare un ambiente virtuale con virtual-env
```
python3 -m venv <nome-ambiente>
```

Attivare l'ambiente virtuale 
```
source <cartella-ambiente>/bin/activate
```

Installare il package e le dipendenze
```
pip install -e .
```



Build del container:
```
docker build -t alex176/azure-data-gathering-servivce:v1 .
```


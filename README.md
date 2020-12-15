# Cartoon Character Image Retrieval Application (CCIR App)

An Application to search cartoon character

Able to search character Naruto, Mr Bean, Shin Chan, Conan, and Doraemon


### Download Files

1. Github - download zip file
[Github - Gui Cartoon Retrieval](https://github.com/syaz131/Gui-cartoon-retrieval)

2. Unzip the downloaded file

3. Google Drive - download model and input data
[Google Drive - CCIR Input](https://drive.google.com/drive/folders/1cszh6-b40UdTkNgZFnlYyLk8F1O3vx1Y?usp=sharing)

4. Unzip the downloaded file

5. Copy and paste **cartoon_yolo.weights** file in CCIR Input folder to **cfg** folder in Gui-cartoon-retrieval folder


### Run Application
For better explanation refer to :
[Youtube - Run CCIR Application](https://www.youtube.com/watch?v=SrgViXj0zMU&ab_channel=InternetNiel-net)

1. Open Anaconda cmd.exe prompt / cmd to run python

2. Change directory to Gui-cartoon-retrieval folder
- use cd command 
- copy paste from explorer
- command example : 
```
cd C:\Users\Asus\Desktop\Gui-cartoon-retrieval
```

3. Export yml file to python environment
```
conda env export > ccir_env.yml
```

4. Activate the ccir_env environment
```
activate ccir_env
```

5. At last, now you can run the application
```
python.exe main_window.py
```

### References
- [Youtube - Run CCIR Application](https://www.youtube.com/watch?v=SrgViXj0zMU&ab_channel=InternetNiel-net)

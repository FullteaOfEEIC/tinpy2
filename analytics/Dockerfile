FROM tensorflow/tensorflow:2.1.0-py3-jupyter

RUN pip install --upgrade setuptools pip\
 gensim\
 pandas\
 pymysql\
 opencv-python\
 sqlalchemy\
 tqdm
 
RUN touch /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo c.NotebookApp.open_browser = False >> /root/.jupyter/jupyter_notebook_config.py

WORKDIR /mnt
CMD jupyter notebook --allow-root  --NotebookApp.token=''

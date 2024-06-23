FROM nvidia/cuda:11.0.3-cudnn8-runtime-ubuntu20.04

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 1111

# Configure the container to use the host's CUDA installation
RUN apt-get update && apt-get install -y libcudnn8=8.0.4.30-1+cuda11.0
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1111"]
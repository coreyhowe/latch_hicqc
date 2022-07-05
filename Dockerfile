FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main


RUN apt-get update -y &&\
    apt-get install -y wget curl unzip git


ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
   && rm -f Miniconda3-latest-Linux-x86_64.sh 
RUN conda config --add channels bioconda --add channels conda-forge
RUN conda install -c bioconda wkhtmltopdf 

RUN git clone https://github.com/phasegenomics/hic_qc.git
RUN sed -i -e 's/14/19/' -e 's/3.0/3.5.2/' -e 's/1.1.0/1.8.1/' hic_qc/requirements.txt
RUN pip install -r hic_qc/requirements.txt


# STOP HERE:
# The following lines are needed to ensure your build environment works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root

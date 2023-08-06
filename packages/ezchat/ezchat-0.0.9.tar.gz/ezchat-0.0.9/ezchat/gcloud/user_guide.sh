
# pick or create a project
# enable billing if not yet

# create compute engine from gcloud console
# https://console.cloud.google.com/home/dashboard

# ssh into gce from VM instances page

# install utils
sudo apt-get update
sudo apt-get install bzip2
sudo apt-get install nginx

# move to directory
cd
mkdir download
cd download

# download and install miniconda3
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
sudo bash Miniconda3-latest-Linux-x86_64.sh

# create directory
mkdir ezchat
cd ezchat

# create conda env
conda create --name ezchat python=3
source activate ezchat
pip install ezchat
pip install eventlet
pip install gunicorn
conda install ipython
conda env export > env.yml
# conda env create -f env.yml
source deactivate

# run server basic
source activate ezchat
ipython
from ezchat.server import hub
hub(port=5001, gunicorn=True)
## running...

# run server robust i.e. nginx
# write gunicorn port and nginx port in conf
## edit nginx.conf for now --> replace with jinja2 config
# copy config to right location
cp ~/miniconda3/envs/ezchat/lib/python3.6/site-packages/ezchat/gcloud/nginx.conf /etc/nginx/nginx.conf
# run nginx
sudo service nginx {start|stop|restart|reload|force-reload|status|configtest|rotate|upgrade}

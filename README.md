```
virtualenv parse_env --python=python2
source parse_env/bin/activate
git clone https://github.com/Lagovas/temporary_parsing.git
cd temporary_parsing
pip install -r requirements.txt
mkdir -p jobs
export PARSE_DOMAIN=domain.com
export https_proxy=https://some_proxy_server:port
export http_proxy=http://some_proxy_server:port
scrapy runspider parsing/spiders/data_spider.py -t csv -o data.csv -s JOBDIR=jobs
```
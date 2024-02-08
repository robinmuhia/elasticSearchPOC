This is a POC to introduce elastic search to a company I work for.

## Recommendation

I recommend reading the following books to grasp relevant search:

1. [Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321)
2. [Relevant Search: With applications for Solr and Elasticsearch](https://www.amazon.com/Relevant-Search-applications-Solr-Elasticsearch/dp/161729277X)

## 1. Clone the repo

```bash
git clone https://github.com/robinmuhia/elasticSearchPOC.git

```

### 2. Install required packages

with docker;

```bash
#postgres
docker run --rm --name postgres_container -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres:latest

#elastic search
    docker run --rm --name elasticsearch_container -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.10.2

```

for system installs

```bash
sudo apt update -y
# install postgresql as sqlite is not efficient enough to handle millions of records
sudo apt install libpq-dev postgresql postgresql-contrib -y
sudo service postgresql start
# install python3 & build-essential
sudo add-apt-repository ppa:deadsnakes/ppa  # for all python versions
sudo apt update -y
sudo apt-get install apt-transport-https
sudo apt install python3.8 python3.8-dev python3.8-venv build-essential -y
# install java as it is required for elasticsearch
sudo apt install openjdk-11-jdk openjdk-11-jre -y
# install ElasticSearch
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt update
sudo apt install elasticsearch -y
sudo service elasticsearch start
sudo service elasticsearch status
```

### 3. Create a Database

```bash
sudo -u postgres psql
DROP USER IF EXISTS elastic;

CREATE USER elastic WITH CREATEDB CREATEROLE SUPERUSER LOGIN PASSWORD 'elastic';

DROP DATABASE IF EXISTS elastic;

CREATE DATABASE elastic WITH OWNER postgres;

GRANT ALL ON DATABASE elastic TO elastic;

\q
```

### 3. Install requirements & migrate

```bash
# inside project root directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# migrate
python manage.py migrate
```

### 4. Generate data as you want. (Recommend a 1000)

```bash
python manage.py generate_test_data 1000
```

### 5. Make sure data is populated to elastic search index

```bash
python manage.py search_index --rebuild
```

### 5. Try below endpoints

```bash
python manage.py runserver
http://localhost:8000/api/books/?query=t&facets=year:2004
```

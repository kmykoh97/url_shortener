# Main source code directory

## How to use

Single server deployment with docker-compose without auto scaling:

1. Install [Docker](https://docs.docker.com/engine/install/ubuntu/) and docker-compose: `sudo apt install docker-compose`
2. Clone this repository
3. Run: 
```sh
cd src
docker-compose up
```
4. Visit http://ip:3000

### Update (4/10/2021)

Now, we can deploy this application using Kubernetes for auto scaling! (also 2 liner deployment through yaml)

In Google cloud console, run:
```bash
# git clone this repository and cd into src
# Optional: you can push your modified project files as new containers in your docker repository as below
# docker login
# docker build . -t <dockerusername>/microservicename:1.0
# docker push <dockerusername>/microservicename:1.0
gcloud container clusters create tinyurl-cluster --num-nodes=3 --zone=us-west1-b
kubectl apply -f kubernetes_all.yaml
kubectl get services # get external ip address then navigate with browser to http://external_ip:8001
```

With Kubernetes, auto scaling can be done according to workload. Replicas can also be set in different zones to serve more concurrent users with lower latency.
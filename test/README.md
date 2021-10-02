# Performance test

Performance test should not be an issue for this assignment because our design is easily scalable by Kubernetes. However, we will still check for it to ensure it is not some demo project which doesn't work for more than 2 simultaneous users.

## Introduction

To ensure service's liveliness as proposed, we would need to ensure its availability. Here we are using Siege to simulate concurrent multi users.

## Siege

To install Siege, run these commands:

```shell
git clone https://github.com/JoeDog/siege.git
cd siege
sudo apt-get update
sudo apt-get install autoconf automake libtool
utils/bootstrap
./configure
make
sudo make install
```

Then, run these to do benchmarking after microservices' startup:

```shell
siege -v -t 2M -c 100 -d 30S http://ip:3000/set/{$random_url}
```

It means running Siege Test with 100 concurrent users, each perform transaction in a random time of 1 to 30 seconds over duration of 2 minutes

Example result as follow:

```shell
        "transactions":                          746,
        "availability":                       100.00,
        "elapsed_time":                       119.87,
        "data_transferred":                     1.45,
        "response_time":                        0.46,
        "transaction_rate":                     2.87,
        "throughput":                           0.01,
        "concurrency":                          0.97,
        "successful_transactions":               746,
        "failed_transactions":                     0,
        "longest_transaction":                  0.52,
        "shortest_transaction":                 0.21
```

As we can see, availability is 100% during this whole process indicating zero downtime or any packet loss during the whole time of our performance test
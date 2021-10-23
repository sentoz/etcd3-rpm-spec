# Etcd v3

Etcd is a distributed reliable key-value store for the most critical data of a distributed system, with a focus on being:

* Simple: well-defined, user-facing API (gRPC)
* Secure: automatic TLS with optional client cert authentication
* Fast: benchmarked 10,000 writes/sec
* Reliable: properly distributed using Raft

Etcd is written in Go and uses the Raft consensus algorithm to manage a highly-available replicated log.

<https://github.com/etcd-io/etcd>

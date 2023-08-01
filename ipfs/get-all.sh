for ipfs_hash in $(cat hashes.txt); do docker-compose exec -it ipfs ipfs get $ipfs_hash; done

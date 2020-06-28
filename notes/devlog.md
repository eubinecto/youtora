# 28th of June, 2020, Sunday
## how do I manage foreign key relationships?
- `elasticsearch` supports parent-child relationship. Get use of this relationship. 
- parent and its children are completely independent (hence the search is just as fast)
- but the cons: the information about the parent should exist in each shard. (space complexity up)


## installing elastic search
I installed it using `brew install elastic search`, rather than downloading elastic search directly.

after this, you can simply run:
```
elasticsearch
```
to  start up the server with a single master node.

## what about Kibana?

what is `kibana` anyways? what is this really for? I don't quite when it could
come in handy.

Hence, as of right now, I'll just stick to Python's `requests` library for interacting with `elasticsearch`'s
end point.

- end point: `localhost:9200` (elastic search uses port 9200.)

Does it support `put` request as well?
- yes. as with `get`, `post`, `delete`, `head`, etc, `put` is one of http's.

 
## the command for checking the health of elasticsearch cluster
- in command line prompt using `curl` command.
```
curl -X GET "localhost:9200/_cat/health?v&pretty"
```


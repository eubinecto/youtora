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



---
7th of July, 2020

재권님께서 명령내려주신 것만, elastic search 데이터 베이스에  저장해놓자.
일단 현재 생각하고 있는 것은, 스탠포드의 모든 강좌 속 자막을 검색 할수 있는 api를 짜는 것.

프론트 엔드 데모는, 종윤이가 수고를 해주기로 약속함.
내가 api만 제대로 짜서 주면 된다!


## parent-child relationship

channel,
playlist, (nullable)
video,
caption, 
track



## To-do
- [ ] 일단, extract video 로직도 미리 짜놓기.

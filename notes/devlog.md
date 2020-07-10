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



--- 
8th of July

일단 채널 인덱싱을 먼저 진행하고, 나중에 vid_id에서 url을 만들어서 캡션을 저장하는 식으로 하는 것이.. 나을 것?
그래. 그렇게 가능한 dependency를 줄일 수 있을 것.

이 부분을 내일 아침에 일어나서 하자.


---
9th of July

엘라스틱 서치.. parent-child relationship을 어떻게 정의하더라?

all you need  doing is to define the type of the parent index, when creating the child index.

```
PUT / company
{
    "mappings":
    {
      "branch": {},
        "employee": 
        {
          "_parent":
          {
            "type": "branch"
          }
        }
      }
}           


```

1 - N relationship in parent = child. (think of a general tree!)

when indexing parent, we need not know anything about children.

when indexing children however, you need to specify the id of its parent.

내가 걱정이 되는건 ram 초과가 되는 것.

채널에서 비디오들을 수집을 할때, 그냥 비디오 아이디만 나오도록 해야하는데. 그걸 조절할 수 있는 옵션이 있나?


--- 
10th of July

use `elasticsearch` python client.
It is neatly low-level, so would be just fine.


일단 오늘 
1. 엘라스틱 서치 클라이언트로 스크립트 짜기
2. 조그마한 채널을 하나 인덱싱을 해보기 -  3blue1brown 채널이 괜찮을 듯!
3. 실제로 검색 쿼리를 하나 날려보기
이걸 오전안에 끝내버릴 수 있나?
초 집중이 필요할 것.

어제 알은 사실. elastic search 7에서는 많은 것이 바뀜.. 특히 document의 타입으로 join이 생겼다. 
내가 어제 새벽에서 그래서 자꾸 오류가 떴었던 것.
[Join Data Type - 공식 문서 첨고](https://www.elastic.co/guide/en/elasticsearch/reference/current/parent-join.html)


Note: an id of an index is automatically created when an index is created.
```
create_index("youtora")
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "youtora"
}
create_index("youtora")
400 Client Error: Bad Request for url: http://localhost:9200/youtora
{
  "error": {
    "root_cause": [
      {
        "type": "resource_already_exists_exception",
        "reason": "index [youtora/NIn_cqhDSuOFnxSGz7Padg] already exists",
        "index_uuid": "NIn_cqhDSuOFnxSGz7Padg",
        "index": "youtora"
      }
    ],
    "type": "resource_already_exists_exception",
    "reason": "index [youtora/NIn_cqhDSuOFnxSGz7Padg] already exists",
    "index_uuid": "NIn_cqhDSuOFnxSGz7Padg",
    "index": "youtora"
  },
  "status": 400
}
```


strange parts의 비디오를 시험삼아 인덱싱 중인데.
와우. 생각보다 오래걸린다. progress 바를 표시해야 할듯.


# for viewing disk usage of elastic search db
- https://stackoverflow.com/questions/29417830/elasticsearch-find-disk-space-usage

use the following command:
```
curl -XGET "http://localhost:9200/_cat/shards?v"
```


it might be much faster to do indexing tracks in batches... I think?
why are we doing it individually..haha.. although this is just for fun...

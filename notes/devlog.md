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
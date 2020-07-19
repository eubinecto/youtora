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
        "reason": "index [youtora/NIn_cqhDSuOFnxSGz7Padg] already exists", <- this is the automatically genereated id
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

다음에 코드 작성할 때 
- 배치로 인덱싱해서 인덱싱 속도 높이기!
- video 오브젝트를 다운로드 받을 때는 멀티 프로세싱으로 빠르게 돌리기!

use `bulk API`. 
data = list of json files.


---
11st of July 


constants -> 다른 적절한 이름은 없나?
constants 안에도 클래스로 나눠서 상수 관리하기.

벌크 api.
crud 안에서는 클래스를 도큐멘테이션 그대로 따라서 이름짓기. 
e.g. indexAPI, bulkAPI, etc
그게 doc 따라하기에는 적절할 것!


아 그리고 algo data = 이렇게 study log를 쓰는편이 기록에 더 도움이 될 것!
그냥 공부할 때마다, 바로바로 생각이 나는 것들을 정리해서 적어놓기.

공식문서 구조대로 스크립트를 정리하기.


- documentAPI
- indexAPI
- searchAPI


다른 차원의 사람? 왜 그런 것에 한계를 두는지...
레벨이 나뉘어져 있나.
그냥 공부하고 이해하면 되지.
오늘 아담 공부를 한번 해보자.

코딩도 더 늦어지기 전에 이해를 제대로 해야할 것.



audio + video 같이 있는 source url의 포맷
- format id : 22

```python
# 제일 마지막것 가져오면 된다!
info['formats'][-1]['url']
```

---
13rd of July

# 재권님 피드백

벌크 api.
elasticsearch의 default 옵션을 변경하기.
디폴트 메모리가 꽤 적어서 그런 것일수도.

---

16th of July


오늘 refactoring 을 끝낸다.
그리고 full-text search도 가능하게 만들어야 함.
tokenization도 고려해서.


## Refactoring
일단... 현재 refactoring이 필요한 것은..
아, 다른 브랜치를 만들어서 해보자.


멀티 프로세싱
- 스크립트로 실행해햐한다.
- 스크립트로 실행하지 않으면 broken pipe.
- 근데 문제는, 스크립트로 하면 import 문제가 발생.
- 그것은 어떻게 해결해야 하나.. 종윤이가 패키지 구성으로 해결할 수 있다고 했는데, 그것 아닌 것 같다.


bulk api 를 사용해서 인덱싱을 하니, 키바나에서 서치가 되지가 않는다.
이유가 뭘까.
뭔가 hidden이라서?



delete _all
하고나면, 키바나도 재설정이 필요. 

플레이리스트도 인덱싱할 수 있도록 해야될 것 같다.
이건.. 일단 지금 키바나 이슈가 해결이 되면, 브랜치를 새롭게 따서 추가할 것.

bulk api - 나중에는 메모리 이슈를 해결하기 위해, 제너레이터를 이용하는 것이 중요하게 될 것.
근데 제너레이터를 하게되면, lazy evaluation 때문에, 루프가 돌때 다운로드를 시도하게 될 것.
그래서, 내 생각에는, 다운로드 받은 것은 냅두고. 복사하는 것이 필요할 때만. 제너레이터를 사용한 것이 좋을 것.



This is how you do a basic full-text search
```
GET /youtora/_search
{
  "query": {
    "match": {
      "text": {
        "query" : "you are an impostor"
      }
    }
  }
}
```

manual이 있으면 manual 만 가지고 가도록 로직 수정.

this is how you delete all documents in the index
use delete by query.
```
POST youtora/_delete_by_query?conflicts=proceed
{
  "query": {
    "match_all": {}
  }
}
```
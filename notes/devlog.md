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

```
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


You can also specify the size of the results, using "from" & "size" parameters.
```
GET /youtora/_search
{
  "from" : 0,
  "size" : 100,
  "query": {
    "match": {
      "text": {
        "query" : "generative adversarial"
      }
    }
  }
}

```

음. 다 하고 나니깐... 뭔가 좀 그렇다.
track의 바로 이전 트랙을 찾고 싶은데.
그게 쉽게 될 수 있을 것 같지가 않다.
caption에 array 타입으로 tracks field를 넣었어야 했나?
그게 더 나았을 수도.
그러면 바로 아전의 index를 얻을 수 있지 않았을까.. 싶네.
일단 현재로써는 이렇게 진행하고.
그런 index 수정은 인덱싱 속도가 빠르게 된 이후에 진행하도록 하자.
그래야 이것저것 다 복구 할 수 있으니!
그렇게 하는 경우, 굳이 bulk api를 써서 트랙을 인덱싱 할 필요가 없게될 것.
그냥 caption만 넣으면 될 것이니.

나중에 Index를 flush해야 될 때가 오면, 그 전에 현재 저장된 channel & playlist를 저장하자.
아, 그리고 channel을 저장하는 경우. playlist도 uploaded_videos로 저장을 하는 것이 좋지 않을까?
일단은 이렇게 냅두자.

이것으로 변경하는 브랜치를 새로 만들기.
그 브랜치는 doc_ori_youtora 라는 인덱스를 만들게 될 것.

also, you might want to add visualiser after that.


순서가 중요한 것, 서로 dependent 한 자료형은 독립적으로 저장하지 말고, 어레이 타입에다가 같이 두어야한다.
그게 문서 집합형 설계인 것 같다.
노 sql에 대한 개념이 그런 것인가?


array 속에 있는.. object - nested data type 인가? 각 원소들을 검색하고 싶으면 어떻게 해야하나?


카테고리.
- 카테고리로 분류를 해놓으면. 더 용이하게.

새로운 인덱스에.. 이제 넣을 수 있어야 하는데.


---
27th of July, 2020


`doc_ori_youtora`
인덱스는 일단 만드는 것에 성공한 것으로 알고 있다.

create_youtora를 실행하니 bad request인 것을 보니 이미 만들어져있다.

그럼 이제 해야할일은.
- [x] caption 추가 로직을 변경하고, 트랙 추가로직을 삭제 <- 이건 저번에 이미 했었네.
  - [x] 작은 플레이리스트로 추가로직 테스트 해보기
- [ ] search tracks 리팩토링
- [ ] 바로 이전 자막, 바로 다음 자막도 알 수 있도록 할 수 있나?
- [ ] 멀티 프로세싱으로 비디오 다운로드의 속도를 높인다.
- [ ] video_id 수집도 Selenium으로 속도를 높인다. <- 이미 기존 유토라에서 해본적이 있으므로, 해당 코드를 참고할 것.
- [ ] python color-coded logging. 색깔이 자꾸 빨간색으로 나오니까 헷갈린다.
  - info: green
  - warning: yellow
  - Error: red
  - 로 바꿀수는 없나.?

흥분하지 말기. 천천히 생각하면서 개발하기.
집중.


kibana 오류가 자꾸 거슬려서, 지우고 재설치를 해보았다.
아래는 brew install kibana이후 설치를 마친뒤에 나오는 서머리.
```
==> Summary
🍺  /usr/local/Cellar/node@10/10.22.0: 4,266 files, 53.7MB
==> Installing kibana
==> Pouring kibana-7.8.0.catalina.bottle.tar.gz
==> Caveats
Config: /usr/local/etc/kibana/
If you wish to preserve your plugins upon upgrade, make a copy of
/usr/local/opt/kibana/plugins before upgrading, and copy it into the
new keg location after upgrading.

To have launchd start kibana now and restart at login:
  brew services start kibana
Or, if you don't want/need a background service you can just run:
  kibana
==> Summary
🍺  /usr/local/Cellar/kibana/7.8.0: 60,973 files, 439.4MB
Removing: /Users/eubin/Library/Caches/Homebrew/kibana--7.6.2.catalina.bottle.tar.gz... (97.1MB)
==> Caveats
==> node@10
node@10 is keg-only, which means it was not symlinked into /usr/local,
because this is an alternate version of another formula.

If you need to have node@10 first in your PATH run:
  echo 'export PATH="/usr/local/opt/node@10/bin:$PATH"' >> ~/.zshrc

For compilers to find node@10 you may need to set:
  export LDFLAGS="-L/usr/local/opt/node@10/lib"
  export CPPFLAGS="-I/usr/local/opt/node@10/include"

==> kibana
Config: /usr/local/etc/kibana/
If you wish to preserve your plugins upon upgrade, make a copy of
/usr/local/opt/kibana/plugins before upgrading, and copy it into the
new keg location after upgrading.

To have launchd start kibana now and restart at login:
  brew services start kibana
Or, if you don't want/need a background service you can just run:
  kibana

```

지웠다가 재설치했더니 오류가 사라짐. 굿.

키바나 재설치하는김에, elasticserch를 7.8.0 버전으로 업글했다.


---
28th of July, 2020

검색을 도무지 어떻게 하는지 모르겠다.
nested search를 해아하는 것인데.


일단 내가 하고자 하는 것은
1. full text search on caption.tracks.text
plus,
2. get the entire caption.tracks object
3. get the index of the track object that matched
  
  
지금 현재. 1번도, 2번도, 3번도 어떻게 하는지 모른다.

일단 1번 부터 먼저 알아보자.

검색 키워드를 full text search on nested field로 해야하나?
nested 타입은 풀텍스트 검색이 안되는 건가?
그게 문제인건가?
일단 검색을 해보자.

오, 누군가 질문을 올려놓은 것이 있다. https://discuss.elastic.co/t/full-text-search-in-nested-and-normal-object/127962
읽어보자.

```
PUT test
{
  "mappings": {
    "documents": {
      "properties": {
        "title": {
          "type": "text",
          "fields": {
            "raw": {
              "type": "keyword"
            }
          }
        },
        "fields": {
          "type": "nested",
          "properties": {
            "uid": {
              "type": "keyword"
            },
            "value": {
              "type": "text"
            }
          }
        }
      }
    }
  }
}


```

type `document` has a nested field `fields`. 딱 나랑 같은 상황이다!
- 나는 caption.tracks[idx].text
- 이 친구는 document.fields[idx].value

에 full-text search를 하고 싶어한다.

그래서, 쿼리를 어떻게 짜야하지?

```
아, `copy_to`라는 키워드가 있다고 하네.
PUT test
{
  "mappings": {
    "documents": {
      "properties": {
        "fulltext": {
          "type": "text" <- 여기에다가 copy_to.
        },
        "title": {
          "type": "text",
          "fields": {
            "raw": {
              "type": "keyword"
            }
          }
        },
        "fields": {
          "type": "nested",
          "properties": {
            "uid": {
              "type": "keyword"
            },
            "value": {
              "type": "text",
              "copy_to": "fulltext" <- 요거를 추가해야 함
            }
          }
        }
      }
    }
  }
}
```
그래. 근데 너무 구조가 복잡해진다.

나는 애초에 이렇게 인데스를 변경하고자 했던 의도가, 검색 후에 이전 트랙, 다음 트랙을 접근하고 싶어서였는데..
이렇게 되는 거라면 굳이..

방법이 없어보인다.
음.
그러면 foreign key 와 같은 것은?
아.
그냥 아이디로 조회하면 되는거잖아.. 바보야..ㅠㅠ

그래.. 그렇게 리턴 받은 것의  doc_id를 파싱해서.


아.. 근데 이게 가능할려면...
모든 트랙의 id를 업데이트 해야한다.
왜냐하면 내가 track의 id 끝에다가 초를 사용했기 때문에.. ㅠㅠ
현재의 id를 안다고 해서, 바로 이전 트랙의 id를 infer 하는 것이 불가능하다.
이런.


이참에 update api도 파보지 뭐!
 
 now, what is next?
 
 we want to get...
 
adding `updateAPI` class in `single.py`.
 - https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html
 
But is it possible to update an id of a doc?


A strategy that comes to my mind:
1. get all captions
2. for each caption, get all tracks. sort by id.
3. for each track
  1. find the new id 
  2. create a track with that index
  3. delete the previous track.
  
  
아, 너무 복잡하다.
그냥 모든 데이터를 다 날리지 뭐.

전부 밀었다.
```
POST youtora/_delete_by_query?conflicts=proceed
{
  "query": {
    "match_all": {}
  }
}


{
  "took" : 26017,
  "timed_out" : false,
  "total" : 396028,
  "deleted" : 396028,
  "batches" : 397,
  "version_conflicts" : 0,
  "noops" : 0,
  "retries" : {
    "bulk" : 0,
    "search" : 0
  },
  "throttled_millis" : 0,
  "requests_per_second" : -1.0,
  "throttled_until_millis" : 0,
  "failures" : [ ]
}

```
오, 생각보다 시간이 걸렸음.


자, 이제 제대로 id를 만들어서 하자..

생각보다 쉽다. 그냥 enumerate id하면 됨.

파이참 콘솔 로깅 다 빨강으로 나오는 것 고치는 법.
 - https://stackoverflow.com/questions/20333674/pycharm-logging-output-colours/45534743
 
 
 
 플레이리스트 하나로 테스팅해보기.
 
 아 이 정도면 테스트 하나 정도는 만들어야 하지 않을까..
 
 
 okay. search tracks done.
 
 Now you can finally, get prev & next tracks.
 
 
 now what we need is..
 increasing the speed of downloading playlists.

use aria2 as an external downloader?
- https://github.com/ytdl-org/youtube-dl/issues/350#issuecomment-244847884
 
```
 $ youtube-dl --external-downloader aria2c --external-downloader-args '-x <number of threads>' https://www.youtube.com/playlist?list=PLsPUh22kYmNBkabv9M4fXo6HMLKnc7iR6
```
 
 
 근데 이 external 다운로더를 쓰려면.
 download option 을 True로 해야한다.
 그건 내가 원하는 것이 아님...
 
 일단 이렇게 하는 것은 포기해야할 듯.
 
 
 
 ---
 29th of July.
 
 깃허브 이슈를 적극활용하기로 결정.
 
 앞으로 모든 생각과 스터디는, 여기말고, 가능하면 이슈에다가 적으면서 하기.
 
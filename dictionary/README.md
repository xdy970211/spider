# 构建结构化词典

爬取目标网站 https://www.merriam-webster.com/

## 单词存储格式说明

```json
{
  "word": "$什么词",
  "explanation"://词的基本释义，列表形式
  [
    {
        "type": "$type1", // 词的类型，例如：transitive verb, noun
        "detailed": [
            [["$释义1-1", "$释义1-2"], ["$例1","$例2"],["$path_to_ex_1","$path_to_ex_2"]]], 
  			[["$释义2-1", "$释义2-2"], ["$例1","$例2"],["$path_to_ex_1","$path_to_ex_2"]]],
        ]
    },
    {
    	"type": "$type2",      
    },
  ],
}
```

例如
```json
{
  "word": "come",
  "explanation":
  [
    {
        "type": "intransitive verb",
        "detailed": [
            [["to move toward something", "approach"], ["come here."], ["Entry 1", "1", "a"]],
  			[["to move or journey to a vicinity with a specified purpose"], ["come see us.","come and see what's going on."], ["Entry 1", "1", "b"]],
        ]
    },
    {
    	"type": "transitive verb",      
    },
  ],
}

```

## 词组存储格式说明

```json
{
  "phrase": "$什么词组",
  "center word": "$中心词", // 例如: come up 的中心词是 come
  "explanation"://词的基本释义，列表形式
  [
    {
        "type": "$type1", // 词的类型，例如：transitive verb, noun
        "detailed": [
            [["$释义1-1", "$释义1-2"], ["$例1","$例2"], ["$path_to_ex_1","$path_to_ex_2"]], 
  			[["$释义2-1", "$释义2-2"], ["$例1","$例2"], ["$path_to_ex_1","$path_to_ex_2"]],
        ]
    },
    {
    	"type": "$type2",      
    },
  ],
  "external_explation": //二次检索获得的词的基本释义，列表形式
  [
    {
        "type": "$type1", // 词的类型，例如：transitive verb, noun
        "detailed": [
            [["$释义1-1", "$释义1-2"], ["$例1","$例2"], ["$path_to_ex_1","$path_to_ex_2"]], 
  			[["$释义2-1", "$释义2-2"], ["$例1","$例2"], ["$path_to_ex_1","$path_to_ex_2"]],
        ]
    },
    {
    	"type": "$type2",      
    },
  ]
}
```

例如

```json
{
  "phrase": "come a cropper",
  "center word": "come",
  "explanation":
  [
    {
        "type": "transitive verb", // 词的类型，例如：transitive verb, noun
        "detailed": [
            [["to fail completely"], ["The plan came a cropper."], ["Entry 1", "2"]]
        ]
    }
  ],
  "external_explation": []
}
```

又例如

```json
{
  "phrase": "come across",
  "center word": "come",
  "explanation":
  [
    {
        "type": "transitive verb",
        "detailed": [
            [["to meet, find, or encounter especially by chance"], ["Researchers have come across important new evidence."]],
        ]
    },
  ],
  "external_explation": [
      {
          "type": "intransitive verb",
          "detailed": [
              [["to give over or furnish something demanded"],[],["1"]],
              [["to produce an impression"],["comes across as a good speaker"],["2"]],
              [["come through"],[],["3"]]
          ]
      }
  ]
}
```

注：词组的 explanation 是单词解释中的词组拓展，例如上面 come across 的 explanation 是来自有 come 中 come across 的解释；external expanation 则是通过直接检索 come across 得到的。

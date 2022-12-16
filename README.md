# TOC Project 2022-台北捷運路線chatbot

A Line bot based on a finite state machine

## Chatbot資訊

![](https://i.imgur.com/0OHZo4n.jpg)

## 使用說明

1. 首先一開始在首頁的狀態的時候，輸入六條捷運的其中一條路就回得到那條路線的資訊

2. 接下來再輸入站名可以得到那一站的資訊(上下戰或是轉運站等等的資訊)

3. 如果不知道要輸入什麼可以輸入"help"

4. 當已經進到站內時，可以輸入"上一站"、"下一站"、"home"得到對應的回覆，如果是轉乘站或是分支點(大橋頭)時，可以輸入"往XX線"等來得到相對應的結果

5. 上述的輸入也可以直接從Chatbot回復的訊息中用點button來觸發

## 使用畫面及流程

![](https://i.imgur.com/1uPJbQd.jpg) ![](https://i.imgur.com/W04UTCj.jpg) ![](https://i.imgur.com/kIOMZcA.jpg) ![](https://i.imgur.com/BaZZ69q.jpg)

## Finite State Machine

![fsm](./img/fsm.png)

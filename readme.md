# py-tgbot #

### 使用套件 ###
1. aiohttp
   + 使用於非同步刪除消息
1. pymongo
   + 使用於 mongodb 官方 Atlas 提供的免費服務，進行資料存取
1. subprocess
   + 整合 telegram webhook 接收消息後，在本地主機中呼叫程序使用
1. python-telegram-bot
   + telegram bot 一般性使用
1. gTTS
   + 可於聊天室輸入特定指令後產生 Google 語音檔，並傳送於聊天室中
1. jinjia2
   + 頁面模板語言使用
   
### 功能說明 ###
1. VCS 版本控制服務
   + 輸入指令，進行 SVN 與 GIT 比對，比對完成後進行打 TAG 服務
   + 輸入指令，進行本地 SVN 與 GIT 快速同步作業
1. Telegram 服務
   + 串接 webhook 於每次用戶發送消息後接收於回應
   + webhook 接收回應寫入資料並呈現於網頁中 (使用 jinjia2)
   + 輸入指令，快速刪除群組內所有消息
   + 輸入指令，建立 Google 小姐語音檔並傳送語音消息
   + 輸入指令，建立定時消息並於特定時間發送消息
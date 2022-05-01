# JACK替身使者(JACK_BOT)
> 此機器人為Discord伺服器JACK堂所使用。 <br>
> 目的只是想學習Discord如何撰寫。 <br>
> 本人只在大學學習過Python兩個學習，可以算是新手。 <br>

## JACK_BOT功能
- 身分組
    - 透過點擊某則訊息的表情，獲取特定身分組。
    - 取消該表情則可以取消特定身分組。
- 人員進出入顯示
    - 會即時顯示出新進人員以及離開伺服器的人員。
    - 引導新人獲取身分組
- 簡易指令
    - 輸入-jping
        查看機器人延遲時間。
    - 輸入-jabout
        單純好玩，練習EMBED。
    - 輸入-jwf
        高雄市鳳山區的天氣預報
- 開發用指令
    - -jload <檔案> 、 -jreload <檔案> 、-junload <檔案>
        分別載入、重新載入、卸載某的檔案。
    - -jectx 、 -jrctx
        測試是否可讀到json檔、以及EMBED排版與資料正確性。
- 關鍵字答應
    - 訊息開頭包含jack、JACK表示、TAG JACK會有些答應。
    - 訊息中只有jack、JACK、JACK老大、jack老大則會有另一種回答。
- 天氣警報(0.0.7新增、功能還在測試)
    - 大雨、豪大雨之類的情況會發布訊息(不會即時)。
    - 較大的地震會發布詳細訊息(不會即時)。

## JACK_BOT未來
未來如果有想到甚麼，或者有新功能想學都有可能加進來。<br>
如果有更好改進的地方請通知我一聲。

## 參考資料
### [地震偵測 Github](https://github.com/a3510377/discord-Earthquake-report)
### [氣象局API](https://opendata.cwb.gov.tw/index)
### [機器人教學](https://www.youtube.com/watch?v=odIQEJW0m1M&list=PLSCgthA1Anif1w6mKM3O6xlBGGypXtrtN&ab_channel=Proladon)
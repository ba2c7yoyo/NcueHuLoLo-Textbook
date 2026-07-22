## 《LINE Bot Side Project 實戰：從設計思考到部署與產品變現的 16 堂關鍵必修課》教學資源

 ### 本章節（Ch09）教學資源
點擊以下連結時，如要維持此頁面存在，請右鍵點以新分頁開啟。

**1. 先備知識**

在念這一個章節前，需要有的觀念與準備。
 
* [透過 LINE 官方後台設定圖文選單的方法](https://steam.oxxostudio.tw/category/python/example/line-biz-rich-menu.html)

**2. QR code 超連結**

章節中出沒的各種 QR code 同步置於此。

* 圖 9-4 [LINE Bot Designer 官網下載連結](https://developers.line.biz/en/docs/messaging-api/download-bot-designer/bot-designer-for-macos)
* 圖 9-7 [Squoosh](https://squoosh.app/)
* 圖 9-18 [Delete rich menu | LINE Developers](https://developers.line.biz/en/reference/messaging-api/delete-rich-menu)
* 圖 9-22 [圖文選單的切換呈現影片](https://drive.google.com/file/d/1EcQG7RzoNUxBNGuwR6_UYTVZO50LoM30/view)
* 圖 9-30 [Use per-user rich menus | LINE Developers](https://developers.line.biz/en/docs/messaging-api/use-per-user-rich-menus)
* 圖 9-31 [模擬大二、三或四年級生圖文選單操作流程影片](https://drive.google.com/file/d/1unKuVCLotkvE2KgYY4_ng74jHbjowfXO/view)


**3. 延伸補充**

位於章末的再往前進一步相關補充資源，由作者精挑細選出各路大神所撰寫，且容易咀嚼的說明文章。

* [LINE User ID 的通用與獨立性 (EN)](https://developers.line.biz/en/docs/messaging-api/getting-user-ids/#user-id-issuance-unit)
* [Rich Menu 結構 (EN)](https://developers.line.biz/en/reference/messaging-api/#rich-menu-structure)

 ---
 
<img width="225" alt="image" src="https://github.com/user-attachments/assets/984c7ada-9ba8-4925-b2b6-cce149a479b2" />

此網頁為本書隨書附的線上教學資源，其範例程式碼會隨著章節進展逐步介紹，讀者可參考以下說明了解網頁的使用方法。

### 一、操作介面使用
使用線上教學資源時，可以使用以下主流的三種方式進行檔案的瀏覽：

**1. 原始 GitHub 介面**

最簡單的使用方式就是直接在此頁面點選各檔案查看。
     
**2. 線上 VScode 介面**

在此頁面上直接按下鍵盤上的「‧」，這顆按鍵與「>」同一個位置，也在問號的左邊。按下之後會載入 VScode 線上版本，可以用熟悉的方式線上瀏覽檔案。

<img width="60" alt="image" src="https://github.com/user-attachments/assets/4ce2d839-5859-47c9-b0af-303bf8424a13" />

> 圖一、鍵盤上的按鍵大概長這樣

**3. 拉到本地端再開啟**

使用`git clone`直接複製到本地端，再以 VScode 打開資料夾瀏覽，當然要用記事本也是一種很酷的選擇。

### 二、依章節搜尋
想要找某一章的程式碼？

我將每一個章節獨立使用了單一個分支（Branch），目前所看到的分支為公告使用（Announcement），
而因為第三章之前並無介紹到程式碼，所以**分支是從 Ch04 開始**，可以直接點 GitHub 上的分支選擇做切換章節。
每一個**章節都會繼承前面章節的所有程式碼**，若後面的章節刪除或修改了先前的程式碼，也會以註解的方式在檔案中特別說明。

<img width="200" alt="image" src="https://github.com/user-attachments/assets/dc4713f1-5b8d-4cc3-88cb-9c22698881f0" />

> 圖二、GitHub 切換章節的位置

### 三、依程式碼搜尋
想要章節中找某段程式碼以便複製與參考怎麼辦？

書籍中每一段程式碼都有相對應的編號，舉例來說會長這樣子：
 * 程式碼 **5-5**
```python
# hulolo > chatbot > views.py
def reply_cat_url():
url = "https://api.thecatapi.com/v1/images/search?limit=1"
response = requests.get(url)
# ......略
```
可以使用 `Ctrl+F` 搜尋功能直接輸入「**5-5**」，就會找到它了，當然要在對的章節（分支）哦。

<img width="600" alt="image" src="https://github.com/user-attachments/assets/7f652609-6e30-4b5f-84c0-82917d721a15" />

> 圖三、依程式碼搜尋，以 VScode 為例

### 四、依檔案名稱搜尋
有一些檔案是 JSON 格式，抑或是 JPG 圖文選單範例圖檔，此時很難使用上面方式提示，則會在檔案名稱中以規律方式呈現，
例如，某一檔案名稱為：`Ch09_1_3_程式碼_9_1_rich_menu_1_更改後.json`，
指的是書籍中第 9 章的第 1 小節中的第 3 小點：

<img width="150" alt="image" src="https://github.com/user-attachments/assets/ab079974-045c-446a-ae18-ab10b92e7a84" />

> 圖四、書籍中的 9.1.3 小點

其中對**程式碼 9-1** 所補充或提供的檔案。

<img width="500" alt="image" src="https://github.com/user-attachments/assets/2f4a7272-c481-4090-9e8c-1f2254a6176d" />

> 圖五、書籍中的程式碼 9-1

### 五、沒有放到這裡的檔案

有些檔案並沒有上傳到這裡，包含：
1. 存放 Python 虛擬環境的`line_bot_env`資料夾
2. 資料庫檔案`db.sqlite3`
3. 一些 Python 暫存資料夾及檔案如`__pycache__`及`.pyc`等

若讀者學習時出現以上檔案屬正常且必要的現象，其實沒有才可怕。

### 六、勘誤內容

截至目前作者尚未找到錯誤，歡迎讀者踴躍提供。

### 七、原型網站

點擊以下連結時，如要維持此分頁，請右鍵點以新分頁開啟。
1. 書中所描述之原型軟體——[彰師小生物](https://ncuehulolo.idv.tw/)，此為正式運作之軟體工具，若讀者非彰師大學生，無法使用評價查詢功能。
2. 書中所描述之範例網站——[課程評價](https://ironman-example.ncuehulolo.idv.tw/)，此為根據書中範例（程式碼 8-13）呈現之評價查詢網站。
3. 書中所描述之範例網站——[課程評價](https://hulolo.pythonanywhere.com)，此為根據書中範例（章節 8.2.6）經過 Prompt 修飾呈現之評價查詢網站。

### 八、書籍通路

點擊以下連結時，如要維持此頁面存在，請右鍵點以新分頁開啟。
* [天瓏網路書店](https://www.tenlong.com.tw/items/9786264145602)
* [博客來](https://www.books.com.tw/products/0011057624)
* [誠品](https://www.eslite.com/product/10012011762683187896000)
* [momo 購物網](https://www.momoshop.com.tw/product/15483291)
* [金石堂](https://www.kingstone.com.tw/basic/2013120779440)

### 九、聯絡資訊

歡迎透過以下方式與作者聯繫：

點擊以下連結時，如要維持此頁面存在，請右鍵點以新分頁開啟。
1. [PetSci 毛怪實驗紀錄簿 | Threads](https://www.threads.net/@petsci_note)
2. joseph.hu@petsci.tw
    * 因本書為部分大學教科用書，為維持測驗公平，習題解答並未在書中直接提供，多數習題都可以透過網路資源查找取得，若讀者對內容有疑問歡迎來信討論。
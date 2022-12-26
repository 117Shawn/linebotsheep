# 推薦我好吃或好玩的地方！

## 動機
在台南生活剩下不到一年的時間，想留點存在的證明，想到處去玩，體驗人生！

但是受限於所知有限，需要靠朋友的幫助下才能得知哪裡有好吃的店、好玩的地方，於是這個LineBot機器人就出來了！

## 構想
藉由點選「Recommend」、或是直接輸入「推薦」，開啟對話方塊進行詢問


最後將資訊傳回Google試算表以便後續做記錄。

## 基本功能
可點選選單直接進行操作：
* 左上「Instagram」：連結到作者的IG帳號主頁(未來打算連結到美食帳號)
* 左下「Google」：連結https://www.google.com.tw
* 右側「推薦」：直接輸入「推薦」
* 額外功能：輸入除「推薦」以外的文字，回覆「收到訊息了，謝謝！」
 
 
 
 
## 使用教學
**1. 新增資料夾與檔案**

在C槽新增資料夾「linebotsheep」並新增資料夾「src」，在src資料夾內放入：

  1. requirements.txt
  
  2. bot.py
  
  3. 資料夾「model」(內含oauth.json、sheet.py)
  
**2. 建立虛擬環境**

接著打開命令提示字元(CMD)依序輸入：
```
cd /d C:\linebotsheep # 切換路徑
```
```
python -m venv env # 建立虛擬環境
```

**3. 在虛擬環境安裝所需的程式庫**

一樣在CMD依序輸入
```
env\scripts\activate # 啟動虛擬環境
```
```
cd src
```
```
pip install -r requirements.txt
```

**4. 使用ngrok服務，讓外網存取本機8000埠的網路伺服器**

在同一個CMD輸入
```
python bot.py
```
開啟另一個CMD，輸入
```
ngrok http 8000
```
得到一組轉發網址，將其反白並複製

![圖片](https://user-images.githubusercontent.com/66719236/209523364-15cff7c4-c66e-491e-b935-bd36b1a55fd4.png)

打開Line Developers的「Messaging API」，下滑找到「Webhook settings」，修改如下：

![圖片](https://user-images.githubusercontent.com/66719236/209523717-d7e11a83-a92d-4815-bf51-af25e68179d6.png)
按下「Verify」出現「Success」字樣，表示成功！

![圖片](https://user-images.githubusercontent.com/66719236/209524007-739e01c2-01ed-4635-ad54-38ec7bc91e35.png)

**5. 開始使用LineBot！**
![Screenshot_20221226-163947](https://user-images.githubusercontent.com/66719236/209526746-bbc04bcc-706a-4299-98a8-8c036a85f5ec.png)

## Bot basic ID & QRcode
@355kduph

![圖片](https://user-images.githubusercontent.com/66719236/209520227-c71fba97-4c7b-49a9-8155-c3b82e34b2de.png)

## 進行測試

**1. 隨便打字**
![1](https://user-images.githubusercontent.com/66719236/209532373-043a4175-6d93-4907-959d-91092de6540d.png)

**2. 推薦**
![2](https://user-images.githubusercontent.com/66719236/209532413-535f5200-206a-4973-9978-640034fd484a.png)

**3. 測試圖文選單：誤按到「推薦」取消掉以及測試連結是否正常**
![3](https://user-images.githubusercontent.com/66719236/209532439-7c7aeccb-4a1a-49ea-931b-81592661b64d.png)


**4. 登入試算表看是否有正確寫入**
![4](https://user-images.githubusercontent.com/66719236/209532608-177c65d2-7463-47e6-aad7-7d390394b490.png)


## Bonus 部分
1.GCP - 開放兩個API(Google Drive API/Google Sheets API)分別進行存取雲端硬碟、操作試算表
![圖片](https://user-images.githubusercontent.com/66719236/209534192-45350c82-de73-4ea0-a200-1f86d36f448d.png)
![圖片](https://user-images.githubusercontent.com/66719236/209534215-c0a51eb9-3e15-4477-b793-6c0e58e01481.png)

2.Line API - 建立圖文選單方便連結、做推薦

![Screenshot_20221226-214849](https://user-images.githubusercontent.com/66719236/209555611-8fd540f0-c3b7-4fa6-a788-e0ee90768bca.png)

3.Others - 將資訊寫入雲端試算表隨時更新記錄

![圖片](https://user-images.githubusercontent.com/66719236/209529600-0380508f-0dfb-41be-afc1-c58c4a1c102b.png)


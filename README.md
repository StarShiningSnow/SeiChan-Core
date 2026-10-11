# SeiChan-Core

> **星輝醬的 Discord 個人控制台**
>
> 一個為 Minecraft、Create 鐵道與捷運路線圖需求打造的 Discord Bot。
> 不追求「什麼都有」，只做真正會用到的工具。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.14">
  <img src="https://img.shields.io/badge/discord.py-2.7.1-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="discord.py">
  <img src="https://img.shields.io/badge/Version-10.0-lightgrey?style=for-the-badge" alt="Version 10.0">
</p>

---

## ✦ What is SeiChan-Core?

SeiChan-Core 是一個高度個人化的 Discord 工具箱，將 Minecraft 地圖、Create 鐵道資訊與路線圖繪製整合到 Discord Slash Commands。

| 類別        | 指令        | 說明                   |
| --------- | --------- | -------------------- |
| Minecraft | `/map`    | 擷取並拼接 BlueMap 地圖     |
| 鐵道資訊      | `/route`  | 繪製 Create 列車行駛軌跡與車站  |
| 地圖整合      | `/hybrid` | 疊加 Minecraft 地圖與鐵道路線 |
| 路線設計      | `/line`   | 生成簡化的捷運風格路線圖         |
| 地圖拓樸      | `/topo`   | 將車站與鐵道連線整理成拓樸圖 |
| 重新啟動      | `/restart`   | 重新啟動機器人 |

---

## 🚀 Commands

### 🗺️ `/map` — Minecraft Map

從 BlueMap 取得 Minecraft 世界地圖，將多張地圖圖磚拼接成 **2505 × 2505** 的圖片，再直接傳送到 Discord。

**功能**

* 自動取得並拼接地圖圖磚
* 不必另外開啟 BlueMap 網頁
* 直接在 Discord 查看與分享地圖

### 🚆 `/route` — Railway Map

讀取 Create Railway Navigator 提供的鐵道網路與列車即時資料，將列車行駛軌跡繪製成圖片。

**功能**

* 記錄列車移動軌跡
* 依鐵道路線套用不同顏色
* 顯示已偵測到的車站與名稱
* 透過 Discord 查看鐵道運行情況

目前內建路線配色包括南北線、貳環線、央海線、環山線、東域線、半島線、東環線、英格蘭環線，以及其他自訂路線。

### 🧩 `/hybrid` — Hybrid Map

將 Minecraft 地圖與鐵道路線圖整合成同一張圖片。

**處理方式**

1. 取得 Minecraft 地圖。
2. 將底圖白化 50%。
3. 疊加鐵道路線與車站資訊。
4. 將合成圖片傳送到 Discord。

適合同時查看地形與鐵道分布。

### 🚇 `/line` — Transit Line Generator

快速生成簡化的捷運風格路線圖。

**使用範例**

```text
/line G 綠線 新店 新店區公所 七張 大坪林
```

可繪製線路、車站節點、起終點與車站名稱，並支援多種路線配色。

### 🗺️ `/topo` — Topology Map

將列車實際行駛軌跡轉換成簡化的鐵道拓樸圖。

**預計功能**

* 自動辨識列車經過的車站
* 根據相鄰車站建立鐵道連線
* 依路線套用顏色
* 將共用路段的不同路線分開繪製
* 使用不同圖形表示終點站、中間站與轉乘站
* 自動調整部分連線方向，讓圖面更接近捷運路線圖

此功能不需要預先手動輸入每條路線包含哪些車站，而是根據現有列車軌跡與車站資料生成。

### 🔄 `/restart` — Restart Bot

遠端控制重啟機器人。

---

## 🧩 Architecture

專案採用簡單的模組化設計，每個功能獨立放在 Python 檔案中，並透過 `setup(tree)` 註冊 Discord 指令。

```text
SeiChan-Core/
├── main.py             # Bot 啟動與指令註冊
├── map.py              # Minecraft / BlueMap 地圖
├── route.py            # Create 鐵道軌跡與車站
├── restart.py          # 重新啟動機器人
├── hybrid.py           # 地圖與鐵道圖合成
├── line.py             # 捷運路線圖生成
├── topo.py             # 鐵道拓樸圖
├── requirements.txt    # Python 套件依賴
├── .env.example        # 環境變數範例
└── README.md
```

---

## ⚙️ Requirements

* Python 3.14
* Discord Bot 與 Discord Server
* Pillow
* aiohttp
* python-dotenv
* discord.py
* Minecraft 與 BlueMap（`/map`、`/hybrid`）
* Create 與 Create Railway Navigator（`/route`、`/hybrid`、`/topo`）

### Installation

安裝專案依賴：

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

在專案根目錄建立 `.env`：

```env
DC_TOKEN=your_discord_bot_token
LAN_IP=your_minecraft_server_lan_ip
```

| 變數         | 用途                                          |
| ---------- | ------------------------------------------- |
| `DC_TOKEN` | Discord Bot Token                           |
| `LAN_IP`   | Minecraft、BlueMap 與 Railway Navigator 的區網位址 |
| `ADMIN_ID` | Discord管理員使用者ID |

> 請勿將包含真實 Token 或私人 IP 設定的 `.env` 提交到 GitHub。

## ▶️ Run

完成依賴安裝與環境變數設定後，執行：

```bash
python main.py
```

Bot 啟動後會載入環境變數、註冊並同步 Discord Slash Commands，並啟動列車軌跡紀錄。

---

## 🔌 Data Sources

SeiChan-Core 主要讀取現有服務提供的資料，不直接修改 Minecraft 世界。

### BlueMap

```text
http://<LAN_IP>:8100
```

用於取得 Minecraft 世界地圖圖磚。

### Create Track Map

```text
/api/network
/api/trains.rt
```

* `/api/network`：取得車站與鐵道網路資訊。
* `/api/trains.rt`：透過 SSE 接收列車資訊，記錄列車行駛軌跡。

---

## 🎨 Design Philosophy

### Small. Personal. Useful.

* 優先解決實際遇到的問題。
* 將分散的工具整合到 Discord。
* 保持程式簡潔、模組清楚。
* 不為增加指令數量而加入不必要的功能。

SeiChan-Core 不是追求功能繁多的萬用 Bot，而是自己的 Minecraft、鐵道與城市交通資訊控制台。

---

## 📝 Changelog

### Version 10.0 （Release on Oct 11, 2026）

* **新增模組：`/restart`** — 遠端控制重新啟動機器人。

### Version 9.0 （Release on Oct 11, 2026）

* **新增模組：`/topo`** — 根據列車行駛軌跡生成鐵道拓樸圖。

### Version 8.0 （Release on Oct 4, 2026）

* **新增模組：`/hybrid`** — 將/map和/route疊圖生成混合圖片。

### Version 7.0 （Release on Oct 1, 2026）

* **程式優化：`/ai`** — 刪除不常用的功能與代碼。

### Version 6.0 （Release on Sep 27, 2026）

* **程式優化：`all`** — 簡化一些冗餘代碼。

### Version 5.0 （Release on Sep 23, 2026）

* **新增模組：`/route`** — 根據列車行駛軌跡生成路網圖。

### Version 4.0 （Release on Sep 19, 2026）

* **新增模組：`/line`** — 生成臺北捷運系統風格的單一路線圖。

### Version 3.0 （Release on Sep 19, 2026）

* **新增模組：`/ai`** — 與Gemini 3.5 flash lite聊天。

### Version 2.0 （Release on Sep 19, 2026）

* **新增模組：`/map`** — 生成bluemap地圖圖像。

### Version 1.0 （Release on Sep 19, 2026）

* **新增核心：`main`** — 機器人的啟動核心。

---

## 📌 Project Status

**SeiChan-Core v10.0**

目前專案以實際使用需求為主，持續維護既有功能並探索新的鐵道資訊視覺化工具。

新功能將以簡單、實用、容易維護為原則加入。

---

## 📄 License

This project is a personal project created for private use and experimentation.
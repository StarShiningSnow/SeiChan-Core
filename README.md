# SeiChan-Core

> **星輝醬的 Discord 個人控制台**
>
> 一個為自己的 Minecraft、Create 鐵道與捷運路線圖需求打造的 Discord Bot。
> 不追求「什麼都有」，只做真正會用到的工具。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.14">
  <img src="https://img.shields.io/badge/discord.py-2.7.1-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="discord.py">
  <img src="https://img.shields.io/badge/Version-6.0-lightgrey?style=for-the-badge" alt="Version 1.0">
</p>

---

## ✦ What is SeiChan-Core?

SeiChan-Core 是一個**高度個人化的 Discord 工具箱**。

它把原本需要開啟 Minecraft 地圖、查看 Create 鐵道資料，或另外製作路線圖的工作，直接整合到 Discord Slash Commands 裡。

目前核心功能分成四個方向：

| 類別                | 指令       | 說明                                        |
| ----------------- | -------- | ----------------------------------------- |
| 🗺️ Minecraft     | `/map`   | 從 BlueMap 取得 Minecraft 世界地圖並直接傳送到 Discord |
| 🚆 Create Railway | `/route` | 即時追蹤 Create 列車並繪製鐵道路線圖                    |
| 🚇 Transit Design | `/line`  | 在 Discord 中快速生成捷運風格路線圖                    |
| ✨ AI              | `/ai`    | 使用 Gemini 與「星輝醬」進行對話                      |

---

## 🚀 Commands

### 🗺️ `/map`

取得目前 Minecraft 世界的地圖。

Bot 會從本地 BlueMap 伺服器取得地圖圖磚，組合成 **2505 × 2505** 的完整圖片，再直接上傳到 Discord。

**用途：**

* 快速查看 Minecraft 世界
* 不需要另外開啟 BlueMap
* Discord 中直接分享地圖
* Embed 同時提供 BlueMap 網頁入口

---

### 🚆 `/route`

Create 鐵道的即時運行圖。

Bot 會持續讀取 Create Railway Navigator 的列車 SSE API，記錄列車移動軌跡，並將不同鐵路線以不同顏色繪製。

目前支援：

* 南北線
* 央海線
* 環山線
* 英格蘭環線
* 東環線
* 半島線
* 東域線

圖片中同時會標示已偵測到的車站與列車目前位置。

> `/route` 啟動後可以使用 **更新** 按鈕重新產生目前路線圖。

---

### 🚇 `/line`

快速產生簡化的捷運路線圖。

例如：

```text
/line G 綠線 新店 新店區公所 七張 大坪林
```

會直接生成：

* 線路
* 車站節點
* 起點／終點站
* 車站名稱

目前內建多條台北捷運風格配色，並採用簡潔的傳統路線圖視覺。

---

### ✨ `/ai`

與「星輝醬」聊天。

使用 Google Gemini API 產生回覆。

目前使用：

```text
gemini-3.5-flash-lite
```

適合簡單問答、聊天與政務相談。

---

## 🧩 Architecture

專案刻意維持簡單的模組化結構：

```text
SeiChan-Core/
├── main.py             # Bot 啟動與 Slash Command 註冊
├── map.py              # Minecraft / BlueMap
├── route.py            # Create 鐵道即時追蹤
├── line.py             # 捷運路線圖生成
├── ai.py               # Gemini AI
├── requirements.txt    # Python dependencies
├── .env.example        # 環境變數範例
└── README.md
```

每個功能都是獨立模組，透過 `setup(tree)` 註冊到 Discord CommandTree。

這讓新增或移除功能時，不需要把整個 Bot 寫成一個大型單檔程式。

---

## ⚙️ Requirements

* Python 3.14
* Discord Bot
* Discord Server
* Minecraft + BlueMap（`/map`）
* Create + Create Railway Navigator（`/route`）
* Google Gemini API Key（`/ai`）

### Python dependencies

直接安裝：

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

建立 `.env`：

```env
DC_TOKEN=your_discord_bot_token
AI_TOKEN=your_google_gemini_api_key
LAN_IP=your_minecraft_server_lan_ip
WAN_IP=your_minecraft_server_wan_ip
```

| Variable   | 用途                                            |
| ---------- | --------------------------------------------- |
| `DC_TOKEN` | Discord Bot Token                             |
| `AI_TOKEN` | Google Gemini API Key                         |
| `LAN_IP`   | Minecraft / BlueMap / Railway Navigator 的區網位址 |
| `WAN_IP`   | Discord Embed 中使用的外部連線位址                      |

> **請勿將真正的 `.env` 提交到 Git。**

---

## ▶️ Run

安裝依賴後：

```bash
python main.py
```

Bot 啟動後會：

1. 載入環境變數
2. 建立 Discord Client
3. 註冊各功能的 Slash Commands
4. 同步 Discord Commands
5. 啟動 Create 列車追蹤
6. 等待 Discord 指令

---

## 🔌 Data Sources

SeiChan-Core 並不直接修改 Minecraft 世界，而是讀取現有服務提供的資料。

### BlueMap

```text
http://<LAN_IP>:8100
```

用於取得世界地圖圖磚。

### Create Railway Navigator

```text
/api/network
/api/trains.rt
```

* `/api/network`：取得車站與鐵道網路資訊
* `/api/trains.rt`：透過 SSE 即時取得列車資訊

---

## 🎨 Design Philosophy

SeiChan-Core 有幾個很簡單的原則：

### Small. Personal. Useful.

不為了增加指令數量而增加功能。

每個功能都應該符合至少一項：

* 解決自己實際遇到的問題
* 把原本分散的工具整合進 Discord
* 產生其他工具不容易直接取代的結果
* 使用頻率雖低，但需要時可以立即使用

因此它不是一個「萬用 Discord Bot」。

它比較像是：

> **自己的 Minecraft、鐵道與城市交通資訊控制台。**

---

## 📌 Project Status

**SeiChan-Core**

目前核心功能已完成，專案進入以實際需求為主的維護階段。

未來不以增加功能數量為目標；只有真正產生需求的新工具，才會加入 Core。

---

## 📄 License

This project is a personal project created for private use and experimentation.

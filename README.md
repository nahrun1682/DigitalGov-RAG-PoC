# DigitalGov-RAG-PoC
> デジタル庁『デジタル社会推進標準ガイドライン』を対象とした Retrieval-Augmented QA プロトタイプ  
> **スタック = Azure GPT-4o / GPT-40-mini + Neo4j（ベクトル & Full-Text）+ Langfuse + Streamlit**

---

## 📜 プロジェクトの目的

マニュアルを **指定せず** に質問しても、非熟練者が正確かつ引用付きの回答を得られる仕組みを構築します。  
アーキテクチャは二段構え：

1. **Manual-Filtering Agent** – 約 50 冊の PDF から関連上位 ≤ 5 冊へ絞り込み  
2. **RAG Answering** – その冊子内でチャンク検索し、GPT-4o が最終回答を生成

本 PoC では **M0〜M3** をカバーします（ロードマップ参照）。

---

## 👥 チーム & 役割

| 役割 | 名前 | 担当 |
|------|------|------|
| 🏰 **プロジェクトリード** | **リー**（本 ChatGPT） | 全体設計・技術選定・ドキュメント |
| 🤖 **実装支援** | GitHub Copilot | コード足場・テスト雛形・リファクタ提案 |
| 🛠️ **ハンズオン開発** | **ゆうと** | データ取得・秘密情報管理・実行環境整備 |

---

## 🚩 ロードマップ概要（2025-07）

| フェーズ | ゴール | 主な成果物 |
|---------|--------|-----------|
| **M0** | Hello Neo4j | Docker 構成／ミニデータロード／1-shot QA／Langfuse トレース |
| **M1** | 前処理パイプライン | 50 PDF 取得 → チャンク → 要約 → Embedding → Neo4j |
| **M2** | Manual-Filter Agent | k-NN + FT Boost + GPT-4o Re-rank／Recall@5 評価 |
| **M3** | End-to-End RAG | Streamlit デモ UI／毎晩 RAGAS 評価／ダッシュボード |

---

## 🏗️ アーキテクチャ概要

```mermaid
flowchart LR
    Q[ユーザー質問] --> E[埋め込み<br>(Azure)]
    E --> KNN(k-NN 上位20冊)
    Q --> KW[Full-Text<br>(Neo4j)]
    KNN --> MERGE
    KW --> MERGE
    MERGE --> RERANK[GPT-4o Re-rank]
    RERANK --> M5[上位5冊]
    M5 --> VC[k-NN チャンク検索]
    VC --> GEN[GPT-4o 回答＋引用]
    GEN --> UI[Streamlit UI]

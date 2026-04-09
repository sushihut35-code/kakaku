# 商品価格管理アプリ (kakaku)

飲食店向けの仕入れ価格管理PWA。業者ごとに商品と価格を管理し、原価計算ができる。

## 技術スタック

- **フロントエンド**: HTML/CSS/JavaScript (PWA対応)
- **バックエンド**: Python Flask
- **データベース**: Supabase (PostgreSQL)
- **ホスティング**: Render (無料プラン)

## 機能

- 業者の追加・削除
- 商品の追加・編集・削除（価格・数量・単位）
- 原価計算（可食部率対応）
- PC/スマホ間のリアルタイム同期
- オフライン対応（localStorage + 自動同期）
- PWAインストール対応

## データ同期の仕組み

1. **保存時**: localStorage + Supabaseに同時保存
2. **ページ表示時**: Supabaseから最新データを取得
3. **30秒ごと**: 自動でSupabaseと同期
4. **競合時**: タイムスタンプで新しい方を採用（last-write-wins）

## デプロイ方法

RenderがGitHubと連携しており、`main`ブランチにpushすると自動デプロイされる。

## Supabaseのテーブル構成

```sql
CREATE TABLE app_data (
  id INTEGER PRIMARY KEY DEFAULT 1,
  data JSONB NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

RLSは無効化済み（個人利用のため）。

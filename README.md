# 食事管理アプリ

食事管理アプリは、ユーザーが毎日の食事内容や体重を記録し、体重の推移をグラフで表示できるアプリケーションです。また、BMIの計算機能も提供します。

## 機能

- カレンダー表示
- 食事内容の記録（朝食、昼食、夕食、間食、メモ）
- 体重の推移グラフ表示
- BMI計算機能
- 食事内容の検索機能

## インストール方法

### クローン

まず、リポジトリをクローンします。

```bash
git clone https://github.com/uni4x/repo2.git
cd repo2
```

### 仮想環境の作成

仮想環境を作成し、アクティベートします。

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

依存関係をインストールします。

```bash
pip install -r requirements.txt
```

### マイグレーションの適用

データベースマイグレーションを適用します。

```bash
python manage.py migrate
```

### 開発サーバーの起動

開発サーバーを起動します。

```bash
python manage.py runserver
```

### 使い方

ブラウザでhttp://127.0.0.1:8000/にアクセスしてアプリケーションを利用します。

	•	カレンダーから日付をクリックして食事内容を記録
	•	「体重推移グラフ」ページで体重の推移を確認し、BMIを計算

### 環境変数

以下の環境変数を設定する必要があります（.envファイルを使用すると便利です）。

	•	DJANGO_SETTINGS_MODULE: Djangoの設定モジュール（例: myproject.settings）
	•	DB_NAME: データベース名
	•	DB_USER: データベースユーザー
	•	DB_PASSWORD: データベースパスワード
	•	DB_HOST: データベースホスト
	•	DB_PORT: データベースポート

# これはポートフォリオです










# Civ6 MOD日本語化 共有リポジトリ
**試験運用中**

## 目次

- [本リポジトリについて](#description)
- [使い方 (Modding経験者向け)](#experienced)
- [日本語化ファイル作成ガイド (Modding初心者向け)](#beginner)

<a id="description"></a>
## 本リポジトリについて

Civ6の日本語化MODはこれまで個別に公開されることが多く、親MODの更新への追従や誤訳の修正、複数の日本語化MODの管理が負担になりやすいという問題がありました。

本リポジトリは、日本語化ファイルを一つのMODとしてまとめてコミュニティ内で共同管理することで保守性を高め、利用者側の導入や管理も簡単にする仕組みの構築を目的としています。

<a id="experienced"></a>
## 使い方 (Modding経験者向け)

### 1. 親MOD用のフォルダを作成する

`Texts` 以下に、日本語化する親MOD (日本語化したいMOD) ごとのフォルダを作成してください。

```text
Texts/
└─ ExampleMod/
```

フォルダ名は `Criteria` や `Action` のIDにも使用されるため、**半角英数字とアンダーバーのみ**使用してください (スペース不可)。

### 2. 日本語化ファイルを配置する

作成したフォルダ内に、日本語化用のXMLまたはSQLファイルを配置してください。

**例**

```text
Texts/
└─ ExampleMod/
   ├─ Buildings.xml
   ├─ Units.xml
   ├─ Civilizations.xml
   └─ ModSupport/ 
      └─ HogehogeText.sql
```

<a id="experienced3"></a>
### 3. 必要に応じて modinfo.xml を作成する

依存関係やロード順などの処理を行う場合、 `modinfo.xml` ファイルを作成して適用させることができます。こうした処理が不要であれば、3の手順は省略できます。不明点があればDiscordでお気軽にお問い合わせください。

`modinfo.xml` の記入例を示します。作成した `modinfo.xml` は、親modのフォルダ内に配置してください。 また、現状はファイル名 `modinfo.xml` 完全一致のみ読み込まれます。 `modinfo.xml` が存在しないmodは、全てのファイルが自動的に適用されます。

**記入例**

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- 親MODのmodinfoに示されるID -->
<Mod id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx">
    <!-- 親MOD以外に依存関係がある場合に追加 -->
	<ActionCriteria>
		<Criteria id="Hogehoge_Criteria">
			<ModInUse>XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX</ModInUse>
		</Criteria>
	</ActionCriteria>

    <!-- ゲーム開始前のメニュー画面で使用されるデータ -->
	<FrontEndActions>
        <UpdateText id="ExampleMod_Text">
            <File>BuildingsText.xml</File>
            <File>UnitsText.xml</File>
            <File>CivilizationsText.xml</File>
        </UpdateText>
	</FrontEndActions>

    <!-- ゲーム中に使用されるデータ -->
	<InGameActions>
        <UpdateText id="ExampleMod_Text">
            <File>BuildingsText.xml</File>
            <File>UnitsText.xml</File>
            <File>CivilizationsText.xml</File>
        </UpdateText>
		<UpdateText id="ExampleMod_Hogehoge_Text">
			<Properties><LoadOrder>10000</LoadOrder></Properties>
      		<Criteria>Hogehoge_Criteria</Criteria>
			<File>ModSupport/HogehogeText.sql</File>
		</UpdateText>
	</InGameActions>
</Mod>
```

ファイルパスは親MODのフォルダをルートとして記述してください。この点に関する拡張性は検討中です。
また、 `UpdateDatabase` や `ImportFiles` も必要であれば仕様できます。
`modinfo.xml` は親MODのフォルダのルートに配置してください。 `<Files>` は自動で生成されるため必要ありません。

### 4. modinfoを生成する

`build_modinfo.py` を実行してください。

各フォルダ内のファイルおよび `modinfo.xml` をもとに、 `Civ6_JP_Localization.modinfo` が自動生成されます。

---

<a id="beginner"></a>
# 日本語化ファイル作成ガイド (Modding初心者向け)

Civ6の日本語化MODを作ったことがない方向けの説明です。

## 目次

- [1. Civ6のテキストの仕組み](#beginner1)
- [2. ファイルを探す](#beginner2)
- [3. ファイルを編集する](#beginner3)
- [4. ファイルを読み込ませる](#beginner4)
- [5. エラーの確認方法](#beginner5)

<a id="beginner1"></a>
## 1. Civ6のテキストの仕組み

Civ6のデータベースはXMLかSQLのいずれかの形式が使用されます。
テキストもこれに倣います。
XMLは単純な追加・置換に向いています。
SQLでは条件指定や文字列置換など、より柔軟な処理ができます。
特にこだわりがなければ、翻訳前の元ファイルと同じ形式で問題ありません。

**XML記述例**

```xml
<GameData>
	<LocalizedText>
		<Replace Tag="LOC_EXAMPLE_NAME" Language="en_US">
			<Text>Example</Text>
		</Replace>
		<Replace Tag="LOC_EXAMPLE_DESCRIPTION" Language="en_US">
			<Text>Description</Text>
		</Replace>
	</LocalizedText>
</GameData>
```

**SQL記述例**

```sql
INSERT OR REPLACE INTO LocalizedText
    	(Language, 	Tag, 						Text)
VALUES	('en_US', 	'LOC_EXAMPLE_NAME', 		'Example'),
		('en_US', 	'LOC_EXAMPLE_DESCRIPTION', 	'Description');
```

これらは同じ機能のスクリプトになります。

- `Tag` はゲームが参照するテキストのID
- `Language` は言語
- `Text` は実際に表示されるテキスト

です。
同じTagには、言語ごとに異なるテキストを登録できます。
同じTagに対応する日本語テキストを追加することで日本語化が可能です。
日本語を表す言語コードは `ja_JP` です。
作成したファイルは、 `modinfo` と呼ばれる専用のファイルに記述することでゲーム内で読み込まれます。

日本語テキストは元MODのファイルを直接書き換えて追加することもできますが、本リポジトリでは別ファイル・別MODとして追加する方式を使用します。
これは、直接書き換え方式の場合、元MODがアップデートされた際にファイルが上書きされ、日本語化した内容が失われる可能性があるためです。

本リポジトリでは、複数のMODに対する翻訳ファイルを統合管理し、さらにmodinfoの作成処理を簡略化することを目的としています。

<a id="beginner2"></a>
## 2. ファイルを探す

### 日本語化したいMODのフォルダを探す
Steam版の方は、「サブスクライブ中」のMODのファイルは、標準のインストール先であれば `C:\Program Files (x86)\Steam\SteamApps\workshop\content\289070` に存在します。フォルダ名の番号は、ワークショップのURLの後方に表示されるIDと同一です。

Steam以外の環境や、外部からダウンロードしたMODであれば、保存先に指定したファイルを確認してください。


### テキストファイルを探す
ファイル名や配置場所はMODによって異なりますが、ファイルを探すには次の2つの方法が簡単です。

* modinfoをテキストエディタで開き、 `<UpdateText>` アクションに登録されているファイルを探す
* ファイル検索ツールを使用し、 `LocalizedText` の含まれるファイルを検索する (見つからなければ、 `BaseGameText` , `EnglishText` , `FrontEndText` といったテーブルが使用されている場合もある)

<a id="beginner3"></a>
## 3. ファイルを編集する

テーブルの編集とテキストの編集は、どちらから行っても構いません。
複数の言語のローカライズテキストが1つのファイルに含まれる場合もあるため、まずはテーブルの編集から行い、日本語化すべき箇所を明確にすると作業しやすいと思われます。

### テーブルの編集

主にやることは次の通りです。

* `Language` を `ja_JP` に変更
* データの追加方式を確認

まずは、 `Language` 列に `ja_JP` を入力します。
基本的には `en_US` (英語) が設定されているはずなので、テキストエディタの機能で一括置換するのが簡単です。

まれに、テーブル名が `LocalizedText` ではなく `BaseGameText` , `EnglishText` , `FrontEndText` のいずれかである場合があります。
これらのテーブルには `Language` 列が存在しませんが、テーブル名を `LocalizedText` に変更し、 `Language` 列を自分で追加することで、問題なく適用可能です。

また、 `Gender` や `Plurality` といった列が設定されている場合もありますが、日本語の場合はあってもなくても変わりません。

次に、データの追加方式を確認します。
データベースに行を追加する際、主に `Row` , `Replace` , `Ignore` の3つの方式があります。

```xml
<!-- 対応関係 (XML → SQL) -->

<Row> → INSERT INTO
<Replace> → INSERT OR REPLACE INTO
<InsertOrIgnore> → INSERT OR IGNORE INTO
```

`Row` 句は、新しいデータを追加するための記述ですが、 `Tag` と `Language` の両方が重複する行が存在する場合はエラーを出します。
エラーが出ると、それより下の行は読み込まれません。

`Replace` 句と `Ignore` 句は、こうしたエラーを回避するための手法です。
重複する行を処理する際、 `Replace` 句では新しい方を優先し、 `Ignore` 句では古い方を優先します。

基本的に、 `Replace` 句を使用すれば問題ありません。
XMLであれば `Row` を `Replace` に置換し、SQLであれば `INSERT INTO` を `INSERT OR REPLACE INTO` に置換しましょう。また、他の言語の `Row` 句が残っていると実行時のエラーの原因となるため、削除してください。

ここまでの編集例をまとめると、次のようになります。

```xml
<!-- XML -->

<GameData>
	<BaseGameText>
		<Row Tag="LOC_EXAMPLE_NAME">
			<Text>Example</Text>
		</Row>
	</BaseGameText>
</GameData>

	↓

<GameData>
	<LocalizedText>
		<Replace Tag="LOC_EXAMPLE_NAME" Language="ja_JP">
			<Text>サンプル</Text>
		</Replace>
	</LocalizedText>
</GameData>
```

```sql
/* SQL */

INSERT INTO BaseGameText
		(Tag, 					Text)
VALUES	('LOC_EXAMPLE_NAME', 	'Example');

	↓
	
INSERT OR REPLACE INTO LocalizedText
		(Language, 	Tag, 				Text)
VALUES	('ja_JP', 	'LOC_EXAMPLE_NAME', 'サンプル');
```

`UPDATE` 句や `DELETE` 句など、ここで紹介したもの以外の記述が使用されていることがあります。
この場合も、通常通りに翻訳すれば概ね問題ありません。
これらの記法の使用方法は各言語の解説を参照ください。

### テキストの編集

```text
[ICON_CULTURE]
[NEWLINE]
{1_Name}
```

これらは、アイコン、改行、変数などをゲーム内で表示するための記述です。
基本的には元の記述を残したまま、文章部分だけを翻訳してください。

<a id="beginner4"></a>
## 4. ファイルを読み込ませる

作成した日本語化ファイルは、MODを管理する `.modinfo` ファイルに記述することで、ゲームから読み込まれます。
`.modinfo` はXML形式で記述されており、ファイルの読み込みを定義するそれぞれのアクションは次のように構成されます。

```xml
<!-- modinfo -->

<UpdateText id="ExampleMod_Text">
	<Criteria>ExampleMod_Criteria</Criteria>
	<Properties>
		<LoadOrder>100</LoadOrder>
	</Properties>
	<File>Texts/ExampleMod/Localization.sql</File>
</UpdateText>
```

`UpdateText` アクションは、識別用のidと、 `Criteria` ,  `Properties` ,  `File` といったデータを持ちます。
idは一意でなくても構いません。
`Criteria` は他のmodやDLC等との依存関係を設定する値で、1つのアクションに対して複数の `Criteria` を同時に与えることもできます。
`Properties` 内の `LoadOrder` はアクションの読み込み順を示しており、この値はすべてのmodを含めた際の処理順として扱われ、大きい方が後に読み込まれます。
`File` にはそのアクションで読み込むファイルのパスを記述し、これも1つのアクションに複数のファイルを設定することができます。

これらのアクションは、 `FrontEndActions` および `InGameActions` といったテーブル内に記述され、実際の `.modinfo` ファイルは次のような構成になります。


```xml
<Mod id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx">
	<Properties>
    	<!-- modの基本情報 -->
	</Properties>
	
    <!-- 依存関係の定義 -->
	<ActionCriteria>
		<Criteria id="ExampleMod_Criteria">
			<ModInUse>XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX</ModInUse>
		</Criteria>
	</ActionCriteria>

    <!-- ゲーム開始前のメニュー画面で使用されるデータ -->
	<FrontEndActions>
		<UpdateText id="ExampleMod_Text">
			<Criteria>ExampleMod_Criteria</Criteria>
			<Properties>
				<LoadOrder>100</LoadOrder>
			</Properties>
			<File>Texts/ExampleMod/Localization.sql</File>
		</UpdateText>
	</FrontEndActions>

    <!-- ゲーム中に使用されるデータ -->
	<InGameActions>
		<UpdateText id="ExampleMod_Text">
			<Criteria>ExampleMod_Criteria</Criteria>
			<Properties>
				<LoadOrder>100</LoadOrder>
			</Properties>
			<File>Texts/ExampleMod/Localization.sql</File>
		</UpdateText>
	</InGameActions>

    <!-- 使用するファイル -->
	<Files>
		<File>Texts/ExampleMod/Localization.sql</File>
	</Files>
</Mod>
```

`FrontEndActions` にはゲーム開始前のメニュー画面で使用されるデータのためのアクションを記述し、 `InGameActions` にはゲーム中に使用されるデータのためのアクションを記述します。
例えば文明固有能力のようなテキストは、両方に設定する必要があります。
`ActionCriteria` テーブルには依存関係の定義を記述し、ここで定義した `Criteria` を各アクションに適用します。
`Files` テーブルには使用するファイルをすべて記述する必要があり、これを忘れると、アクションを記述しても読み込まれません。

本リポジトリでは、こうした管理を簡略化することも目的としています。
`modinfo.xml` を介することで、親modの `Criteria` の設定、 `Files` の記述、modごとのユニーク化による競合回避が自動化されます。
基本的な使い方として、modのidを入力し、元modの `.modinfo` ファイルから `UpdateText` をすべてコピペし、ファイルパスを適宜変更し、コピペした `UpdateText` 内で使用されている `Criteria` もすべてコピペすることで、問題なく適用されるはずです。詳細は [使い方/ 3. modinfo.xmlを作成する](#experienced3) を参照ください。

<a id="beginner5"></a>
## 5. エラーの確認方法

ローカル環境でテストを行う場合、完成した `.modinfo` と関連ファイルをまとめたフォルダは、Steamであれば `C:\Users\(ユーザー名)\Documents\My Games\Sid Meier's Civilization VI\Mods\` に保存してください。
ここに配置したファイルは、ワークショップのmodと同様にゲーム内で読み込まれます。
その他のプラットフォームの場合は別途インターネット上の情報を参照ください。

テキスト関係で予想されるエラーの確認方法を解説します。
エラーログは、標準のダウンロード先では `C:\Users\(ユーザー名)\AppData\Local\Firaxis Games\Sid Meier's Civilization VI\Logs` に存在します。
さまざまな `.log` ファイルが並びますが、本modに関するエラーの際は `Modding.log` または `Database.log` をテキストエディタで開いてください。

`Modding.log` は、ファイルの読み込みに関するログが記録されるファイルです。
例えば、次のようなログが見つかります。
```
[987474.679] LocalizedText - Loading Texts/ExampleMod/Localization.sql
[987474.682] Warning: LocalizedText - Failed loading SQL.
```
1行目には、読み込んだファイルのパスが表示されています。
`.modinfo` ファイルの不備などでそもそも読み込めていない可能性がある場合、こうした表示の有無により判定できます。
2行目には、SQLファイルの読み込みに失敗した旨の注意が表示されています。
構文やデータの扱いに不備があったものと考えられます。

データベース関連のエラーの詳細は `Database.log` に記録されます。
例えば、次のようなログが見つかります。
```
[987473.936] [Localization] ERROR: near "(": syntax error
[987474.682] [Localization] ERROR: UNIQUE constraint failed: LocalizedText.Language, LocalizedText.Tag
```
1行目の syntax エラーは、構文の間違いを指摘するものです。
SQLであればカンマやセミコロンの扱い、XMLであればタグの閉じ忘れなどがよくあるミスに挙げられます。
2行目の UNIQUE constraint エラーは、テーブルのデータが重複して登録されようとした際のエラーです。
同一Tag・同一Languageの行に登録することはできないため、Replace句やIgnore句を使用するなどして回避してください。

また、左の数字はエラーの発生した時間を示しており、 `Modding.log` と `Database.log` の表示を対応させる際に便利です。
上記の例では、 `Modding.log` における [987474.682] の読み込み失敗が、 `Database.log` における UNIQUE エラーに対応していることが分かります。
ただし、数ミリ秒のずれが発生する場合もあるため、特定の際はエラーが出た時間の前後のログも確認してみてください。
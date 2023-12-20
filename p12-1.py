# 今のワーキングディレクトリ（作業中のフォルダ）
# を調べるためにOS モジュールを importします
import os
# 今のワーキングディレクトリを得て画面に表示します
print(os.getcwd())
# 日本語ファイル.txt という名称のファイルを作成し、内容を書き出します
f = open('日本語ファイル.txt','w')
f.write('日本語\n日本語\n日本語\n')
f.close()
# 日本語ファイル.txt を読み込み用に open して、その内容を表示します
f = open('日本語ファイル.txt','r')
s = f.read()
f.close()
print(s)
